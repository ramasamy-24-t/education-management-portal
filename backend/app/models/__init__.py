from app.models.user import User, UserRole
from app.models.course import Course, ClassGroup
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance, AttendanceStatus
from app.models.assignment import Assignment, AssignmentSubmission
from app.models.exam import Exam, Grade, ExamAnalysis
from app.models.contact import ContactMessage, FAQ
from app.models.announcement import Announcement
from app.models.ai_insight import AIInsight, InsightType

__all__ = [
    "User",
    "UserRole",
    "Course",
    "ClassGroup",
    "Enrollment",
    "Attendance",
    "AttendanceStatus",
    "Assignment",
    "AssignmentSubmission",
    "Exam",
    "Grade",
    "ExamAnalysis",
    "ContactMessage",
    "FAQ",
    "Announcement",
    "AIInsight",
    "InsightType",
]
