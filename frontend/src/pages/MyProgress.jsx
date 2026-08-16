import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

export default function MyProgress() {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/users/me/progress-overview", { token })
      .then(setData)
      .catch((err) => setError(err.message));
  }, [token]);

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">User Area</p>
      <h1 className="text-3xl font-bold">My Progress</h1>
      <p className="text-slate-600">Student-only view of performance. AI sections are placeholders until Prompt 6.</p>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {!data && !error ? <p className="text-slate-600">Loading progress…</p> : null}

      {data ? (
        <>
          <div className="rounded-xl border border-slate-200 bg-white p-5">
            <h2 className="text-lg font-semibold">Performance overview</h2>
            <dl className="mt-3 grid gap-3 sm:grid-cols-2 text-sm">
              <Item label="Courses" value={data.course_count} />
              <Item label="Attendance" value={`${data.attendance_percent}%`} />
              <Item label="Exam average" value={`${data.average_exam_percent}%`} />
              <Item
                label="Assignments completed"
                value={`${data.assignments_submitted}/${data.assignments_total} (${data.assignment_completion_percent}%)`}
              />
              <Item
                label="Assignment grade average"
                value={data.average_assignment_grade == null ? "—" : data.average_assignment_grade}
              />
            </dl>
          </div>

          <Placeholder title="Weak subjects" body="The AI Engine will identify weak subjects here in Prompt 6." />
          <Placeholder title="Improvement tips" body="Study recommendations will appear here in Prompt 6." />
          <Placeholder title="AI insights" body="Stored AI insights and reports will appear here in Prompt 6." />
        </>
      ) : null}
    </section>
  );
}

function Item({ label, value }) {
  return (
    <div className="rounded-md bg-slate-50 px-3 py-2">
      <dt className="text-slate-500">{label}</dt>
      <dd className="font-medium">{value}</dd>
    </div>
  );
}

function Placeholder({ title, body }) {
  return (
    <div className="rounded-xl border border-dashed border-violet-200 bg-violet-50 p-5">
      <h2 className="text-lg font-semibold text-violet-950">{title}</h2>
      <p className="mt-2 text-sm text-violet-900">{body}</p>
    </div>
  );
}
