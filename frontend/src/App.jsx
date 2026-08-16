import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout.jsx";
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
        <Route path="/dashboard" element={<UserDashboard />} />
        <Route path="/progress" element={<MyProgress />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/reports" element={<PerformanceReports />} />
      </Route>
    </Routes>
  );
}
