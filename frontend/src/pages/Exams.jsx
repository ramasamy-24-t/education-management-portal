import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import ClassSelect from "../components/ClassSelect.jsx";
import { useAuth } from "../hooks/useAuth.js";

const emptyExam = { title: "", date: "", max_marks: 100 };

export default function Exams({ embedded = false }) {
  const { user, token } = useAuth();
  const canManage = user.role === "teacher" || user.role === "admin";
  const [classes, setClasses] = useState([]);
  const [classId, setClassId] = useState("");
  const [exams, setExams] = useState([]);
  const [history, setHistory] = useState([]);
  const [form, setForm] = useState(emptyExam);
  const [activeId, setActiveId] = useState(null);
  const [roster, setRoster] = useState([]);
  const [marks, setMarks] = useState({});
  const [grades, setGrades] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    api("/academic/classes", { token })
      .then((rows) => {
        setClasses(rows);
        if (rows[0]) setClassId(String(rows[0].id));
      })
      .catch((err) => setError(err.message));
    if (user.role === "student") {
      api("/grades/me", { token }).then(setHistory).catch((err) => setError(err.message));
    }
  }, [token, user.role]);

  async function loadExams(nextClassId = classId) {
    if (!nextClassId) return;
    setExams(await api(`/exams?class_id=${nextClassId}`, { token }));
  }

  useEffect(() => {
    loadExams(classId).catch((err) => setError(err.message));
    setActiveId(null);
    setGrades([]);
  }, [classId, token]);

  async function createExam(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api("/exams", {
        method: "POST",
        token,
        body: {
          class_id: Number(classId),
          title: form.title,
          date: form.date,
          max_marks: Number(form.max_marks),
        },
      });
      setForm(emptyExam);
      setMessage("Exam created. Record marks for each student — this is not a live exam-taking UI.");
      await loadExams();
    } catch (err) {
      setError(err.message);
    }
  }

  async function openExam(examId) {
    setActiveId(examId);
    setError("");
    try {
      const nextGrades = await api(`/exams/${examId}/grades`, { token });
      setGrades(nextGrades);
      if (canManage) {
        const students = await api(`/academic/classes/${classId}/students`, { token });
        setRoster(students);
        const nextMarks = {};
        students.forEach((student) => {
          const existing = nextGrades.find((row) => row.student_id === student.id);
          nextMarks[student.id] = existing ? String(existing.marks_obtained) : "";
        });
        setMarks(nextMarks);
      }
    } catch (err) {
      setError(err.message);
    }
  }

  async function saveMarks(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      const records = roster
        .filter((student) => marks[student.id] !== "" && marks[student.id] != null)
        .map((student) => ({ student_id: student.id, marks_obtained: Number(marks[student.id]) }));
      await api(`/exams/${activeId}/grades`, { method: "PUT", token, body: { records } });
      setMessage("Marks recorded. Exam analysis will be generated in Prompt 6.");
      setGrades(await api(`/exams/${activeId}/grades`, { token }));
      if (user.role === "student") {
        setHistory(await api("/grades/me", { token }));
      }
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="space-y-6">
      {embedded ? null : <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Academic Flow</p>}
      <h1 className={embedded ? "text-xl font-bold" : "text-3xl font-bold"}>Exams & Grades</h1>
      <p className="text-slate-600">
        {canManage
          ? "Create an exam, then record marks per student. “Take Exams” means entering results, not a live quiz."
          : "View your grades and full exam history."}
      </p>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {message ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{message}</p> : null}

      <ClassSelect classes={classes} value={classId} onChange={setClassId} />

      {canManage ? (
        <form onSubmit={createExam} className="grid gap-3 rounded-xl border border-slate-200 bg-white p-5 md:grid-cols-3">
          <h2 className="md:col-span-3 font-semibold">Create exam</h2>
          <input
            required
            placeholder="Title"
            value={form.title}
            onChange={(event) => setForm((prev) => ({ ...prev, title: event.target.value }))}
            className="rounded-md border border-slate-300 px-3 py-2"
          />
          <input
            required
            type="date"
            value={form.date}
            onChange={(event) => setForm((prev) => ({ ...prev, date: event.target.value }))}
            className="rounded-md border border-slate-300 px-3 py-2"
          />
          <input
            required
            type="number"
            min="1"
            value={form.max_marks}
            onChange={(event) => setForm((prev) => ({ ...prev, max_marks: event.target.value }))}
            className="rounded-md border border-slate-300 px-3 py-2"
          />
          <button type="submit" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white">
            Create exam
          </button>
        </form>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-3">
          <h2 className="font-semibold">Exams</h2>
          {exams.map((exam) => (
            <button
              key={exam.id}
              type="button"
              onClick={() => openExam(exam.id)}
              className={`w-full rounded-xl border p-4 text-left ${
                activeId === exam.id ? "border-slate-900 bg-slate-50" : "border-slate-200 bg-white"
              }`}
            >
              <p className="font-medium">{exam.title}</p>
              <p className="text-sm text-slate-600">
                {exam.date} · max {exam.max_marks}
              </p>
            </button>
          ))}
        </div>

        <div className="space-y-3">
          <h2 className="font-semibold">View grades</h2>
          {canManage && activeId ? (
            <form onSubmit={saveMarks} className="space-y-2 rounded-xl border border-slate-200 bg-white p-4">
              {roster.map((student) => (
                <label key={student.id} className="flex items-center justify-between gap-3 text-sm">
                  <span>{student.name}</span>
                  <input
                    type="number"
                    min="0"
                    value={marks[student.id] ?? ""}
                    onChange={(event) => setMarks((prev) => ({ ...prev, [student.id]: event.target.value }))}
                    className="w-24 rounded-md border border-slate-300 px-2 py-1"
                  />
                </label>
              ))}
              <button type="submit" className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white">
                Record marks
              </button>
            </form>
          ) : null}

          {grades.length === 0 ? (
            <p className="text-sm text-slate-600">No grades for this exam yet.</p>
          ) : (
            <ul className="space-y-2 text-sm">
              {grades.map((row) => (
                <li key={row.id} className="rounded-md border border-slate-200 bg-white px-3 py-2">
                  {row.student_name}: {row.marks_obtained}/{row.max_marks} ({row.percent}%)
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {user.role === "student" ? (
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="font-semibold">Grade history</h2>
          {history.length === 0 ? (
            <p className="mt-2 text-sm text-slate-600">No exam grades yet.</p>
          ) : (
            <table className="mt-3 w-full text-left text-sm">
              <thead>
                <tr className="text-slate-500">
                  <th className="py-1">Exam</th>
                  <th>Course</th>
                  <th>Date</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {history.map((row) => (
                  <tr key={row.id} className="border-t border-slate-100">
                    <td className="py-2">{row.exam_title}</td>
                    <td>{row.course_title}</td>
                    <td>{row.date}</td>
                    <td>
                      {row.marks_obtained}/{row.max_marks} ({row.percent}%)
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      ) : null}
    </section>
  );
}
