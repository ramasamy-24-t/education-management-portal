import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

const emptyCourse = {
  title: "",
  description: "",
  category: "",
  schedule: "",
  syllabus: "",
  teacher_id: "",
};

export default function ManageCourses() {
  const { user, token } = useAuth();
  const [courses, setCourses] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [form, setForm] = useState(emptyCourse);
  const [editingId, setEditingId] = useState(null);
  const [className, setClassName] = useState("");
  const [activeCourseId, setActiveCourseId] = useState(null);
  const [classes, setClasses] = useState([]);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  const isAdmin = user?.role === "admin";

  async function loadCourses() {
    const query = isAdmin ? "" : `?teacher_id=${user.id}`;
    setCourses(await api(`/courses${query}`, { token }));
  }

  useEffect(() => {
    loadCourses().catch((err) => setError(err.message));
    if (isAdmin) {
      api("/teachers").then(setTeachers).catch((err) => setError(err.message));
    }
  }, [token, isAdmin, user?.id]);

  async function loadClasses(courseId) {
    setActiveCourseId(courseId);
    setClasses(await api(`/courses/${courseId}/classes`));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setPending(true);
    setError("");
    try {
      const body = {
        title: form.title,
        description: form.description,
        category: form.category,
        schedule: form.schedule,
        syllabus: form.syllabus,
      };
      if (isAdmin && form.teacher_id) body.teacher_id = Number(form.teacher_id);
      if (editingId) {
        await api(`/courses/${editingId}`, { method: "PATCH", token, body });
      } else {
        await api("/courses", { method: "POST", token, body });
      }
      setForm(emptyCourse);
      setEditingId(null);
      await loadCourses();
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  async function removeCourse(courseId) {
    if (!window.confirm("Delete this course? This only works if it has no attendance, assignments, or exams.")) {
      return;
    }
    setError("");
    try {
      await api(`/courses/${courseId}`, { method: "DELETE", token });
      if (activeCourseId === courseId) {
        setActiveCourseId(null);
        setClasses([]);
      }
      await loadCourses();
    } catch (err) {
      setError(err.message);
    }
  }

  async function addClass(event) {
    event.preventDefault();
    if (!activeCourseId) return;
    setError("");
    try {
      await api(`/courses/${activeCourseId}/classes`, {
        method: "POST",
        token,
        body: { name: className },
      });
      setClassName("");
      await loadClasses(activeCourseId);
      await loadCourses();
    } catch (err) {
      setError(err.message);
    }
  }

  async function removeClass(classId) {
    setError("");
    try {
      await api(`/classes/${classId}`, { method: "DELETE", token });
      await loadClasses(activeCourseId);
      await loadCourses();
    } catch (err) {
      setError(err.message);
    }
  }

  function startEdit(course) {
    setEditingId(course.id);
    setForm({
      title: course.title,
      description: course.description,
      category: course.category,
      schedule: course.schedule,
      syllabus: course.syllabus,
      teacher_id: String(course.teacher_id),
    });
  }

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {isAdmin ? "Admin Area" : "User Area"}
      </p>
      <h1 className="text-3xl font-bold">Manage courses & classes</h1>
      <p className="text-slate-600">
        Teachers can only edit their own courses. Admins can assign a teacher when creating a course.
      </p>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

      <form onSubmit={handleSubmit} className="grid gap-3 rounded-xl border border-slate-200 bg-white p-5 md:grid-cols-2">
        <h2 className="md:col-span-2 text-lg font-semibold">{editingId ? "Edit course" : "Create course"}</h2>
        <Input label="Title" value={form.title} onChange={(title) => setForm((prev) => ({ ...prev, title }))} />
        <Input label="Category" value={form.category} onChange={(category) => setForm((prev) => ({ ...prev, category }))} />
        <Input label="Schedule" value={form.schedule} onChange={(schedule) => setForm((prev) => ({ ...prev, schedule }))} />
        {isAdmin ? (
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-slate-700">Teacher</span>
            <select
              required={!editingId}
              value={form.teacher_id}
              onChange={(event) => setForm((prev) => ({ ...prev, teacher_id: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            >
              <option value="">Select teacher</option>
              {teachers.map((teacher) => (
                <option key={teacher.id} value={teacher.id}>
                  {teacher.name}
                </option>
              ))}
            </select>
          </label>
        ) : null}
        <label className="md:col-span-2 block text-sm">
          <span className="mb-1 block font-medium text-slate-700">Description</span>
          <textarea
            required
            value={form.description}
            onChange={(event) => setForm((prev) => ({ ...prev, description: event.target.value }))}
            className="w-full rounded-md border border-slate-300 px-3 py-2"
            rows={3}
          />
        </label>
        <label className="md:col-span-2 block text-sm">
          <span className="mb-1 block font-medium text-slate-700">Syllabus</span>
          <textarea
            value={form.syllabus}
            onChange={(event) => setForm((prev) => ({ ...prev, syllabus: event.target.value }))}
            className="w-full rounded-md border border-slate-300 px-3 py-2"
            rows={3}
          />
        </label>
        <div className="md:col-span-2 flex gap-2">
          <button
            type="submit"
            disabled={pending}
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          >
            {editingId ? "Save changes" : "Create course"}
          </button>
          {editingId ? (
            <button
              type="button"
              onClick={() => {
                setEditingId(null);
                setForm(emptyCourse);
              }}
              className="rounded-md border border-slate-300 px-4 py-2 text-sm"
            >
              Cancel
            </button>
          ) : null}
        </div>
      </form>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Courses</h2>
          {courses.map((course) => (
            <article key={course.id} className="rounded-xl border border-slate-200 bg-white p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <Link to={`/courses/${course.id}`} className="font-semibold hover:underline">
                    {course.title}
                  </Link>
                  <p className="text-sm text-slate-600">
                    {course.category} · {course.teacher_name} · {course.class_count} classes
                  </p>
                </div>
                <div className="flex gap-2">
                  <button type="button" onClick={() => startEdit(course)} className="text-sm underline">
                    Edit
                  </button>
                  <button type="button" onClick={() => removeCourse(course.id)} className="text-sm text-red-700 underline">
                    Delete
                  </button>
                </div>
              </div>
              <button
                type="button"
                onClick={() => loadClasses(course.id).catch((err) => setError(err.message))}
                className="mt-2 text-sm font-medium text-slate-800 underline"
              >
                Manage classes
              </button>
            </article>
          ))}
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">Classes</h2>
          {!activeCourseId ? (
            <p className="text-slate-600">Select a course to add or remove class sections.</p>
          ) : (
            <>
              <form onSubmit={addClass} className="flex gap-2">
                <input
                  required
                  value={className}
                  onChange={(event) => setClassName(event.target.value)}
                  placeholder="Class name, e.g. CS101-B"
                  className="flex-1 rounded-md border border-slate-300 px-3 py-2"
                />
                <button type="submit" className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white">
                  Add class
                </button>
              </form>
              <ul className="space-y-2">
                {classes.map((item) => (
                  <li key={item.id} className="flex items-center justify-between rounded-md border border-slate-200 bg-white px-3 py-2">
                    <span>{item.name}</span>
                    <button type="button" onClick={() => removeClass(item.id)} className="text-sm text-red-700 underline">
                      Delete
                    </button>
                  </li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </section>
  );
}

function Input({ label, value, onChange }) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block font-medium text-slate-700">{label}</span>
      <input
        required
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-md border border-slate-300 px-3 py-2"
      />
    </label>
  );
}
