export default function TeacherCard({ teacher }) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="font-semibold text-slate-900">{teacher.name}</h3>
      <p className="mt-1 text-sm text-slate-600">{teacher.email}</p>
      <p className="mt-3 text-sm text-slate-700">
        ★ {Number(teacher.average_rating).toFixed(1)} average · {teacher.course_count} courses ·{" "}
        {teacher.student_count} students
      </p>
    </article>
  );
}
