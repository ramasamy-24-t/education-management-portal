import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import CourseCard from "../components/CourseCard.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function StudentDashboard() {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [drafts, setDrafts] = useState({});
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function load() {
    setData(await api("/users/me/dashboard", { token }));
  }

  useEffect(() => {
    load().catch((err) => setError(err.message));
  }, [token]);

  async function submit(assignmentId) {
    setError("");
    setMessage("");
    try {
      await api(`/assignments/${assignmentId}/submissions`, {
        method: "POST",
        token,
        body: { content: drafts[assignmentId] || "" },
      });
      setDrafts((prev) => ({ ...prev, [assignmentId]: "" }));
      setMessage("Submission saved.");
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  if (!data) {
    return error ? <p className="text-red-700">{error}</p> : <p className="text-slate-600">Loading dashboard…</p>;
  }

  const overview = data.progress_overview;

  return (
    <div className="space-y-6">
      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {message ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{message}</p> : null}

      <section className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="text-lg font-semibold">Profile</h2>
        <p className="mt-2">{data.profile.name}</p>
        <p className="text-sm text-slate-600">{data.profile.email}</p>
        <p className="text-sm capitalize text-slate-600">Role: {data.profile.role}</p>
      </section>

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">My courses</h2>
          <Link to="/courses" className="text-sm underline">
            Explore courses
          </Link>
        </div>
        {data.courses.length === 0 ? (
          <p className="text-slate-600">You are not enrolled in any courses.</p>
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {data.courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-lg font-semibold">My assignments</h2>
        {data.assignments.length === 0 ? (
          <p className="text-slate-600">No assignments yet.</p>
        ) : (
          data.assignments.map((item) => (
            <article key={item.id} className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="font-medium">{item.title}</p>
              <p className="text-sm text-slate-600">
                {item.course_title} · due {new Date(item.due_date).toLocaleString()}
              </p>
              <p className="mt-2 text-sm text-slate-700">{item.description}</p>
              {item.my_submission ? (
                <div className="mt-2 space-y-1 text-sm">
                  <p className="text-emerald-800">
                    Submitted · teacher grade {item.my_submission.grade ?? "pending"} ·{" "}
                    {item.my_submission.feedback || "no teacher feedback yet"}
                  </p>
                  <p className="text-violet-900">
                    AI feedback: {item.my_submission.ai_feedback || "Will appear after your teacher grades this."}
                  </p>
                </div>
              ) : null}
              <textarea
                rows={3}
                value={drafts[item.id] ?? ""}
                onChange={(event) => setDrafts((prev) => ({ ...prev, [item.id]: event.target.value }))}
                placeholder="Write your submission"
                className="mt-3 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
              />
              <button
                type="button"
                onClick={() => submit(item.id)}
                className="mt-2 rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white"
              >
                {item.my_submission ? "Update submission" : "Submit assignment"}
              </button>
            </article>
          ))
        )}
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="text-lg font-semibold">Attendance</h2>
        {data.attendance.length === 0 ? (
          <p className="mt-2 text-sm text-slate-600">No attendance recorded yet.</p>
        ) : (
          <ul className="mt-3 space-y-2 text-sm">
            {data.attendance.map((row) => (
              <li key={row.class_id} className="flex justify-between">
                <span>{row.class_name}</span>
                <span>{row.percent_present}% present</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="text-lg font-semibold">Grades</h2>
        {data.grades.length === 0 ? (
          <p className="mt-2 text-sm text-slate-600">No exam grades yet.</p>
        ) : (
          <ul className="mt-3 space-y-2 text-sm">
            {data.grades.map((row) => (
              <li key={row.id} className="border-b border-slate-100 py-2 last:border-0">
                <div className="flex justify-between">
                  <span>{row.exam_title}</span>
                  <span>
                    {row.marks_obtained}/{row.max_marks} ({row.percent}%)
                  </span>
                </div>
                {row.ai_summary ? <p className="mt-1 text-violet-900">{row.ai_summary}</p> : null}
                {row.weak_topics ? <p className="text-slate-600">Weak topics: {row.weak_topics}</p> : null}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="rounded-xl border border-violet-200 bg-violet-50 p-5">
        <h2 className="text-lg font-semibold text-violet-950">AI recommendations</h2>
        {data.ai_recommendations?.length ? (
          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-violet-900">
            {data.ai_recommendations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-sm text-violet-900">No stored recommendations yet. Open My Progress to generate them.</p>
        )}
      </section>

      <section className="rounded-xl border border-slate-200 bg-white p-5">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Progress overview</h2>
          <Link to="/progress" className="text-sm underline">
            Open My Progress
          </Link>
        </div>
        <dl className="mt-3 grid gap-3 sm:grid-cols-3 text-sm">
          <Stat label="Attendance" value={`${overview.attendance_percent}%`} />
          <Stat label="Exam average" value={`${overview.average_exam_percent}%`} />
          <Stat
            label="Assignments"
            value={`${overview.assignments_submitted}/${overview.assignments_total} (${overview.assignment_completion_percent}%)`}
          />
        </dl>
      </section>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="rounded-md bg-slate-50 px-3 py-2">
      <dt className="text-slate-500">{label}</dt>
      <dd className="font-medium">{value}</dd>
    </div>
  );
}
