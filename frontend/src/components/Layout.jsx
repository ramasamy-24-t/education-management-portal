import { NavLink, Outlet } from "react-router-dom";

const linkClass = ({ isActive }) =>
  `rounded-md px-3 py-1.5 text-sm font-medium ${
    isActive ? "bg-slate-900 text-white" : "text-slate-700 hover:bg-slate-200"
  }`;

export default function Layout() {
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <NavLink to="/" className="text-lg font-semibold text-slate-900">
            Education Management Portal
          </NavLink>
          <nav className="flex flex-wrap gap-1">
            <NavLink to="/" className={linkClass} end>
              Home
            </NavLink>
            <NavLink to="/courses" className={linkClass}>
              Courses
            </NavLink>
            <NavLink to="/contact" className={linkClass}>
              Contact
            </NavLink>
            <NavLink to="/login" className={linkClass}>
              Login / Register
            </NavLink>
            <NavLink to="/dashboard" className={linkClass}>
              User Dashboard
            </NavLink>
            <NavLink to="/progress" className={linkClass}>
              My Progress
            </NavLink>
            <NavLink to="/admin/login" className={linkClass}>
              Admin Login
            </NavLink>
            <NavLink to="/admin" className={linkClass}>
              Admin Dashboard
            </NavLink>
            <NavLink to="/reports" className={linkClass}>
              Reports
            </NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
