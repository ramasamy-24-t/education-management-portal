import { useEffect, useRef, useState } from "react";
import { api } from "../api/client.js";
import { useAuth } from "../hooks/useAuth.js";

const MAX_MESSAGES = 16;

export default function AssistantChat() {
  const { user, token } = useAuth();
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending, open]);

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  if (!user || user.role !== "student" || !token) return null;

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
      const payload = await api(`/ai/assistant/${user.id}`, {
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
    <div className="fixed bottom-5 right-5 z-40 print:hidden">
      {open ? (
        <div className="mb-3 w-[min(22rem,calc(100vw-2.5rem))]">
          <div className="rounded-[1.75rem] border border-slate-200 bg-white p-4 shadow-2xl shadow-black/20">
            <div className="flex items-start justify-between gap-2">
              <div>
                <p className="font-semibold text-slate-900">Study assistant</p>
                <p className="text-xs text-slate-500">Ask about your attendance, grades, or study plan.</p>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="rounded-full px-2 text-lg leading-none text-slate-500 hover:bg-slate-100"
                aria-label="Close assistant"
              >
                ×
              </button>
            </div>

            <div className="mt-3 max-h-64 space-y-2 overflow-y-auto rounded-2xl bg-slate-50 p-3">
              {messages.length === 0 && !sending ? (
                <p className="text-sm text-slate-500">
                  Try “Why is my attendance flagged?” or “What should I study first?”
                </p>
              ) : null}
              {messages.map((item, index) => (
                <div
                  key={`${item.role}-${index}-${item.text.slice(0, 24)}`}
                  className={`max-w-[90%] rounded-2xl px-3 py-2 text-sm ${
                    item.role === "user"
                      ? "ml-auto bg-black text-white"
                      : "bg-white text-slate-800 shadow-sm"
                  }`}
                >
                  {item.text}
                </div>
              ))}
              {sending ? <p className="text-sm text-slate-500">Thinking…</p> : null}
              <div ref={bottomRef} />
            </div>

            {error ? <p className="mt-2 text-xs text-red-700">{error}</p> : null}

            <form onSubmit={send} className="mt-3 flex gap-2">
              <input
                ref={inputRef}
                value={draft}
                onChange={(event) => setDraft(event.target.value)}
                maxLength={500}
                placeholder="Ask a question…"
                className="min-w-0 flex-1 rounded-full border border-slate-200 px-3 py-2 text-sm"
              />
              <button
                type="submit"
                disabled={sending || !draft.trim()}
                className="rounded-full bg-black px-3 py-2 text-sm font-medium text-white disabled:opacity-60"
              >
                Send
              </button>
            </form>
          </div>
        </div>
      ) : null}

      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="ml-auto flex h-14 w-14 items-center justify-center rounded-full bg-black text-white shadow-lg shadow-black/30 transition hover:scale-105"
        aria-label={open ? "Close study assistant" : "Open study assistant"}
      >
        {open ? (
          <span className="text-2xl leading-none">×</span>
        ) : (
          <RobotIcon />
        )}
      </button>
    </div>
  );
}

function RobotIcon() {
  return (
    <svg viewBox="0 0 24 24" className="h-7 w-7" fill="none" aria-hidden="true">
      <rect x="5" y="8" width="14" height="11" rx="3" stroke="currentColor" strokeWidth="1.8" />
      <circle cx="9.5" cy="13" r="1.2" fill="currentColor" />
      <circle cx="14.5" cy="13" r="1.2" fill="currentColor" />
      <path d="M12 4v4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      <circle cx="12" cy="3.5" r="1.2" fill="currentColor" />
      <path d="M8 19.5v1.2M16 19.5v1.2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}
