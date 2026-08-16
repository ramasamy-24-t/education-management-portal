import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import CourseCard from "../components/CourseCard.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function Courses() {
  const { token } = useAuth();
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [categories, setCategories] = useState([]);
  const [courses, setCourses] = useState([]);
  const [topRated, setTopRated] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/courses/categories")
      .then(setCategories)
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    const params = new URLSearchParams();
    if (search.trim()) params.set("search", search.trim());
    if (category) params.set("category", category);
    const query = params.toString();
    api(`/courses${query ? `?${query}` : ""}`, { token })
      .then(setCourses)
      .catch((err) => setError(err.message));
  }, [search, category, token]);

  useEffect(() => {
    api("/courses/top-rated?limit=5", { token })
      .then(setTopRated)
      .catch((err) => setError(err.message));
  }, [token]);

  return (
    <section className="space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Public Pages</p>
      <h1 className="text-3xl font-bold">Courses</h1>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

      <div className="flex flex-wrap gap-3">
        <input
          type="search"
          placeholder="Search courses"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          className="min-w-[220px] flex-1 rounded-md border border-slate-300 px-3 py-2"
        />
        <select
          value={category}
          onChange={(event) => setCategory(event.target.value)}
          className="rounded-md border border-slate-300 px-3 py-2"
        >
          <option value="">All categories</option>
          {categories.map((item) => (
            <option key={item} value={item}>
              {item}
            </option>
          ))}
        </select>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-3 lg:col-span-2">
          <h2 className="text-lg font-semibold">Course listing</h2>
          {courses.length === 0 ? (
            <p className="text-slate-600">No courses match these filters.</p>
          ) : (
            <div className="grid gap-3 sm:grid-cols-2">
              {courses.map((course) => (
                <CourseCard key={course.id} course={course} />
              ))}
            </div>
          )}
        </div>
        <aside className="space-y-3">
          <h2 className="text-lg font-semibold">Top rated courses</h2>
          <div className="space-y-3">
            {topRated.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        </aside>
      </div>
    </section>
  );
}
