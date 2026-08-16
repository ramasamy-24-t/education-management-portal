import { Link } from "react-router-dom";
import AdminContactPanel from "../dashboards/AdminContactPanel.jsx";
import AdminInsightsPanel from "../dashboards/AdminInsightsPanel.jsx";
import AdminPeoplePanel from "../dashboards/AdminPeoplePanel.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function AdminDashboard() {
  const { user } = useAuth();

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Admin Area</p>
      <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      <p className="text-slate-600">
        Signed in as {user.name} ({user.email}).
      </p>

      <AdminPeoplePanel />
      <AdminContactPanel />

      <div className="grid gap-3 md:grid-cols-2">
        <AdminLink to="/manage/courses" title="Manage courses & classes" body="Create, edit, and delete courses and class sections." />
        <AdminLink to="/assignments" title="Manage assignments" body="Create assignments and grade submissions for any class." />
        <AdminLink to="/exams" title="Manage exams & grades" body="Create exams and record marks per student." />
        <AdminLink to="/attendance" title="Attendance" body="Mark and review attendance for any class." />
        <AdminLink to="/reports" title="View reports & analytics" body="Class, comparative, and AI insight summaries, plus print and PDF download." />
      </div>

      <AdminInsightsPanel />
    </section>
  );
}

function AdminLink({ to, title, body }) {
  return (
    <Link to={to} className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:border-slate-300">
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="mt-1 text-sm text-slate-600">{body}</p>
    </Link>
  );
}
