import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import ClassSelect from "../components/ClassSelect.jsx";
import { useAuth } from "../hooks/useAuth.js";

const emptyAssignment = { title: "", description: "", due_date: "" };

export default function Assignments({ embedded = false }) {
  const { user, token } = useAuth();
  const canCreate = user.role === "teacher" || user.role === "admin";
  const [classes, setClasses] = useState([]);
  const [classId, setClassId] = useState("");
  const [assignments, setAssignments] = useState([]);
  const [form, setForm] = useState(emptyAssignment);
  const [activeId, setActiveId] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [content, setContent] = useState("");
  const [gradeForm, setGradeForm] = useState({});
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    api("/academic/classes", { token })
      .then((rows) => {
        setClasses(rows);
        if (rows[0]) setClassId(String(rows[0].id));
      })
      .catch((err) => setError(err.message));
  }, [token]);

  async function loadAssignments(nextClassId = classId) {
    if (!nextClassId) return;
    setAssignments(await api(`/assignments?class_id=${nextClassId}`, { token }));
  }

  useEffect(() => {
    loadAssignments(classId).catch((err) => setError(err.message));
    setActiveId(null);
    setSubmissions([]);
  }, [classId, token]);

  async function createAssignment(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api("/assignments", {
        method: "POST",
        token,
        body: {
          class_id: Number(classId),
          title: form.title,
          description: form.description,
          due_date: new Date(form.due_date).toISOString(),
        },
      });
      setForm(emptyAssignment);
      setMessage("Assignment created.");
      await loadAssignments();
    } catch (err) {
      setError(err.message);
    }
  }

  async function openAssignment(assignmentId) {
    setActiveId(assignmentId);
    setError("");
    try {
      setSubmissions(await api(`/assignments/${assignmentId}/submissions`, { token }));
    } catch (err) {
      setError(err.message);
    }
  }

  async function submitWork(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api(`/assignments/${activeId}/submissions`, {
        method: "POST",
        token,
        body: { content },
      });
      setContent("");
      setMessage("Submission saved.");
      setSubmissions(await api(`/assignments/${activeId}/submissions`, { token }));
    } catch (err) {
      setError(err.message);
    }
  }

  async function gradeSubmission(submissionId) {
    const payload = gradeForm[submissionId];
    setError("");
    setMessage("");
    try {
      await api(`/submissions/${submissionId}`, {
        method: "PATCH",
        token,
        body: { grade: Number(payload?.grade), feedback: payload?.feedback || "" },
      });
      setMessage("Grade saved. AI feedback is generated beside your comments.");
      setSubmissions(await api(`/assignments/${activeId}/submissions`, { token }));
    } catch (err) {
      setError(err.message);
    }
  }

  const active = assignments.find((item) => item.id === activeId);

  return (
    <section className="space-y-6">
      {embedded ? null : <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Academic Flow</p>}
      <h1 className={embedded ? "text-xl font-bold" : "text-3xl font-bold"}>Assignments</h1>
      <p className="text-slate-600">
        {canCreate
          ? "Create assignments with due dates and grade student submissions. Saving a grade also writes AI feedback for the student."
          : "View due dates and submit your work. You cannot grade your own assignment."}
      </p>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {message ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{message}</p> : null}

      <ClassSelect classes={classes} value={classId} onChange={setClassId} />

      {canCreate ? (
        <form onSubmit={createAssignment} className="grid gap-3 rounded-xl border border-slate-200 bg-white p-5 md:grid-cols-2">
          <h2 className="md:col-span-2 font-semibold">Create assignment</h2>
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Title</span>
            <input
              required
              value={form.title}
              onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Due date</span>
            <input
              required
              type="datetime-local"
              value={form.due_date}
              onChange={(event) => setForm((prev) => ({ ...prev, due_date: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
          <label className="md:col-span-2 block text-sm">
            <span className="mb-1 block font-medium">Description</span>
            <textarea
              required
              rows={3}
              value={form.description}
              onChange={(event) => setForm((prev) => ({ ...prev, description: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
          <button type="submit" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white">
            Create
          </button>
        </form>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-3">
          <h2 className="font-semibold">Assignments</h2>
          {assignments.map((item) => (
            <button
              key={item.id}
              type="button"
              onClick={() => openAssignment(item.id)}
              className={`w-full rounded-xl border p-4 text-left ${
                activeId === item.id ? "border-slate-900 bg-slate-50" : "border-slate-200 bg-white"
              }`}
            >
              <p className="font-medium">{item.title}</p>
              <p className="text-sm text-slate-600">Due {new Date(item.due_date).toLocaleString()}</p>
            </button>
          ))}
        </div>

        <div className="space-y-3">
          <h2 className="font-semibold">{active ? active.title : "Select an assignment"}</h2>
          {active ? <p className="text-sm text-slate-700">{active.description}</p> : null}

          {user.role === "student" && active ? (
            <form onSubmit={submitWork} className="space-y-2 rounded-xl border border-slate-200 bg-white p-4">
              <textarea
                required
                rows={4}
                value={content}
                onChange={(event) => setContent(event.target.value)}
                placeholder="Write your submission"
                className="w-full rounded-md border border-slate-300 px-3 py-2"
              />
              <button type="submit" className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white">
                Submit assignment
              </button>
            </form>
          ) : null}

          {submissions.map((row) => (
            <article key={row.id} className="rounded-xl border border-slate-200 bg-white p-4 text-sm">
              <p className="font-medium">{row.student_name}</p>
              <p className="mt-1 text-slate-700">{row.content}</p>
              <p className="mt-2 text-slate-600">
                Grade: {row.grade ?? "—"} · Feedback: {row.feedback || "—"}
              </p>
              <p className="text-violet-900">AI feedback: {row.ai_feedback || "Unavailable — teacher feedback still stands."}</p>
              {canCreate ? (
                <div className="mt-3 grid gap-2 md:grid-cols-2">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    placeholder="Grade"
                    value={gradeForm[row.id]?.grade ?? ""}
                    onChange={(event) =>
                      setGradeForm((prev) => ({ ...prev, [row.id]: { ...prev[row.id], grade: event.target.value } }))
                    }
                    className="rounded-md border border-slate-300 px-3 py-2"
                  />
                  <input
                    placeholder="Manual feedback"
                    value={gradeForm[row.id]?.feedback ?? ""}
                    onChange={(event) =>
                      setGradeForm((prev) => ({ ...prev, [row.id]: { ...prev[row.id], feedback: event.target.value } }))
                    }
                    className="rounded-md border border-slate-300 px-3 py-2"
                  />
                  <button
                    type="button"
                    onClick={() => gradeSubmission(row.id)}
                    className="rounded-md bg-slate-900 px-3 py-2 text-white"
                  >
                    Save grade
                  </button>
                </div>
              ) : null}
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
