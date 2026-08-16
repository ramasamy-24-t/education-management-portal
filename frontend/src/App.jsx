import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";
import Home from "./pages/Home.jsx";
import Courses from "./pages/Courses.jsx";
import CourseDetails from "./pages/CourseDetails.jsx";
import Contact from "./pages/Contact.jsx";
import LoginRegister from "./pages/LoginRegister.jsx";
import UserDashboard from "./pages/UserDashboard.jsx";
import MyProgress from "./pages/MyProgress.jsx";
import AdminLogin from "./pages/AdminLogin.jsx";
import AdminDashboard from "./pages/AdminDashboard.jsx";
import PerformanceReports from "./pages/PerformanceReports.jsx";
import ManageCourses from "./pages/ManageCourses.jsx";
import Attendance from "./pages/Attendance.jsx";
import Assignments from "./pages/Assignments.jsx";
import Exams from "./pages/Exams.jsx";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/courses/:courseId" element={<CourseDetails />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login" element={<LoginRegister />} />
        <Route path="/register" element={<Navigate to="/login" replace />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute roles={["student", "teacher"]}>
              <UserDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/progress"
          element={
            <ProtectedRoute roles={["student", "teacher"]}>
              <MyProgress />
            </ProtectedRoute>
          }
        />
        <Route
          path="/manage/courses"
          element={
            <ProtectedRoute roles={["teacher", "admin"]}>
              <ManageCourses />
            </ProtectedRoute>
          }
        />
        <Route
          path="/attendance"
          element={
            <ProtectedRoute roles={["student", "teacher", "admin"]}>
              <Attendance />
            </ProtectedRoute>
          }
        />
        <Route
          path="/assignments"
          element={
            <ProtectedRoute roles={["student", "teacher", "admin"]}>
              <Assignments />
            </ProtectedRoute>
          }
        />
        <Route
          path="/exams"
          element={
            <ProtectedRoute roles={["student", "teacher", "admin"]}>
              <Exams />
            </ProtectedRoute>
          }
        />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route
          path="/admin"
          element={
            <ProtectedRoute roles={["admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute roles={["student", "teacher", "admin"]}>
              <PerformanceReports />
            </ProtectedRoute>
          }
        />
      </Route>
    </Routes>
  );
}
