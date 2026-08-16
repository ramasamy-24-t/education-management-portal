import { useEffect, useState } from "react";
import { api } from "../api/client.js";

const emptyForm = { name: "", email: "", message: "" };

export default function Contact() {
  const [info, setInfo] = useState(null);
  const [faqs, setFaqs] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [pending, setPending] = useState(false);
  const [openFaq, setOpenFaq] = useState(null);

  useEffect(() => {
    Promise.all([api("/contact/info"), api("/faqs")])
      .then(([nextInfo, nextFaqs]) => {
        setInfo(nextInfo);
        setFaqs(nextFaqs);
      })
      .catch((err) => setError(err.message));
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    setPending(true);
    setError("");
    setSuccess("");
    try {
      await api("/contact", { method: "POST", body: form });
      setForm(emptyForm);
      setSuccess("Message sent. An admin will follow up by email.");
    } catch (err) {
      setError(err.message);
    } finally {
      setPending(false);
    }
  }

  return (
    <section className="space-y-8">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Public Pages</p>
      <h1 className="text-3xl font-bold">Contact</h1>

      {error ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
      {success ? <p className="rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-800">{success}</p> : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-4">
          <div className="rounded-xl border border-slate-200 bg-white p-5">
            <h2 className="text-lg font-semibold">Contact info</h2>
            {info ? (
              <dl className="mt-3 space-y-2 text-sm text-slate-700">
                <div>
                  <dt className="font-medium text-slate-500">Organization</dt>
                  <dd>{info.organization}</dd>
                </div>
                <div>
                  <dt className="font-medium text-slate-500">Email</dt>
                  <dd>{info.email}</dd>
                </div>
                <div>
                  <dt className="font-medium text-slate-500">Phone</dt>
                  <dd>{info.phone}</dd>
                </div>
                <div>
                  <dt className="font-medium text-slate-500">Address</dt>
                  <dd>{info.address}</dd>
                </div>
                <div>
                  <dt className="font-medium text-slate-500">Hours</dt>
                  <dd>{info.hours}</dd>
                </div>
              </dl>
            ) : (
              <p className="mt-2 text-sm text-slate-600">Loading contact info…</p>
            )}
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5">
            <h2 className="text-lg font-semibold">Support</h2>
            {info ? (
              <>
                <p className="mt-2 text-sm text-slate-700">
                  Email <span className="font-medium">{info.support_email}</span>
                </p>
                <p className="mt-2 text-sm text-slate-600">{info.support_note}</p>
              </>
            ) : null}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3 rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="text-lg font-semibold">Contact form</h2>
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-slate-700">Name</span>
            <input
              required
              value={form.name}
              onChange={(event) => setForm((prev) => ({ ...prev, name: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-slate-700">Email</span>
            <input
              type="email"
              required
              value={form.email}
              onChange={(event) => setForm((prev) => ({ ...prev, email: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
          <label className="block text-sm">
            <span className="mb-1 block font-medium text-slate-700">Message</span>
            <textarea
              required
              minLength={10}
              rows={5}
              value={form.message}
              onChange={(event) => setForm((prev) => ({ ...prev, message: event.target.value }))}
              className="w-full rounded-md border border-slate-300 px-3 py-2"
            />
          </label>
          <button
            type="submit"
            disabled={pending}
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          >
            {pending ? "Sending…" : "Send message"}
          </button>
        </form>
      </div>

      <div className="space-y-3">
        <h2 className="text-lg font-semibold">FAQ</h2>
        {faqs.length === 0 ? (
          <p className="text-slate-600">No FAQs yet.</p>
        ) : (
          <ul className="space-y-2">
            {faqs.map((item) => {
              const open = openFaq === item.id;
              return (
                <li key={item.id} className="rounded-xl border border-slate-200 bg-white">
                  <button
                    type="button"
                    onClick={() => setOpenFaq(open ? null : item.id)}
                    className="flex w-full items-center justify-between px-4 py-3 text-left font-medium"
                  >
                    {item.question}
                    <span className="text-slate-400">{open ? "−" : "+"}</span>
                  </button>
                  {open ? <p className="px-4 pb-4 text-sm text-slate-700">{item.answer}</p> : null}
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </section>
  );
}
