import { useEffect, useRef, useState } from "react";
import { api } from "../api/client.js";

const MAX_MESSAGES = 16;

export default function AssistantChat({ studentId, token }) {
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  async function send(event) {
    event.preventDefault();
    const question = draft.trim();
    if (!question || sending) return;

    setDraft("");
    setError("");
    setSending(true);
    const nextMessages = [...messages, { role: "user", text: question }].slice(-MAX_MESSAGES);
    setMessages(nextMessages);

    const history = nextMessages.slice(0, -1).slice(-6).map((item) => ({
      role: item.role,
      content: item.text,
    }));

    try {
      const payload = await api(`/ai/assistant/${studentId}`, {
        method: "POST",
        token,
        body: { question, history },
      });
      const answer = payload.answer || "No answer came back. Try again.";
      setMessages((prev) => [...prev, { role: "assistant", text: answer }].slice(-MAX_MESSAGES));
    } catch (err) {
      setError(err.message || "Could not reach the assistant.");
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900 p-5 text-slate-100">
      <h2 className="text-lg font-semibold text-white">Ask about your progress</h2>
      <p className="mt-1 text-sm text-slate-300">
        A short Q&amp;A over your attendance, grades, weak subjects, and assignment feedback. Off-topic
        questions get a polite redirect.
      </p>

      <div className="mt-3 max-h-72 space-y-2 overflow-y-auto rounded-lg bg-slate-800/80 p-3">
        {messages.length === 0 && !sending ? (
          <p className="text-sm text-slate-400">
            Try “Why is my attendance flagged?” or “What should I study first?”
          </p>
        ) : null}
        {messages.map((item, index) => (
          <div
            key={`${item.role}-${index}-${item.text.slice(0, 24)}`}
            className={`max-w-[90%] rounded-lg px-3 py-2 text-sm ${
              item.role === "user"
                ? "ml-auto bg-violet-600 text-white"
                : "bg-slate-700 text-slate-100"
            }`}
          >
            {item.text}
          </div>
        ))}
        {sending ? <p className="text-sm text-slate-400">Thinking…</p> : null}
        <div ref={bottomRef} />
      </div>

      {error ? (
        <p className="mt-2 rounded-md bg-red-950 px-3 py-2 text-sm text-red-200">{error}</p>
      ) : null}

      <form onSubmit={send} className="mt-3 flex flex-wrap gap-2">
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          maxLength={500}
          placeholder="Ask about your courses, grades, or study plan"
          className="min-w-0 flex-1 rounded-md border border-slate-600 bg-slate-800 px-3 py-2 text-sm text-white placeholder:text-slate-500"
        />
        <button
          type="submit"
          disabled={sending || !draft.trim()}
          className="rounded-md bg-violet-500 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
        >
          {sending ? "Sending…" : "Send"}
        </button>
      </form>
    </section>
  );
}
