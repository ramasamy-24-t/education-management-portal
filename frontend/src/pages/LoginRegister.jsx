import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

const emptyRegister = { name: "", email: "", password: "", role: "student" };

export default function LoginRegister() {
  const { user, login, register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mode, setMode] = useState("login");
  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [registerForm, setRegisterForm] = useState(emptyRegister);
  const [error, setError] = useState("");
  const [pending, setPending] = useState(false);

  if (user) {
    const dest = user.role === "admin" ? "/admin" : "/dashboard";
    return <Navigate to={dest} replace />;
  }

  const redirectTo = location.state?.from?.pathname || "/dashboard";

  async function handleLogin(event) {
    event.preventDefault();
    setError("");
    setPending(true);
    try {
      await login(loginForm.email, loginForm.password);
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  async function handleRegister(event) {
    event.preventDefault();
    setError("");
    setPending(true);
    try {
      await register(registerForm);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="mx-auto max-w-md space-y-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">User Area</p>
      <h1 className="text-3xl font-bold">User Login / Register</h1>
      <p className="text-slate-600">
        Students and teachers sign in here. Admins use{" "}
        <Link to="/admin/login" className="font-medium text-slate-900 underline">
          Admin Login
        </Link>
        .
      </p>

      <div className="flex rounded-lg bg-slate-200 p-1">
        {["login", "register"].map((item) => (
          <button
            key={item}
            type="button"
            onClick={() => {
              setMode(item);
              setError("");
            }}
            className={`flex-1 rounded-md px-3 py-2 text-sm font-medium capitalize ${
              mode === item ? "bg-white text-slate-900 shadow-sm" : "text-slate-600"
            }`}
          >
            {item}
          </button>
        ))}
      </div>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}

      {mode === "login" ? (
        <form onSubmit={handleLogin} className="space-y-4 rounded-xl border border-slate-200 bg-white p-5">
          <Field
            label="Email"
            type="email"
            value={loginForm.email}
            onChange={(email) => setLoginForm((prev) => ({ ...prev, email }))}
          />
          <Field
            label="Password"
            type="password"
            value={loginForm.password}
            onChange={(password) => setLoginForm((prev) => ({ ...prev, password }))}
          />
          <button
            type="submit"
            disabled={pending}
            className="w-full rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          >
            {pending ? "Signing in…" : "Sign in"}
          </button>
        </form>
      ) : (
        <form onSubmit={handleRegister} className="space-y-4 rounded-xl border border-slate-200 bg-white p-5">
          <Field
            label="Full name"
            value={registerForm.name}
            onChange={(name) => setRegisterForm((prev) => ({ ...prev, name }))}
          />
          <Field
            label="Email"
            type="email"
            value={registerForm.email}
            onChange={(email) => setRegisterForm((prev) => ({ ...prev, email }))}
          />
          <Field
            label="Password"
            type="password"
            value={registerForm.password}
            onChange={(password) => setRegisterForm((prev) => ({ ...prev, password }))}
          />
          <fieldset>
            <legend className="mb-2 text-sm font-medium text-slate-700">Role</legend>
            <div className="flex gap-4">
              {["student", "teacher"].map((role) => (
                <label key={role} className="flex items-center gap-2 text-sm capitalize">
                  <input
                    type="radio"
                    name="role"
                    value={role}
                    checked={registerForm.role === role}
                    onChange={() => setRegisterForm((prev) => ({ ...prev, role }))}
                  />
                  {role}
                </label>
              ))}
            </div>
          </fieldset>
          <button
            type="submit"
            disabled={pending}
            className="w-full rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          >
            {pending ? "Creating account…" : "Create account"}
          </button>
        </form>
      )}
    </section>
  );
}

function Field({ label, type = "text", value, onChange }) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block font-medium text-slate-700">{label}</span>
      <input
        type={type}
        required
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-slate-500"
      />
    </label>
  );
}
