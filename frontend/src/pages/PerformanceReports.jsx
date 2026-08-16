import { useEffect, useState, useRef } from "react";
import { api, downloadFile } from "../api/client.js";
import ClassSelect from "../components/ClassSelect.jsx";
import { useAuth } from "../hooks/useAuth.js";

export default function PerformanceReports() {
  const { user, token } = useAuth();
  const isStudent = user.role === "student";
  const isAdmin = user.role === "admin";
  const isTeacher = user.role === "teacher";

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [report, setReport] = useState(null);
  const [classes, setClasses] = useState([]);
  const [classId, setClassId] = useState("");
  const [classReport, setClassReport] = useState(null);
  const [comparative, setComparative] = useState(null);
  const [adminSummary, setAdminSummary] = useState(null);
  const [tab, setTab] = useState(isStudent ? "my" : "class");

  const printRef = useRef(null);

  useEffect(() => {
    loadInitial();
  }, [token, user.role]);

  async function loadInitial() {
    setLoading(true);
    setError("");
    try {
      if (isStudent) {
        const data = await api("/reports/me", { token });
        setReport(data);
      } else {
        const [cls, comp] = await Promise.all([
          api("/academic/classes", { token }),
          api("/reports/comparative", { token }),
        ]);
        setClasses(cls);
        setComparative(comp);
        if (cls[0]) {
          setClassId(String(cls[0].id));
          await loadClassReport(cls[0].id);
        }
        if (isAdmin) {
          const summary = await api("/reports/admin/summary", { token });
          setAdminSummary(summary);
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function loadClassReport(id) {
    if (!id) return;
    try {
      const data = await api(`/reports/class/${id}`, { token });
      setClassReport(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    if (classId && !isStudent) {
      loadClassReport(classId);
    }
  }, [classId]);

  async function handleDownloadPdf() {
    try {
      const path = isStudent ? "/reports/me/pdf" : null;
      if (!path) {
        window.print();
        return;
      }
      await downloadFile(path, { token, filename: "performance-report.pdf" });
    } catch (err) {
      setError(err.message);
    }
  }

  if (loading) {
    return (
      <section className="space-y-6">
        <h1 className="text-3xl font-bold">Performance Reports</h1>
        <p className="text-slate-600">Loading report data...</p>
      </section>
    );
  }

  return (
    <section className="space-y-6 print:space-y-4" ref={printRef}>
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 print:hidden">
        {isAdmin ? "Admin Area" : "Reports"}
      </p>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-3xl font-bold print:text-2xl">Performance Reports & Summary</h1>
        <div className="flex gap-2 print:hidden">
          {isStudent ? (
            <button
              type="button"
              onClick={handleDownloadPdf}
              className="rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white"
            >
              Download PDF
            </button>
          ) : null}
          <button
            type="button"
            onClick={() => window.print()}
            className="rounded-md border border-slate-300 px-3 py-2 text-sm font-medium"
          >
            Print
          </button>
        </div>
      </div>

      {error && <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

      {!isStudent && (
        <div className="flex gap-2 print:hidden">
          <TabButton active={tab === "class"} onClick={() => setTab("class")}>Class Report</TabButton>
          <TabButton active={tab === "comparative"} onClick={() => setTab("comparative")}>Comparative</TabButton>
          {isAdmin && <TabButton active={tab === "insights"} onClick={() => setTab("insights")}>AI Insights</TabButton>}
        </div>
      )}

      {isStudent && report && <StudentReport data={report} />}

      {!isStudent && tab === "class" && (
        <>
          <ClassSelect classes={classes} value={classId} onChange={setClassId} />
          {classReport && <ClassReportView data={classReport} token={token} />}
          {!classReport && <p className="text-slate-600">Select a class to view its report.</p>}
        </>
      )}

      {!isStudent && tab === "comparative" && comparative && <ComparativeView data={comparative} />}

      {isAdmin && tab === "insights" && adminSummary && <AdminInsightsView data={adminSummary} />}
    </section>
  );
}

function TabButton({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`rounded-md px-3 py-1.5 text-sm font-medium ${
        active ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700 hover:bg-slate-200"
      }`}
    >
      {children}
    </button>
  );
}

function StudentReport({ data }) {
  return (
    <div className="space-y-4">
      <Card title="Academic Performance Summary">
        <dl className="grid gap-3 sm:grid-cols-2 md:grid-cols-4 text-sm">
          <Stat label="Attendance" value={`${data.attendance_percent}%`} />
          <Stat label="Exam Average" value={`${data.exam_average}%`} />
          <Stat label="Assignments" value={`${data.assignments_submitted}/${data.assignments_total}`} />
          <Stat label="At Risk" value={data.at_risk ? "Yes" : "No"} warn={data.at_risk} />
        </dl>
      </Card>

      <Card title="Weak Areas Identified" variant="warning">
        {data.weak_subjects?.length ? (
          <ul className="list-disc pl-5 text-sm space-y-1">
            {data.weak_subjects.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        ) : (
          <p className="text-sm text-slate-600">No weak areas flagged.</p>
        )}
      </Card>

      <Card title="Risk Analysis" variant={data.at_risk ? "danger" : "success"}>
        <p className="text-sm">{data.risk_reason || (data.at_risk ? "Flagged as at-risk based on attendance or exam scores." : "Not currently at risk.")}</p>
      </Card>

      <Card title="AI Recommendations" variant="ai">
        {data.ai_recommendations?.length ? (
          <ul className="list-disc pl-5 text-sm space-y-1">
            {data.ai_recommendations.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        ) : (
          <p className="text-sm">No recommendations yet. Visit My Progress to generate them.</p>
        )}
      </Card>

      {data.grade_lines?.length > 0 && (
        <Card title="Grade History">
          <ul className="text-sm space-y-1">
            {data.grade_lines.map((line, i) => <li key={i}>{line}</li>)}
          </ul>
        </Card>
      )}
    </div>
  );
}

function ClassReportView({ data, token }) {
  const [pdfError, setPdfError] = useState("");

  async function downloadStudentPdf(studentId, name) {
    const safe = (name || "student").toLowerCase().replace(/[^a-z0-9]+/g, "-");
    setPdfError("");
    try {
      await downloadFile(`/reports/student/${studentId}/pdf`, {
        token,
        filename: `performance-report-${safe}.pdf`,
      });
    } catch (err) {
      setPdfError(err.message);
    }
  }
  return (
    <div className="space-y-4">
      {pdfError ? <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-700">{pdfError}</p> : null}
      <Card title={`Class: ${data.class_name} — ${data.course_title}`}>
        <dl className="grid gap-3 sm:grid-cols-2 md:grid-cols-4 text-sm">
          <Stat label="Students" value={data.student_count} />
          <Stat label="Avg Attendance" value={`${data.average_attendance}%`} />
          <Stat label="Avg Exam Score" value={`${data.average_exam}%`} />
          <Stat label="At Risk" value={data.at_risk_count} warn={data.at_risk_count > 0} />
        </dl>
      </Card>

      {data.class_insight && (
        <Card title="AI Class Insight" variant="ai">
          <p className="text-sm">{data.class_insight}</p>
        </Card>
      )}

      {data.at_risk_students?.length > 0 && (
        <Card title="At-Risk Students" variant="danger">
          <ul className="text-sm space-y-1">
            {data.at_risk_students.map((s) => (
              <li key={s.id}>{s.name} — Attendance {s.attendance}%, Exam Avg {s.exam_avg}%</li>
            ))}
          </ul>
        </Card>
      )}

      {data.student_summaries?.length > 0 && (
        <Card title="All Students">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="py-2 pr-4">Name</th>
                  <th className="py-2 pr-4">Attendance</th>
                  <th className="py-2 pr-4">Exam Avg</th>
                  <th className="py-2 pr-4">Status</th>
                  <th className="py-2 print:hidden">Report</th>
                </tr>
              </thead>
              <tbody>
                {data.student_summaries.map((s) => (
                  <tr key={s.id} className="border-b last:border-0">
                    <td className="py-2 pr-4">{s.name}</td>
                    <td className="py-2 pr-4">{s.attendance}%</td>
                    <td className="py-2 pr-4">{s.exam_avg}%</td>
                    <td className="py-2">
                      {s.at_risk ? (
                        <span className="rounded bg-red-100 px-2 py-0.5 text-red-800 text-xs">At Risk</span>
                      ) : (
                        <span className="rounded bg-emerald-100 px-2 py-0.5 text-emerald-800 text-xs">OK</span>
                      )}
                    </td>
                    <td className="py-2 print:hidden">
                      <button
                        type="button"
                        onClick={() => downloadStudentPdf(s.id, s.name)}
                        className="text-sm font-medium underline"
                      >
                        Download PDF
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}

function ComparativeView({ data }) {
  return (
    <div className="space-y-4">
      <Card title="Comparative Overview">
        <dl className="grid gap-3 sm:grid-cols-2 md:grid-cols-4 text-sm">
          <Stat label="Total Classes" value={data.total_classes} />
          <Stat label="Total Students" value={data.total_students} />
          <Stat label="Total At Risk" value={data.total_at_risk} warn={data.total_at_risk > 0} />
          <Stat label="At Risk %" value={`${data.overall_at_risk_percent}%`} warn={data.overall_at_risk_percent > 20} />
        </dl>
      </Card>

      {data.classes?.length > 0 && (
        <Card title="Class Comparison">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="py-2 pr-4">Class</th>
                  <th className="py-2 pr-4">Course</th>
                  <th className="py-2 pr-4">Students</th>
                  <th className="py-2 pr-4">Avg Attendance</th>
                  <th className="py-2 pr-4">Avg Exam</th>
                  <th className="py-2">At Risk</th>
                </tr>
              </thead>
              <tbody>
                {data.classes.map((c) => (
                  <tr key={c.class_id} className="border-b last:border-0">
                    <td className="py-2 pr-4">{c.class_name}</td>
                    <td className="py-2 pr-4">{c.course_title}</td>
                    <td className="py-2 pr-4">{c.student_count}</td>
                    <td className="py-2 pr-4">{c.average_attendance}%</td>
                    <td className="py-2 pr-4">{c.average_exam}%</td>
                    <td className="py-2">{c.at_risk_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}

      {data.ai_recommendations_rollup?.length > 0 && (
        <Card title="AI Recommendations Rollup" variant="ai">
          <ul className="list-disc pl-5 text-sm space-y-1">
            {data.ai_recommendations_rollup.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        </Card>
      )}
    </div>
  );
}

function AdminInsightsView({ data }) {
  const counts = data.insight_counts || {};
  return (
    <div className="space-y-4">
      <Card title="Insight Statistics">
        <dl className="grid gap-3 sm:grid-cols-3 md:grid-cols-5 text-sm">
          <Stat label="Performance" value={counts.performance || 0} />
          <Stat label="At Risk" value={counts.at_risk || 0} />
          <Stat label="Weak Subject" value={counts.weak_subject || 0} />
          <Stat label="Recommendations" value={counts.recommendation || 0} />
          <Stat label="Class Insights" value={counts.class_insight || 0} />
        </dl>
      </Card>

      {data.recent_insights?.length > 0 && (
        <Card title="Recent AI Insights">
          <ul className="space-y-2 text-sm">
            {data.recent_insights.map((row, i) => (
              <li key={i} className="rounded-md border border-slate-200 bg-white px-3 py-2">
                <span className="font-medium capitalize">{row.type.replace("_", " ")}</span>
                <p className="mt-1 text-slate-700">{row.content}</p>
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}

function Card({ title, variant, children }) {
  const variantStyles = {
    warning: "border-amber-200 bg-amber-50",
    danger: "border-red-200 bg-red-50",
    success: "border-emerald-200 bg-emerald-50",
    ai: "border-violet-200 bg-violet-50",
  };
  const style = variantStyles[variant] || "border-slate-200 bg-white";

  return (
    <div className={`rounded-xl border p-5 ${style} print:break-inside-avoid`}>
      <h2 className="text-lg font-semibold mb-3">{title}</h2>
      {children}
    </div>
  );
}

function Stat({ label, value, warn }) {
  return (
    <div className={`rounded-md px-3 py-2 ${warn ? "bg-red-100" : "bg-slate-50"}`}>
      <dt className="text-slate-500">{label}</dt>
      <dd className={`font-medium ${warn ? "text-red-800" : ""}`}>{value}</dd>
    </div>
  );
}
