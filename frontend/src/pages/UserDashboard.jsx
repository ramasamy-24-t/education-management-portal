import StudentDashboard from "../dashboards/StudentDashboard.jsx";
import TeacherDashboard from "../dashboards/TeacherDashboard.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function UserDashboard() {
  const { user } = useAuth();

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">User Area</p>
      <h1 className="text-3xl font-bold">User Dashboard</h1>
      {user.role === "teacher" ? <TeacherDashboard /> : <StudentDashboard />}
    </section>
  );
}
