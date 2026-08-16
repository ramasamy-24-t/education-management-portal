import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

export default function CourseDetails() {
  const { courseId } = useParams();
  const { user, token } = useAuth();
  const [course, setCourse] = useState(null);
  const [classes, setClasses] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [pending, setPending] = useState(false);
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

  async function load() {
    const [courseData, classData] = await Promise.all([
      api(`/courses/${courseId}`, { token }),
      api(`/courses/${courseId}/classes`),
    ]);
    setCourse(courseData);
    setClasses(classData);
  }

  useEffect(() => {
    load().catch((err) => setError(err.message));
  }, [courseId, token]);

  async function enroll() {
    if (!user) {
      setShowLoginPrompt(true);
      return;
    }
    setPending(true);
    setError("");
    setMessage("");
    try {
      await api("/enrollments", { method: "POST", token, body: { course_id: Number(courseId) } });
      setMessage("You are enrolled. Open your dashboard to see My Courses.");
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  if (!course && !error) {
    return <p className="text-slate-600">Loading course…</p>;
  }

  if (!course) {
    return <p className="text-red-700">{error}</p>;
  }

  const canEnroll = !user || user.role === "student";
  const canManage = user && (user.role === "admin" || (user.role === "teacher" && user.id === course.teacher_id));

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Public Pages</p>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-3xl font-bold">{course.title}</h1>
          <p className="mt-1 text-slate-600">
            {course.category} · ★ {Number(course.rating).toFixed(1)} · {course.enrollment_count} enrolled
          </p>
        </div>
        {canManage ? (
          <Link to="/manage/courses" className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white">
            Manage course
          </Link>
        ) : null}
      </div>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {message ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{message}</p> : null}

      <div className="grid gap-4 md:grid-cols-2">
        <Card title="Course info">
          <p>{course.description}</p>
        </Card>
        <Card title="Teacher info">
          <p>{course.teacher_name}</p>
        </Card>
        <Card title="Schedule">
          <p>{course.schedule}</p>
        </Card>
        <Card title="Classes">
          {classes.length === 0 ? (
            <p>No class sections yet.</p>
          ) : (
            <ul className="list-disc pl-5">
              {classes.map((item) => (
                <li key={item.id}>{item.name}</li>
              ))}
            </ul>
          )}
        </Card>
      </div>

      <Card title="Syllabus">
        <pre className="whitespace-pre-wrap font-sans text-sm text-slate-800">{course.syllabus || "No syllabus posted."}</pre>
      </Card>

      {canEnroll ? (
        course.enrolled ? (
          <p className="rounded-md bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-800">You are enrolled in this course.</p>
        ) : (
          <div className="space-y-3">
            <button
              type="button"
              onClick={enroll}
              disabled={pending}
              className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
            >
              {pending ? "Enrolling…" : "Enroll now"}
            </button>
            {showLoginPrompt ? (
              <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950">
                <p className="font-medium">Log in as a student to enroll.</p>
                <p className="mt-1">You will return to this course after signing in.</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  <Link
                    to="/login"
                    state={{ from: { pathname: `/courses/${courseId}` } }}
                    className="rounded-md bg-slate-900 px-3 py-1.5 text-white"
                  >
                    Go to login
                  </Link>
                  <button type="button" onClick={() => setShowLoginPrompt(false)} className="rounded-md px-3 py-1.5 underline">
                    Not now
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        )
      ) : (
        <p className="text-sm text-slate-600">Teachers and admins manage courses instead of enrolling.</p>
      )}
    </section>
  );
}

function Card({ title, children }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <h2 className="mb-2 font-semibold">{title}</h2>
      <div className="text-sm text-slate-700">{children}</div>
    </div>
  );
}
