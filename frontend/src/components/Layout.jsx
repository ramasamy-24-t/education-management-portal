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
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-slate-900 focus:px-3 focus:py-2 focus:text-sm focus:text-white"
      >
        Skip to main content
      </a>
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <NavLink to="/" className="text-lg font-semibold text-slate-900">
            Education Management Portal
          </NavLink>
          <nav className="flex flex-wrap items-center gap-1" aria-label="Main">
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
      <main id="main-content" tabIndex={-1} className="mx-auto max-w-6xl px-4 py-8 outline-none">
        <Outlet />
      </main>
      <AssistantChat />
    </div>
  );
}
