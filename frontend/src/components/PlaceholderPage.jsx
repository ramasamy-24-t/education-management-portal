export default function PlaceholderPage({ title, area, items }) {
  return (
    <section className="space-y-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{area}</p>
      <h1 className="text-3xl font-bold">{title}</h1>
      <p className="text-slate-600">
        Placeholder route for this diagram box. Features below will be wired in later prompts.
      </p>
      <ul className="list-disc space-y-1 pl-6 text-slate-800">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}
