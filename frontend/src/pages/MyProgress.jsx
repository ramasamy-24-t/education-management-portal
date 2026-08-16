import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

export default function MyProgress() {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  async function load() {
    setData(await api("/users/me/progress-overview", { token }));
  }

  useEffect(() => {
    load().catch((err) => setError(err.message));
  }, [token]);

  async function refresh() {
    setPending(true);
    setError("");
    try {
      await api("/ai/refresh", { method: "POST", token });
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">User Area</p>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-3xl font-bold">My Progress</h1>
        <button
          type="button"
          onClick={refresh}
          disabled={pending}
          className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white disabled:opacity-60"
        >
          {pending ? "Refreshing…" : "Refresh AI insights"}
        </button>
      </div>
      <p className="text-slate-600">
        Performance numbers come from your attendance, assignments, and exams. Insights are stored in the AI Engine
        and reused so pages stay up if Azure is unavailable.
      </p>

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

          <ListCard title="Weak subjects" items={data.weak_subjects} empty="No weak subjects stored yet." />
          <ListCard title="Improvement tips" items={data.improvement_tips} empty="No study recommendations stored yet." />
          <ListCard title="AI insights" items={data.ai_insights} empty="No performance or at-risk insights stored yet." />
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

function ListCard({ title, items, empty }) {
  return (
    <div className="rounded-xl border border-violet-200 bg-violet-50 p-5">
      <h2 className="text-lg font-semibold text-violet-950">{title}</h2>
      {items?.length ? (
        <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-violet-900">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="mt-2 text-sm text-violet-900">{empty}</p>
      )}
    </div>
  );
}
