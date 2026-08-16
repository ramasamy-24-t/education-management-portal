import PlaceholderPage from "../components/PlaceholderPage.jsx";

export default function UserDashboard() {
  return (
    <PlaceholderPage
      area="User Area"
      title="User Dashboard"
      items={[
        "Profile",
        "My Courses",
        "My Assignments",
        "Attendance",
        "Grades",
        "AI Recommendations",
        "Progress Overview",
      ]}
    />
  );
}
