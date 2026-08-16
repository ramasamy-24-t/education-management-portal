import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import RiskTrend from "../components/RiskTrend.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function MyProgress() {
  const { token, user } = useAuth();
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

          <div className="rounded-xl border border-amber-200 bg-amber-50 p-5">
            <h2 className="text-lg font-semibold text-amber-950">At-risk trend</h2>
            <p className="mt-1 text-sm text-amber-900">
              Compares the last 3 days with the 3 days before that. Shown next to the at-risk insight — never guessed
              when a window is empty.
            </p>
            <RiskTrend trend={data.risk_trend} reason={data.risk_trend_reason} />
          </div>

          <WeakSubjectsCard
            items={data.weak_subjects}
            studentId={user.id}
            token={token}
          />
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

function WeakSubjectsCard({ items, studentId, token }) {
  const [bySubject, setBySubject] = useState({});

  async function generate(subject) {
    setBySubject((prev) => ({
      ...prev,
      [subject]: { ...(prev[subject] || {}), status: "loading", error: "" },
    }));
    try {
      const payload = await api(`/ai/practice-questions/${studentId}`, {
        method: "POST",
        token,
        body: { subject },
      });
      const questions = payload.questions || [];
      const failed = payload.source === "error" || questions.length === 0;
      setBySubject((prev) => ({
        ...prev,
        [subject]: {
          status: failed ? "error" : "ok",
          questions,
          source: payload.source,
          error: failed ? payload.detail || "Could not generate questions." : "",
        },
      }));
    } catch (err) {
      setBySubject((prev) => ({
        ...prev,
        [subject]: {
          status: "error",
          questions: prev[subject]?.questions || [],
          source: "error",
          error: err.message || "Could not generate questions.",
        },
      }));
    }
  }

  return (
    <div className="rounded-xl border border-violet-200 bg-violet-50 p-5">
      <h2 className="text-lg font-semibold text-violet-950">Weak subjects</h2>
      {items?.length ? (
        <ul className="mt-3 space-y-3">
          {items.map((subject) => {
            const state = bySubject[subject] || { status: "idle", questions: [] };
            const label =
              state.status === "loading"
                ? "Generating…"
                : state.questions?.length
                  ? "Regenerate"
                  : "Generate practice questions";
            return (
              <li key={subject} className="rounded-lg border border-violet-200 bg-white p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="font-medium text-violet-950">{subject}</p>
                  <button
                    type="button"
                    onClick={() => generate(subject)}
                    disabled={state.status === "loading"}
                    className="rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white disabled:opacity-60"
                  >
                    {label}
                  </button>
                </div>
                {state.status === "loading" ? (
                  <p className="mt-2 text-sm text-slate-600">Generating practice questions…</p>
                ) : null}
                {state.status === "error" ? (
                  <div className="mt-2 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">
                    <p>{state.error}</p>
                    <button
                      type="button"
                      onClick={() => generate(subject)}
                      className="mt-2 rounded-md border border-red-300 px-2 py-1 text-xs font-medium"
                    >
                      Retry
                    </button>
                  </div>
                ) : null}
                {state.questions?.length && state.status !== "loading" ? (
                  <div className="mt-2">
                    {state.source === "fallback" ? (
                      <p className="mb-1 text-xs text-amber-800">
                        Local prompts (AI unavailable). Retry for model-generated questions.
                      </p>
                    ) : null}
                    <ol className="list-decimal space-y-1 pl-5 text-sm text-slate-800">
                      {state.questions.map((question) => (
                        <li key={question}>{question}</li>
                      ))}
                    </ol>
                  </div>
                ) : null}
              </li>
            );
          })}
        </ul>
      ) : (
        <p className="mt-2 text-sm text-violet-900">No weak subjects stored yet.</p>
      )}
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
