from app.models.user import User, UserRole
from app.models.school import School
from app.models.course import Course, ClassGroup
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance, AttendanceStatus
from app.models.assignment import Assignment, AssignmentSubmission
from app.models.exam import Exam, Grade, ExamAnalysis, ExamAttempt
from app.models.contact import ContactMessage, FAQ
from app.models.announcement import Announcement
from app.models.ai_insight import AIInsight, InsightType
from app.models.practice import PracticeQuestionSet
from app.models.assistant import AssistantMessage, AssistantRateHit
from app.models.study_tip import StudyTip

__all__ = [
    "User",
    "UserRole",
    "School",
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
    "ExamAttempt",
    "ContactMessage",
    "FAQ",
    "Announcement",
    "AIInsight",
    "InsightType",
    "PracticeQuestionSet",
    "AssistantMessage",
    "AssistantRateHit",
    "StudyTip",
]
