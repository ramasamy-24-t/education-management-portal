import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

export default function AdminContactPanel() {
  const { token } = useAuth();
  const [rows, setRows] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api("/contact/messages", { token })
      .then(setRows)
      .catch((err) => setError(err.message));
  }, [token]);

  return (
    <section className="space-y-3 rounded-xl border border-slate-200 bg-white p-5">
      <h2 className="text-lg font-semibold">Contact messages</h2>
      <p className="text-sm text-slate-600">
        Public Contact form submissions are stored here. There is no outbound email from this portal.
      </p>
      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {rows.length === 0 && !error ? (
        <p className="text-sm text-slate-600">No messages yet.</p>
      ) : (
        <ul className="space-y-2 text-sm">
          {rows.map((row) => (
            <li key={row.id} className="rounded-md border border-slate-200 px-3 py-2">
              <p className="font-medium">
                {row.name} · {row.email}
              </p>
              <p className="mt-1 text-slate-700">{row.message}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
