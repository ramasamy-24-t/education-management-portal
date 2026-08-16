const STYLES = {
  improving: "bg-emerald-100 text-emerald-800",
  worsening: "bg-red-100 text-red-800",
  stable: "bg-slate-200 text-slate-800",
};

const ARROWS = {
  improving: "↑",
  worsening: "↓",
  stable: "→",
};

export default function RiskTrend({ trend, reason, compact = false }) {
  const label = trend && STYLES[trend] ? trend : null;
  const text = label ? `${ARROWS[label]} ${label}` : "not enough data yet";
  const detail = label ? reason : reason || "Not enough data yet";

  return (
    <div className={compact ? "mt-1" : "mt-2"}>
      <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-semibold capitalize ${label ? STYLES[label] : "bg-slate-100 text-slate-500"}`}>
        {text}
      </span>
      {detail ? <p className={`text-slate-600 ${compact ? "mt-1 text-xs" : "mt-2 text-sm"}`}>{detail}</p> : null}
    </div>
  );
}
