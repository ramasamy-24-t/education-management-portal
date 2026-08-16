import PlaceholderPage from "../components/PlaceholderPage.jsx";

export default function AdminDashboard() {
  return (
    <PlaceholderPage
      area="Admin Area"
      title="Admin Dashboard"
      items={[
        "Manage Students",
        "Manage Teachers",
        "Manage Courses & Classes",
        "Manage Assignments",
        "Manage Exams & Grades",
        "View Reports & Analytics",
        "AI Insights & Monitoring",
      ]}
    />
  );
}
