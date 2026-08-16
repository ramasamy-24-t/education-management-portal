export default function ClassSelect({ classes, value, onChange, label = "Class" }) {
  return (
    <label className="block text-sm">
      <span className="mb-1 block font-medium text-slate-700">{label}</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-md border border-slate-300 px-3 py-2"
      >
        <option value="">Select a class</option>
        {classes.map((item) => (
          <option key={item.id} value={item.id}>
            {item.course_title} — {item.name}
          </option>
        ))}
      </select>
    </label>
  );
}
