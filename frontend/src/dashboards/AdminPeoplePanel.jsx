import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

const empty = { name: "", email: "", password: "", role: "student" };

export default function AdminPeoplePanel() {
  const { token } = useAuth();
  const [role, setRole] = useState("student");
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(empty);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function load(nextRole = role) {
    setUsers(await api(`/admin/users?role=${nextRole}`, { token }));
  }

  useEffect(() => {
    load(role).catch((err) => setError(err.message));
  }, [role, token]);

  async function createUser(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      await api("/admin/users", { method: "POST", token, body: { ...form, role } });
      setForm({ ...empty, role });
      setMessage(`${role} created.`);
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function toggleActive(user) {
    setError("");
    try {
      await api(`/admin/users/${user.id}`, {
        method: "PATCH",
        token,
        body: { is_active: !user.is_active },
      });
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section className="space-y-4 rounded-xl border border-slate-200 bg-white p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-lg font-semibold">Manage {role === "student" ? "students" : "teachers"}</h2>
        <div className="flex gap-2">
          {["student", "teacher"].map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => setRole(item)}
              className={`rounded-md px-3 py-1.5 text-sm capitalize ${
                role === item ? "bg-slate-900 text-white" : "bg-slate-200"
              }`}
            >
              {item}s
            </button>
          ))}
        </div>
      </div>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {message ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{message}</p> : null}

      <form onSubmit={createUser} className="grid gap-2 md:grid-cols-4">
        <input
          required
          placeholder="Name"
          value={form.name}
          onChange={(event) => setForm((prev) => ({ ...prev, name: event.target.value }))}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
        />
        <input
          required
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
        />
        <input
          required
          type="password"
          minLength={8}
          placeholder="Password"
          value={form.password}
          onChange={(event) => setForm((prev) => ({ ...prev, password: event.target.value }))}
          className="rounded-md border border-slate-300 px-3 py-2 text-sm"
        />
        <button type="submit" className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white">
          Create {role}
        </button>
      </form>

      <table className="w-full text-left text-sm">
        <thead>
          <tr className="text-slate-500">
            <th className="py-1">Name</th>
            <th>Email</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id} className="border-t border-slate-100">
              <td className="py-2">{user.name}</td>
              <td>{user.email}</td>
              <td>{user.is_active ? "Active" : "Deactivated"}</td>
              <td>
                <button type="button" onClick={() => toggleActive(user)} className="underline">
                  {user.is_active ? "Deactivate" : "Reactivate"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
