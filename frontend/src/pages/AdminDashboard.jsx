import { Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

const later = [
  "Manage Students",
  "Manage Teachers",
  "View Reports & Analytics",
  "AI Insights & Monitoring",
];

export default function AdminDashboard() {
  const { user } = useAuth();

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Admin Area</p>
      <h1 className="text-3xl font-bold">Admin Dashboard</h1>
      <p className="text-slate-600">Signed in as {user.name} ({user.email}).</p>

      <div className="grid gap-3 md:grid-cols-2">
        <Link
          to="/manage/courses"
          className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:border-slate-300"
        >
          <h2 className="text-lg font-semibold">Manage courses & classes</h2>
          <p className="mt-1 text-sm text-slate-600">Create, edit, and delete courses and class sections.</p>
        </Link>
        <Link to="/assignments" className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:border-slate-300">
          <h2 className="text-lg font-semibold">Manage assignments</h2>
          <p className="mt-1 text-sm text-slate-600">Create assignments and grade submissions for any class.</p>
        </Link>
        <Link to="/exams" className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:border-slate-300">
          <h2 className="text-lg font-semibold">Manage exams & grades</h2>
          <p className="mt-1 text-sm text-slate-600">Create exams and record marks per student.</p>
        </Link>
        <Link to="/attendance" className="block rounded-xl border border-slate-200 bg-white p-5 shadow-sm hover:border-slate-300">
          <h2 className="text-lg font-semibold">Attendance</h2>
          <p className="mt-1 text-sm text-slate-600">Mark and review attendance for any class.</p>
        </Link>
      </div>

      <div className="rounded-xl border border-dashed border-slate-300 p-5">
        <h2 className="font-semibold">Coming in later prompts</h2>
        <ul className="mt-2 list-disc pl-5 text-sm text-slate-600">
          {later.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </section>
  );
}
