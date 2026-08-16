from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.attendance import Attendance, AttendanceStatus
from app.models.course import ClassGroup
from app.models.user import User, UserRole
from app.schemas.academic import AttendanceMarkRequest, AttendanceOut, AttendanceSummaryOut
from app.services.academic_access import (
    assert_can_manage_class,
    assert_enrolled_in_class,
    can_view_class,
    enrolled_students,
    load_class,
)


def _to_out(row: Attendance) -> AttendanceOut:
    student = row.student
    class_group = row.class_group
    course = class_group.course if class_group else None
    return AttendanceOut(
        id=row.id,
        student_id=row.student_id,
        student_name=student.name if student else "",
        class_id=row.class_id,
        class_name=class_group.name if class_group else "",
        course_title=course.title if course else "",
        date=row.date,
        status=row.status,
    )


def mark_attendance(db: Session, payload: AttendanceMarkRequest, actor: User) -> list[AttendanceOut]:
    class_group = load_class(db, payload.class_id)
    assert_can_manage_class(class_group, actor)
    roster_ids = {student.id for student in enrolled_students(db, class_group)}
    if not roster_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No enrolled students in this class")

    results: list[Attendance] = []
    for record in payload.records:
        if record.student_id not in roster_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student {record.student_id} is not enrolled in this course",
            )
        existing = (
            db.query(Attendance)
            .filter(
                Attendance.student_id == record.student_id,
                Attendance.class_id == class_group.id,
                Attendance.date == payload.date,
            )
            .first()
        )
        if existing:
            existing.status = record.status
            results.append(existing)
        else:
            row = Attendance(
                student_id=record.student_id,
                class_id=class_group.id,
                date=payload.date,
                status=record.status,
            )
            db.add(row)
            results.append(row)
    db.commit()
    ids = [row.id for row in results]
    rows = (
        db.query(Attendance)
        .options(
            joinedload(Attendance.student),
            joinedload(Attendance.class_group).joinedload(ClassGroup.course),
        )
        .filter(Attendance.id.in_(ids))
        .all()
    )
    return [_to_out(row) for row in rows]


def list_attendance(
    db: Session,
    actor: User,
    *,
    class_id: int | None = None,
    on_date: date | None = None,
) -> list[AttendanceOut]:
    query = db.query(Attendance).options(
        joinedload(Attendance.student),
        joinedload(Attendance.class_group).joinedload(ClassGroup.course),
    )
    if actor.role == UserRole.student:
        query = query.filter(Attendance.student_id == actor.id)
        if class_id:
            class_group = load_class(db, class_id)
            assert_enrolled_in_class(db, class_group, actor)
            query = query.filter(Attendance.class_id == class_id)
    else:
        if not class_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="class_id is required")
        class_group = load_class(db, class_id)
        assert_can_manage_class(class_group, actor)
        query = query.filter(Attendance.class_id == class_id)
    if on_date:
        query = query.filter(Attendance.date == on_date)
    rows = query.order_by(Attendance.date.desc(), Attendance.student_id.asc()).all()
    return [_to_out(row) for row in rows]


def attendance_summary(db: Session, actor: User, *, class_id: int) -> list[AttendanceSummaryOut]:
    class_group = load_class(db, class_id)
    if not can_view_class(db, class_group, actor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot view this class")

    if actor.role == UserRole.student:
        students = [actor]
    else:
        assert_can_manage_class(class_group, actor)
        students = enrolled_students(db, class_group)

    summaries: list[AttendanceSummaryOut] = []
    for student in students:
        rows = (
            db.query(Attendance)
            .filter(Attendance.class_id == class_id, Attendance.student_id == student.id)
            .all()
        )
        present = sum(1 for row in rows if row.status == AttendanceStatus.present)
        late = sum(1 for row in rows if row.status == AttendanceStatus.late)
        absent = sum(1 for row in rows if row.status == AttendanceStatus.absent)
        total = len(rows)
        attended = present + late
        percent = round((attended / total) * 100, 1) if total else 0.0
        summaries.append(
            AttendanceSummaryOut(
                student_id=student.id,
                student_name=student.name,
                class_id=class_group.id,
                class_name=class_group.name,
                present=present,
                late=late,
                absent=absent,
                total=total,
                percent_present=percent,
            )
        )
    return summaries
