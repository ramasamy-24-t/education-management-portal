import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

export default function AdminInsightsPanel() {
  const { token } = useAuth();
  const [data, setData] = useState({ configured: false, insights: [] });
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  async function load() {
    setData(await api("/ai/monitoring", { token }));
  }

  useEffect(() => {
    load().catch((err) => setError(err.message));
  }, [token]);

  async function refresh() {
    setPending(true);
    setError("");
    try {
      await api("/ai/monitoring/refresh", { method: "POST", token });
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="space-y-3 rounded-xl border border-violet-200 bg-violet-50 p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-lg font-semibold text-violet-950">AI insights & monitoring</h2>
        <button
          type="button"
          onClick={refresh}
          disabled={pending}
          className="rounded-md bg-slate-900 px-3 py-1.5 text-sm font-medium text-white disabled:opacity-60"
        >
          {pending ? "Refreshing…" : "Refresh insights"}
        </button>
      </div>
      <p className="text-sm text-violet-900">
        {data.configured
          ? "Azure Model Router is configured. Insights are stored in ai_insights for reports."
          : "Azure is not configured. Rule-based fallbacks are stored so this page still works."}
      </p>
      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {data.insights?.length ? (
        <ul className="space-y-2 text-sm">
          {data.insights.map((row) => (
            <li key={row.id} className="rounded-md border border-violet-200 bg-white px-3 py-2">
              <p className="font-medium capitalize">
                {row.type.replace("_", " ")}
                {row.student_name ? ` · ${row.student_name}` : ""}
                {row.class_name ? ` · ${row.class_name}` : ""}
              </p>
              <p className="mt-1 text-slate-700">{row.content}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-violet-900">No stored insights yet. Click refresh to generate class and at-risk notes.</p>
      )}
    </section>
  );
}
