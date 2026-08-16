import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import ClassSelect from "../components/ClassSelect.jsx";
import { useAuth } from "../hooks/useAuth.js";

function today() {
  return new Date().toISOString().slice(0, 10);
}

export default function Attendance({ embedded = false }) {
  const { user, token } = useAuth();
  const canMark = user.role === "teacher" || user.role === "admin";
  const [classes, setClasses] = useState([]);
  const [classId, setClassId] = useState("");
  const [date, setDate] = useState(today());
  const [roster, setRoster] = useState([]);
  const [marks, setMarks] = useState({});
  const [records, setRecords] = useState([]);
  const [summary, setSummary] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);

  useEffect(() => {
    api("/academic/classes", { token })
      .then((rows) => {
        setClasses(rows);
        if (rows[0]) setClassId(String(rows[0].id));
      })
      .catch((err) => setError(err.message));
  }, [token]);

  useEffect(() => {
    if (!classId) return;
    setError("");
    const load = async () => {
      const [nextSummary, nextRecords] = await Promise.all([
        api(`/attendance/summary?class_id=${classId}`, { token }),
        api(`/attendance?class_id=${classId}${canMark ? `&on_date=${date}` : ""}`, { token }),
      ]);
      setSummary(nextSummary);
      setRecords(nextRecords);
      if (canMark) {
        const students = await api(`/academic/classes/${classId}/students`, { token });
        setRoster(students);
        const nextMarks = {};
        students.forEach((student) => {
          const existing = nextRecords.find((row) => row.student_id === student.id);
          nextMarks[student.id] = existing?.status || "present";
        });
        setMarks(nextMarks);
      }
    };
    load().catch((err) => setError(err.message));
  }, [classId, date, token, canMark]);

  async function save(event) {
    event.preventDefault();
    setPending(true);
    setError("");
    setMessage("");
    try {
      await api("/attendance/mark", {
        method: "POST",
        token,
        body: {
          class_id: Number(classId),
          date,
          records: roster.map((student) => ({
            student_id: student.id,
            status: marks[student.id] || "present",
          })),
        },
      });
      setMessage("Attendance saved.");
      setSummary(await api(`/attendance/summary?class_id=${classId}`, { token }));
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="space-y-6">
      {embedded ? null : <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Academic Flow</p>}
      <h1 className={embedded ? "text-xl font-bold" : "text-3xl font-bold"}>Attendance</h1>
      <p className="text-slate-600">
        {canMark
          ? "Mark attendance per class and date. Late counts toward percent present."
          : "View your own attendance and percent present for each class."}
      </p>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {message ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{message}</p> : null}

      <div className="grid gap-3 md:grid-cols-2">
        <ClassSelect classes={classes} value={classId} onChange={setClassId} />
        {canMark ? (
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-slate-700">Date</span>
            <input
              type="date"
              value={date}
              onChange={(event) => setDate(event.target.value)}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
        ) : null}
      </div>

      {canMark && roster.length > 0 ? (
        <form onSubmit={save} className="space-y-3 rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="font-semibold">Mark attendance</h2>
          <ul className="space-y-2">
            {roster.map((student) => (
              <li key={student.id} className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 py-2">
                <span>{student.name}</span>
                <select
                  value={marks[student.id] || "present"}
                  onChange={(event) => setMarks((prev) => ({ ...prev, [student.id]: event.target.value }))}
                  className="rounded-md border border-slate-300 px-2 py-1 text-sm"
                >
                  <option value="present">Present</option>
                  <option value="late">Late</option>
                  <option value="absent">Absent</option>
                </select>
              </li>
            ))}
          </ul>
          <button
            type="submit"
            disabled={pending}
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          >
            {pending ? "Saving…" : "Save attendance"}
          </button>
        </form>
      ) : null}

      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="font-semibold">Attendance summary</h2>
        {summary.length === 0 ? (
          <p className="mt-2 text-sm text-slate-600">No attendance recorded yet.</p>
        ) : (
          <table className="mt-3 w-full text-left text-sm">
            <thead>
              <tr className="text-slate-500">
                <th className="py-1">Student</th>
                <th>Present</th>
                <th>Late</th>
                <th>Absent</th>
                <th>% present</th>
              </tr>
            </thead>
            <tbody>
              {summary.map((row) => (
                <tr key={row.student_id} className="border-t border-slate-100">
                  <td className="py-2">{row.student_name}</td>
                  <td>{row.present}</td>
                  <td>{row.late}</td>
                  <td>{row.absent}</td>
                  <td>{row.percent_present}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <h2 className="font-semibold">View attendance</h2>
        {records.length === 0 ? (
          <p className="mt-2 text-sm text-slate-600">No records for this selection.</p>
        ) : (
          <ul className="mt-3 space-y-2 text-sm">
            {records.map((row) => (
              <li key={row.id} className="flex justify-between border-b border-slate-100 py-2">
                <span>
                  {row.date} · {row.student_name}
                </span>
                <span className="capitalize">{row.status}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}
