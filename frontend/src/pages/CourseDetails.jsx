import { useParams } from "react-router-dom";
import PlaceholderPage from "../components/PlaceholderPage.jsx";

export default function CourseDetails() {
  const { courseId } = useParams();
  return (
    <PlaceholderPage
      area="Public Pages"
      title={`Course Details (${courseId ?? "sample"})`}
      items={["Course Info", "Syllabus", "Teacher Info", "Schedule", "Enroll Now"]}
    />
  );
}
