import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import CourseCard from "../components/CourseCard.jsx";
import { useAuth } from "../hooks/useAuth.js";
import Assignments from "../pages/Assignments.jsx";
import Attendance from "../pages/Attendance.jsx";
import Exams from "../pages/Exams.jsx";

const tabs = [
  { id: "classes", label: "My classes" },
  { id: "attendance", label: "Mark attendance" },
  { id: "assignments", label: "Assignments" },
  { id: "exams", label: "Exams & marks" },
];

export default function TeacherDashboard() {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [tab, setTab] = useState("classes");
  const [error, setError] = useState("");

  useEffect(() => {
    api("/users/me/dashboard", { token })
      .then(setData)
      .catch((err) => setError(err.message));
  }, [token]);

  if (!data) {
    return error ? <p className="text-red-700">{error}</p> : <p className="text-slate-600">Loading dashboard…</p>;
  }

  return (
    <div className="space-y-6">
      <section className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="text-lg font-semibold">Profile</h2>
        <p className="mt-2">{data.profile.name}</p>
        <p className="text-sm text-slate-600">{data.profile.email}</p>
        <p className="text-sm capitalize text-slate-600">Role: {data.profile.role}</p>
      </section>

      <div className="flex flex-wrap gap-2">
        {tabs.map((item) => (
          <button
            key={item.id}
            type="button"
            onClick={() => setTab(item.id)}
            className={`rounded-md px-3 py-1.5 text-sm font-medium ${
              tab === item.id ? "bg-slate-900 text-white" : "bg-slate-200 text-slate-700"
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {tab === "classes" ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">My classes</h2>
            <Link to="/manage/courses" className="text-sm underline">
              Manage courses
            </Link>
          </div>
          <ul className="space-y-2">
            {data.classes.map((item) => (
              <li key={item.id} className="rounded-xl border border-slate-200 bg-white px-4 py-3">
                <p className="font-medium">{item.course_title}</p>
                <p className="text-sm text-slate-600">{item.name}</p>
              </li>
            ))}
          </ul>
          <h3 className="font-semibold">Courses I teach</h3>
          <div className="grid gap-3 sm:grid-cols-2">
            {data.courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        </div>
      ) : null}

      {tab === "attendance" ? <Attendance embedded /> : null}
      {tab === "assignments" ? <Assignments embedded /> : null}
      {tab === "exams" ? <Exams embedded /> : null}
    </div>
  );
}
