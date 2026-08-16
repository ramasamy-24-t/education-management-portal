import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";
import AssistantChat from "./AssistantChat.jsx";

const linkClass = ({ isActive }) =>
  `rounded-md px-3 py-1.5 text-sm font-medium ${
    isActive ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-200"
  }`;

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <NavLink to="/" className="text-lg font-semibold text-slate-900">
            Education Management Portal
          </NavLink>
          <nav className="flex flex-wrap items-center gap-1">
            <NavLink to="/" className={linkClass} end>
              Home
            </NavLink>
            <NavLink to="/courses" className={linkClass}>
              Courses
            </NavLink>
            <NavLink to="/contact" className={linkClass}>
              Contact
            </NavLink>
            {!user ? (
              <>
                <NavLink to="/login" className={linkClass}>
                  Login / Register
                </NavLink>
                <NavLink to="/admin/login" className={linkClass}>
                  Admin Login
                </NavLink>
              </>
            ) : null}
            {user?.role === "student" || user?.role === "teacher" ? (
              <NavLink to="/dashboard" className={linkClass}>
                Dashboard
              </NavLink>
            ) : null}
            {user?.role === "student" ? (
              <NavLink to="/progress" className={linkClass}>
                My Progress
              </NavLink>
            ) : null}
            {user ? (
              <>
                <NavLink to="/attendance" className={linkClass}>
                  Attendance
                </NavLink>
                <NavLink to="/assignments" className={linkClass}>
                  Assignments
                </NavLink>
                <NavLink to="/exams" className={linkClass}>
                  Exams
                </NavLink>
              </>
            ) : null}
            {user?.role === "teacher" || user?.role === "admin" ? (
              <NavLink to="/manage/courses" className={linkClass}>
                Manage Courses
              </NavLink>
            ) : null}
            {user?.role === "admin" ? (
              <NavLink to="/admin" className={linkClass}>
                Admin
              </NavLink>
            ) : null}
            {user ? (
              <>
                <NavLink to="/reports" className={linkClass}>
                  Reports
                </NavLink>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded-md px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-200"
                >
                  Logout
                </button>
              </>
            ) : null}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
      <AssistantChat />
    </div>
  );
}
