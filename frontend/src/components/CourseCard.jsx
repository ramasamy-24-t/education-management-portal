import { Link } from "react-router-dom";

export default function CourseCard({ course }) {
  return (
    <Link
      to={`/courses/${course.id}`}
      className="block rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition hover:border-slate-300 hover:shadow"
    >
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-lg font-semibold text-slate-900">{course.title}</h3>
        <span className="shrink-0 rounded-full bg-amber-50 px-2 py-0.5 text-sm font-medium text-amber-800">
          ★ {Number(course.rating).toFixed(1)}
        </span>
      </div>
      <p className="mt-1 text-sm text-slate-500">{course.category}</p>
      <p className="mt-2 line-clamp-2 text-sm text-slate-700">{course.description}</p>
      <p className="mt-3 text-sm text-slate-600">
        {course.teacher_name} · {course.schedule}
      </p>
    </Link>
  );
}
