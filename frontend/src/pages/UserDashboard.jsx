import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import CourseCard from "../components/CourseCard.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function UserDashboard() {
  const { user, token } = useAuth();
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      if (user.role === "teacher") {
        setCourses(await api(`/courses?teacher_id=${user.id}`, { token }));
        return;
      }
      const enrollments = await api("/enrollments/me", { token });
      const details = await Promise.all(enrollments.map((row) => api(`/courses/${row.course_id}`, { token })));
      setCourses(details);
    }
    load().catch((err) => setError(err.message));
  }, [user, token]);

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">User Area</p>
      <h1 className="text-3xl font-bold">User Dashboard</h1>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="text-lg font-semibold">Profile</h2>
        <p className="mt-2 text-slate-700">{user.name}</p>
        <p className="text-sm text-slate-600">{user.email}</p>
        <p className="mt-1 text-sm capitalize text-slate-600">Role: {user.role}</p>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">My courses</h2>
          {user.role === "teacher" ? (
            <Link to="/manage/courses" className="text-sm font-medium underline">
              Manage courses
            </Link>
          ) : (
            <Link to="/courses" className="text-sm font-medium underline">
              Explore courses
            </Link>
          )}
        </div>
        {courses.length === 0 ? (
          <p className="text-slate-600">No courses yet.</p>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        )}
      </div>

      <div className="grid gap-3 sm:grid-cols-3">
        <Link to="/attendance" className="rounded-xl border border-slate-200 bg-white p-4 hover:border-slate-300">
          <h3 className="font-semibold">Attendance</h3>
          <p className="mt-1 text-sm text-slate-600">View or mark attendance and see percent present.</p>
        </Link>
        <Link to="/assignments" className="rounded-xl border border-slate-200 bg-white p-4 hover:border-slate-300">
          <h3 className="font-semibold">My assignments</h3>
          <p className="mt-1 text-sm text-slate-600">Due dates, submissions, and teacher feedback.</p>
        </Link>
        <Link to="/exams" className="rounded-xl border border-slate-200 bg-white p-4 hover:border-slate-300">
          <h3 className="font-semibold">Grades</h3>
          <p className="mt-1 text-sm text-slate-600">Exam marks and grade history.</p>
        </Link>
      </div>
      <div className="rounded-xl border border-dashed border-slate-300 p-5 text-sm text-slate-600">
        Coming in later prompts: AI Recommendations, Progress Overview.
      </div>
    </section>
  );
}
