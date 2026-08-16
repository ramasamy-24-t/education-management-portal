-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 16, 2026 at 01:49 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `education_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `ai_insights`
--

CREATE TABLE `ai_insights` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `type` enum('performance','at_risk','weak_subject','recommendation','class_insight') NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `trend` varchar(32) DEFAULT NULL,
  `trend_reason` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `ai_insights`
--

INSERT INTO `ai_insights` (`id`, `student_id`, `class_id`, `type`, `content`, `created_at`, `trend`, `trend_reason`) VALUES
(1, 5, 2, 'at_risk', 'Attendance is significantly lower than classmates at 61.6%, which may hinder consistent understanding of cumulative Linear Algebra concepts despite a moderate exam average of 70.0.', '2026-08-16 07:10:33', NULL, NULL),
(2, 5, 1, 'weak_subject', 'Proof-style questions in Linear Algebra are a weak area; Python fundamentals are strong.', '2026-08-16 11:16:35', NULL, NULL),
(3, 5, NULL, 'recommendation', 'Focus on low-scoring quizzes and checkpoints | Review Python and Linear Algebra fundamentals weekly | Use practice tests to raise exam consistency', '2026-08-16 10:25:02', NULL, NULL),
(4, 6, 1, 'performance', 'Ananya is consistent in Python with high attendance and assignment scores.', '2026-08-16 11:16:35', NULL, NULL),
(5, NULL, 1, 'class_insight', 'CS101-A shows moderate overall performance, with a class exam average of 70.0 and average attendance of 82.8. Engagement appears uneven: one student has perfect attendance and strong performance, one has solid attendance but weaker exam results, and one has low attendance that may limit consistency. Teaching focus should be on reinforcing foundational Python concepts for lower-performing students while improving participation and attendance follow-through.', '2026-08-16 07:10:21', NULL, NULL),
(6, 5, NULL, 'performance', 'Rohan shows strong academic engagement with excellent attendance (97.4%) and solid assignment completion (10/12). Overall performance is moderate, with an exam average of 66.7%, indicating he is passing but not consistently strong across all assessments. His best area appears to be Statistics for Decision Making, while Data Structures shows mixed performance with strong smoke exam scores but weaker quiz and checkpoint results. Introduction to Python and Linear Algebra are also weaker areas based on midterm and checkpoint scores in the high-50s to low-60s.', '2026-08-16 10:25:02', NULL, NULL),
(7, 5, NULL, 'at_risk', 'Not currently flagged as at-risk.', '2026-08-16 10:25:02', 'stable', 'Exam average improved from 63.2 to 68.2, but attendance declined from 100.0% to 94.8%, so the overall trend is mixed.'),
(8, 5, NULL, 'weak_subject', 'Data Structures; Introduction to Python; Linear Algebra', '2026-08-16 10:25:02', NULL, NULL),
(9, NULL, 4, 'class_insight', 'CS201-A shows strong overall attendance (average 87.2%) and moderate exam performance (average 72.7%). Two students maintain perfect attendance, suggesting solid engagement across most of the class, but exam averages clustered between 70 and 78 indicate room to deepen conceptual understanding in Data Structures. A useful teaching move would be to reinforce core problem-solving patterns and provide targeted support for students whose attendance may be limiting their progress.', '2026-08-16 12:40:11', NULL, NULL),
(10, 5, 4, 'at_risk', 'Attendance is significantly lower than classmates at 61.6%, which may hinder continuity of learning, even though the exam average is 70.0.', '2026-08-16 12:40:11', NULL, NULL),
(11, 5, 1, 'at_risk', 'Attendance is significantly lower than classmates (61.6), which may put the student at risk of falling behind even though current exam performance is borderline acceptable (70.0).', '2026-08-16 12:40:21', NULL, NULL),
(12, NULL, 2, 'class_insight', 'MATH201-B / Linear Algebra is showing generally steady performance, with an average exam score of 71.8 and average attendance of 87.2 based on the provided data. Two students have perfect attendance, which suggests strong engagement, while overall achievement is moderate rather than high. The main instructional priority is addressing attendance-related risk, since lower presence in class may affect continuity of understanding in cumulative topics.', '2026-08-16 12:40:33', NULL, NULL),
(13, NULL, 5, 'class_insight', 'STAT101-A shows strong overall attendance (average 87.1%) and moderate exam performance (average 70.7%). Two students have perfect attendance, suggesting good engagement across much of the class, but performance is uneven: the top exam average is 78.0 while the lowest is 64.7. A key teaching insight is that attendance alone is not fully translating into achievement for all students, so the class may benefit from more targeted practice on core statistical reasoning and decision-making applications, along with quick checks for understanding during instruction.', '2026-08-16 12:40:47', NULL, NULL),
(14, 5, 5, 'at_risk', 'Attendance is notably low (61.6%), which may put future performance at risk even though the current exam average (70.0) is near the class average.', '2026-08-16 12:40:47', NULL, NULL),
(15, NULL, 3, 'class_insight', 'HIST110-A shows strong overall attendance (about 95.6% on average), but exam performance is more mixed (about 72.7 average). Two students are performing in the mid-to-high 70s with perfect attendance, suggesting solid engagement and understanding. The main instructional need is targeted support for lower-performing students while maintaining challenge for those already meeting expectations.', '2026-08-16 12:41:00', NULL, NULL),
(16, 6, NULL, 'performance', 'Ananya shows steady overall performance with strong assignment completion and generally good attendance. Exam results are moderate, with Introduction to Python as the strongest subject and weaker performance in World History and Statistics. Class attendance is excellent in CS101-A but lower in STAT101-A and HIST110-A, which may be contributing to the lower scores in those subjects.', '2026-08-16 12:43:12', NULL, NULL),
(17, 6, NULL, 'at_risk', 'Not currently flagged as at-risk.', '2026-08-16 12:43:12', NULL, NULL),
(18, 6, NULL, 'weak_subject', 'World History: 1900–Present; Statistics for Decision Making', '2026-08-16 12:43:12', NULL, NULL),
(19, 6, NULL, 'recommendation', 'Focus revision on History and Statistics concepts. | Raise attendance in STAT101-A and HIST110-A. | Keep up strong assignment completion and Python performance.', '2026-08-16 12:43:12', NULL, NULL),
(20, 17, NULL, 'performance', 'Ram\'s record shows no measurable academic engagement or performance data. With no attendance, no exam performance, no graded assignments, and no subject-level grades recorded, there is not enough evidence of active participation or academic progress.', '2026-08-16 15:43:05', NULL, NULL),
(21, 17, NULL, 'at_risk', 'Flagged at risk due to zero recorded attendance and exam average, along with no completed assignments or grades.', '2026-08-16 15:43:05', NULL, 'Not enough data yet'),
(22, 17, NULL, 'weak_subject', 'Core exam topics', '2026-08-16 15:43:05', NULL, NULL),
(23, 17, NULL, 'recommendation', 'Begin attending classes consistently. | Complete and submit upcoming assignments. | Meet with a teacher or advisor immediately.', '2026-08-16 15:43:05', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `announcements`
--

CREATE TABLE `announcements` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `body` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `announcements`
--

INSERT INTO `announcements` (`id`, `title`, `body`, `created_at`) VALUES
(1, 'Semester kickoff', 'Welcome back. Check your dashboard for new assignments and the midterm schedule.', '2026-08-16 11:16:35'),
(2, 'AI study tips are live', 'Open My Progress to see weak-subject tips generated from your latest exam analysis.', '2026-08-16 11:16:35');

-- --------------------------------------------------------

--
-- Table structure for table `assignments`
--

CREATE TABLE `assignments` (
  `id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `due_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assignments`
--

INSERT INTO `assignments` (`id`, `class_id`, `title`, `description`, `due_date`) VALUES
(1, 1, 'Introduction to Python — Problem Set 1', 'Complete the listed exercises and upload your write-up.', '2026-08-23 05:46:35'),
(2, 1, 'Introduction to Python — Reflection', 'Short reflection on this week\'s lectures.', '2026-08-13 05:46:35'),
(3, 2, 'Linear Algebra — Problem Set 1', 'Complete the listed exercises and upload your write-up.', '2026-08-23 05:46:35'),
(4, 2, 'Linear Algebra — Reflection', 'Short reflection on this week\'s lectures.', '2026-08-13 05:46:35'),
(5, 3, 'World History: 1900–Present — Problem Set 1', 'Complete the listed exercises and upload your write-up.', '2026-08-23 05:46:35'),
(6, 3, 'World History: 1900–Present — Reflection', 'Short reflection on this week\'s lectures.', '2026-08-13 05:46:35'),
(7, 4, 'Data Structures — Problem Set 1', 'Complete the listed exercises and upload your write-up.', '2026-08-23 05:46:35'),
(8, 4, 'Data Structures — Reflection', 'Short reflection on this week\'s lectures.', '2026-08-13 05:46:35'),
(9, 5, 'Statistics for Decision Making — Problem Set 1', 'Complete the listed exercises and upload your write-up.', '2026-08-23 05:46:35'),
(10, 5, 'Statistics for Decision Making — Reflection', 'Short reflection on this week\'s lectures.', '2026-08-13 05:46:35'),
(11, 4, 'Smoke Assignment', 'Write a short answer.', '2026-08-16 06:28:07'),
(12, 4, 'Smoke Assignment', 'Write a short answer.', '2026-08-16 07:02:06'),
(13, 4, 'Smoke Assignment', 'Write a short answer.', '2026-08-16 09:46:12'),
(14, 4, 'Smoke Assignment', 'Write a short answer.', '2026-08-16 09:46:58');

-- --------------------------------------------------------

--
-- Table structure for table `assignment_submissions`
--

CREATE TABLE `assignment_submissions` (
  `id` int(11) NOT NULL,
  `assignment_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `submitted_at` datetime NOT NULL DEFAULT current_timestamp(),
  `content` text NOT NULL,
  `grade` float DEFAULT NULL,
  `feedback` text DEFAULT NULL,
  `ai_feedback` text DEFAULT NULL,
  `file_path` varchar(500) DEFAULT NULL,
  `original_filename` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assignment_submissions`
--

INSERT INTO `assignment_submissions` (`id`, `assignment_id`, `student_id`, `submitted_at`, `content`, `grade`, `feedback`, `ai_feedback`, `file_path`, `original_filename`) VALUES
(1, 1, 5, '2026-08-16 11:16:35', 'Submission from Rohan Sharma for Introduction to Python — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(2, 1, 6, '2026-08-16 11:16:35', 'Submission from Ananya Iyer for Introduction to Python — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(3, 1, 8, '2026-08-16 11:16:35', 'Submission from Meera Joshi for Introduction to Python — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(4, 2, 5, '2026-08-16 11:16:35', 'Submission from Rohan Sharma for Introduction to Python — Reflection.', 78, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(5, 2, 6, '2026-08-16 11:16:35', 'Submission from Ananya Iyer for Introduction to Python — Reflection.', 82, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(6, 3, 5, '2026-08-16 11:16:35', 'Submission from Rohan Sharma for Linear Algebra — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(7, 3, 7, '2026-08-16 11:16:35', 'Submission from Vikram Patel for Linear Algebra — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(8, 3, 8, '2026-08-16 11:16:35', 'Submission from Meera Joshi for Linear Algebra — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(9, 4, 5, '2026-08-16 11:16:35', 'Submission from Rohan Sharma for Linear Algebra — Reflection.', 78, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(10, 4, 7, '2026-08-16 11:16:35', 'Submission from Vikram Patel for Linear Algebra — Reflection.', 82, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(11, 5, 6, '2026-08-16 11:16:35', 'Submission from Ananya Iyer for World History: 1900–Present — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(12, 5, 8, '2026-08-16 11:16:35', 'Submission from Meera Joshi for World History: 1900–Present — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(13, 5, 9, '2026-08-16 11:16:35', 'Submission from Sahil Khan for World History: 1900–Present — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(14, 6, 6, '2026-08-16 11:16:35', 'Submission from Ananya Iyer for World History: 1900–Present — Reflection.', 78, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(15, 6, 8, '2026-08-16 11:16:35', 'Submission from Meera Joshi for World History: 1900–Present — Reflection.', 82, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(16, 7, 5, '2026-08-16 11:16:35', 'Submission from Rohan Sharma for Data Structures — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(17, 7, 7, '2026-08-16 11:16:35', 'Submission from Vikram Patel for Data Structures — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(18, 7, 9, '2026-08-16 11:16:35', 'Submission from Sahil Khan for Data Structures — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(19, 8, 5, '2026-08-16 11:16:35', 'Submission from Rohan Sharma for Data Structures — Reflection.', 78, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(20, 8, 7, '2026-08-16 11:16:35', 'Submission from Vikram Patel for Data Structures — Reflection.', 82, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(21, 9, 6, '2026-08-16 11:16:35', 'Submission from Ananya Iyer for Statistics for Decision Making — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(22, 9, 7, '2026-08-16 11:16:35', 'Submission from Vikram Patel for Statistics for Decision Making — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(23, 9, 9, '2026-08-16 11:16:35', 'Submission from Sahil Khan for Statistics for Decision Making — Problem Set 1.', NULL, NULL, NULL, NULL, NULL),
(24, 10, 6, '2026-08-16 11:16:35', 'Submission from Ananya Iyer for Statistics for Decision Making — Reflection.', 78, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(25, 10, 7, '2026-08-16 11:16:35', 'Submission from Vikram Patel for Statistics for Decision Making — Reflection.', 82, 'Solid effort; review the last section.', 'Clear structure. Strengthen examples in the conclusion.', NULL, NULL),
(26, 11, 5, '2026-08-16 11:58:07', 'My smoke submission.', 88, 'Good work', NULL, NULL, NULL),
(27, 12, 5, '2026-08-16 12:32:06', 'My smoke submission.', 88, 'Good work', 'Nice effort on this assignment—your response meets the basic expectations and shows that you completed the task. To make your short answers even stronger next time, try adding a specific detail or example so your thinking feels more developed. Keep it up; with a little more depth, your work can become even more polished.', NULL, NULL),
(28, 13, 5, '2026-08-16 15:16:12', 'My smoke submission.', 88, 'Good work', 'Your submission is concise and meets the basic requirement, which aligns well with the solid score you earned. To make it even stronger next time, try adding a little more detail or explanation so your answer shows deeper thought and fully demonstrates your understanding.', NULL, NULL),
(29, 14, 5, '2026-08-16 15:16:58', 'My smoke submission.', 88, 'Good work', 'Nice job completing the assignment and earning a solid grade. Your submission shows that you participated, and to make future short answers stronger, try adding a bit more detail or explanation so your thinking is easier to see. Keep building on this work by aiming for one or two specific supporting ideas in each response.', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `assistant_messages`
--

CREATE TABLE `assistant_messages` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `role` varchar(16) NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assistant_messages`
--

INSERT INTO `assistant_messages` (`id`, `student_id`, `role`, `content`, `created_at`) VALUES
(1, 5, 'user', 'What should I study first given my grades?', '2026-08-16 15:15:00'),
(2, 5, 'assistant', 'Start with **Introduction to Python and Linear Algebra**, where your midterm scores were 62% and checkpoint scores were 58%. Prioritize Linear Algebra proof writing and applied word problems, then practice Python fundamentals using checkpoint- and midterm-style questions. After that, review minor mistakes in core Data Structures concepts; Statistics is a lower priority given your 79% checkpoint score.', '2026-08-16 15:15:00'),
(3, 5, 'user', 'What should I study first given my grades?', '2026-08-16 15:17:57'),
(4, 5, 'assistant', 'Study **Linear Algebra first**, focusing on proof writing and applied word problems, since your checkpoint was 58% and midterm was 62%. Next, review **Introduction to Python** checkpoint topics and practice **Data Structures**, especially core-concept mistakes and quiz questions. Keep Statistics as a lower priority because your checkpoint score was stronger at 79%.', '2026-08-16 15:17:57');

-- --------------------------------------------------------

--
-- Table structure for table `assistant_rate_hits`
--

CREATE TABLE `assistant_rate_hits` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `assistant_rate_hits`
--

INSERT INTO `assistant_rate_hits` (`id`, `student_id`, `created_at`) VALUES
(1, 5, '2026-08-16 09:44:52'),
(2, 5, '2026-08-16 09:47:52');

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `status` enum('present','absent','late') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `student_id`, `class_id`, `date`, `status`) VALUES
(1, 5, 1, '2026-08-15', 'absent'),
(2, 6, 1, '2026-08-15', 'present'),
(3, 8, 1, '2026-08-15', 'present'),
(4, 5, 1, '2026-08-14', 'present'),
(5, 6, 1, '2026-08-14', 'present'),
(6, 8, 1, '2026-08-14', 'present'),
(7, 5, 1, '2026-08-13', 'present'),
(8, 6, 1, '2026-08-13', 'late'),
(9, 8, 1, '2026-08-13', 'present'),
(10, 5, 1, '2026-08-12', 'present'),
(11, 6, 1, '2026-08-12', 'present'),
(12, 8, 1, '2026-08-12', 'present'),
(13, 5, 1, '2026-08-11', 'present'),
(14, 6, 1, '2026-08-11', 'present'),
(15, 8, 1, '2026-08-11', 'present'),
(16, 5, 2, '2026-08-15', 'absent'),
(17, 7, 2, '2026-08-15', 'present'),
(18, 8, 2, '2026-08-15', 'present'),
(19, 5, 2, '2026-08-14', 'present'),
(20, 7, 2, '2026-08-14', 'present'),
(21, 8, 2, '2026-08-14', 'present'),
(22, 5, 2, '2026-08-13', 'present'),
(23, 7, 2, '2026-08-13', 'late'),
(24, 8, 2, '2026-08-13', 'present'),
(25, 5, 2, '2026-08-12', 'present'),
(26, 7, 2, '2026-08-12', 'present'),
(27, 8, 2, '2026-08-12', 'present'),
(28, 5, 2, '2026-08-11', 'present'),
(29, 7, 2, '2026-08-11', 'present'),
(30, 8, 2, '2026-08-11', 'present'),
(31, 6, 3, '2026-08-15', 'absent'),
(32, 8, 3, '2026-08-15', 'present'),
(33, 9, 3, '2026-08-15', 'present'),
(34, 6, 3, '2026-08-14', 'present'),
(35, 8, 3, '2026-08-14', 'present'),
(36, 9, 3, '2026-08-14', 'present'),
(37, 6, 3, '2026-08-13', 'present'),
(38, 8, 3, '2026-08-13', 'late'),
(39, 9, 3, '2026-08-13', 'present'),
(40, 6, 3, '2026-08-12', 'present'),
(41, 8, 3, '2026-08-12', 'present'),
(42, 9, 3, '2026-08-12', 'present'),
(43, 6, 3, '2026-08-11', 'present'),
(44, 8, 3, '2026-08-11', 'present'),
(45, 9, 3, '2026-08-11', 'present'),
(46, 5, 4, '2026-08-15', 'absent'),
(47, 7, 4, '2026-08-15', 'present'),
(48, 9, 4, '2026-08-15', 'present'),
(49, 5, 4, '2026-08-14', 'present'),
(50, 7, 4, '2026-08-14', 'present'),
(51, 9, 4, '2026-08-14', 'present'),
(52, 5, 4, '2026-08-13', 'present'),
(53, 7, 4, '2026-08-13', 'late'),
(54, 9, 4, '2026-08-13', 'present'),
(55, 5, 4, '2026-08-12', 'present'),
(56, 7, 4, '2026-08-12', 'present'),
(57, 9, 4, '2026-08-12', 'present'),
(58, 5, 4, '2026-08-11', 'present'),
(59, 7, 4, '2026-08-11', 'present'),
(60, 9, 4, '2026-08-11', 'present'),
(61, 6, 5, '2026-08-15', 'absent'),
(62, 7, 5, '2026-08-15', 'present'),
(63, 9, 5, '2026-08-15', 'present'),
(64, 6, 5, '2026-08-14', 'present'),
(65, 7, 5, '2026-08-14', 'present'),
(66, 9, 5, '2026-08-14', 'present'),
(67, 6, 5, '2026-08-13', 'present'),
(68, 7, 5, '2026-08-13', 'late'),
(69, 9, 5, '2026-08-13', 'present'),
(70, 6, 5, '2026-08-12', 'present'),
(71, 7, 5, '2026-08-12', 'present'),
(72, 9, 5, '2026-08-12', 'present'),
(73, 6, 5, '2026-08-11', 'present'),
(74, 7, 5, '2026-08-11', 'present'),
(75, 9, 5, '2026-08-11', 'present'),
(76, 5, 4, '2026-08-16', 'present'),
(77, 9, 4, '2026-08-16', 'present'),
(78, 7, 4, '2026-08-16', 'present'),
(79, 6, 1, '2026-08-16', 'present'),
(80, 8, 1, '2026-08-16', 'present'),
(81, 5, 1, '2026-08-16', 'present'),
(82, 5, 1, '2026-08-10', 'present'),
(83, 5, 1, '2026-08-09', 'present'),
(84, 5, 1, '2026-08-08', 'late'),
(85, 5, 1, '2026-08-07', 'present'),
(86, 5, 1, '2026-08-06', 'present'),
(87, 5, 1, '2026-08-05', 'present'),
(88, 5, 1, '2026-08-04', 'present'),
(89, 5, 1, '2026-08-03', 'present'),
(90, 5, 1, '2026-08-02', 'present'),
(91, 5, 1, '2026-08-01', 'present'),
(92, 5, 1, '2026-07-31', 'late'),
(93, 5, 1, '2026-07-30', 'present'),
(94, 5, 1, '2026-07-29', 'present'),
(95, 5, 1, '2026-07-28', 'present'),
(96, 5, 1, '2026-07-27', 'present'),
(97, 5, 1, '2026-07-26', 'present'),
(98, 5, 1, '2026-07-25', 'present'),
(99, 5, 1, '2026-07-24', 'present'),
(100, 5, 1, '2026-07-23', 'late'),
(101, 5, 1, '2026-07-22', 'present'),
(102, 5, 1, '2026-07-21', 'present'),
(103, 5, 1, '2026-07-20', 'present'),
(104, 5, 1, '2026-07-19', 'present'),
(105, 5, 2, '2026-08-10', 'present'),
(106, 5, 2, '2026-08-09', 'present'),
(107, 5, 2, '2026-08-08', 'late'),
(108, 5, 2, '2026-08-07', 'present'),
(109, 5, 2, '2026-08-06', 'present'),
(110, 5, 2, '2026-08-05', 'present'),
(111, 5, 2, '2026-08-04', 'present'),
(112, 5, 2, '2026-08-03', 'present'),
(113, 5, 2, '2026-08-02', 'present'),
(114, 5, 2, '2026-08-01', 'present'),
(115, 5, 2, '2026-07-31', 'late'),
(116, 5, 2, '2026-07-30', 'present'),
(117, 5, 2, '2026-07-29', 'present'),
(118, 5, 2, '2026-07-28', 'present'),
(119, 5, 2, '2026-07-27', 'present'),
(120, 5, 2, '2026-07-26', 'present'),
(121, 5, 2, '2026-07-25', 'present'),
(122, 5, 2, '2026-07-24', 'present'),
(123, 5, 2, '2026-07-23', 'late'),
(124, 5, 2, '2026-07-22', 'present'),
(125, 5, 2, '2026-07-21', 'present'),
(126, 5, 2, '2026-07-20', 'present'),
(127, 5, 2, '2026-07-19', 'present'),
(128, 5, 4, '2026-08-10', 'present'),
(129, 5, 4, '2026-08-09', 'present'),
(130, 5, 4, '2026-08-08', 'late'),
(131, 5, 4, '2026-08-07', 'present'),
(132, 5, 4, '2026-08-06', 'present'),
(133, 5, 4, '2026-08-05', 'present'),
(134, 5, 4, '2026-08-04', 'present'),
(135, 5, 4, '2026-08-03', 'present'),
(136, 5, 4, '2026-08-02', 'present'),
(137, 5, 4, '2026-08-01', 'present'),
(138, 5, 4, '2026-07-31', 'late'),
(139, 5, 4, '2026-07-30', 'present'),
(140, 5, 4, '2026-07-29', 'present'),
(141, 5, 4, '2026-07-28', 'present'),
(142, 5, 4, '2026-07-27', 'present'),
(143, 5, 4, '2026-07-26', 'present'),
(144, 5, 4, '2026-07-25', 'present'),
(145, 5, 4, '2026-07-24', 'present'),
(146, 5, 4, '2026-07-23', 'late'),
(147, 5, 4, '2026-07-22', 'present'),
(148, 5, 4, '2026-07-21', 'present'),
(149, 5, 4, '2026-07-20', 'present'),
(150, 5, 4, '2026-07-19', 'present'),
(151, 6, 1, '2026-08-10', 'present'),
(152, 6, 1, '2026-08-09', 'present'),
(153, 6, 1, '2026-08-08', 'late'),
(154, 6, 1, '2026-08-07', 'present'),
(155, 6, 1, '2026-08-06', 'present'),
(156, 6, 1, '2026-08-05', 'absent'),
(157, 6, 1, '2026-08-04', 'present'),
(158, 6, 1, '2026-08-03', 'present'),
(159, 6, 1, '2026-08-02', 'present'),
(160, 6, 1, '2026-08-01', 'present'),
(161, 6, 1, '2026-07-31', 'late'),
(162, 6, 1, '2026-07-30', 'present'),
(163, 6, 1, '2026-07-29', 'present'),
(164, 6, 1, '2026-07-28', 'present'),
(165, 6, 1, '2026-07-27', 'present'),
(166, 6, 1, '2026-07-26', 'present'),
(167, 6, 1, '2026-07-25', 'absent'),
(168, 6, 1, '2026-07-24', 'present'),
(169, 6, 1, '2026-07-23', 'late'),
(170, 6, 1, '2026-07-22', 'present'),
(171, 6, 1, '2026-07-21', 'present'),
(172, 6, 1, '2026-07-20', 'present'),
(173, 6, 1, '2026-07-19', 'present'),
(174, 6, 3, '2026-08-10', 'present'),
(175, 6, 3, '2026-08-09', 'present'),
(176, 6, 3, '2026-08-08', 'late'),
(177, 6, 3, '2026-08-07', 'present'),
(178, 6, 3, '2026-08-06', 'present'),
(179, 6, 3, '2026-08-05', 'absent'),
(180, 6, 3, '2026-08-04', 'present'),
(181, 6, 3, '2026-08-03', 'present'),
(182, 6, 3, '2026-08-02', 'present'),
(183, 6, 3, '2026-08-01', 'present'),
(184, 6, 3, '2026-07-31', 'late'),
(185, 6, 3, '2026-07-30', 'present'),
(186, 6, 3, '2026-07-29', 'present'),
(187, 6, 3, '2026-07-28', 'present'),
(188, 6, 3, '2026-07-27', 'present'),
(189, 6, 3, '2026-07-26', 'present'),
(190, 6, 3, '2026-07-25', 'absent'),
(191, 6, 3, '2026-07-24', 'present'),
(192, 6, 3, '2026-07-23', 'late'),
(193, 6, 3, '2026-07-22', 'present'),
(194, 6, 3, '2026-07-21', 'present'),
(195, 6, 3, '2026-07-20', 'present'),
(196, 6, 3, '2026-07-19', 'present'),
(197, 6, 5, '2026-08-10', 'present'),
(198, 6, 5, '2026-08-09', 'present'),
(199, 6, 5, '2026-08-08', 'late'),
(200, 6, 5, '2026-08-07', 'present'),
(201, 6, 5, '2026-08-06', 'present'),
(202, 6, 5, '2026-08-05', 'absent'),
(203, 6, 5, '2026-08-04', 'present'),
(204, 6, 5, '2026-08-03', 'present'),
(205, 6, 5, '2026-08-02', 'present'),
(206, 6, 5, '2026-08-01', 'present'),
(207, 6, 5, '2026-07-31', 'late'),
(208, 6, 5, '2026-07-30', 'present'),
(209, 6, 5, '2026-07-29', 'present'),
(210, 6, 5, '2026-07-28', 'present'),
(211, 6, 5, '2026-07-27', 'present'),
(212, 6, 5, '2026-07-26', 'present'),
(213, 6, 5, '2026-07-25', 'absent'),
(214, 6, 5, '2026-07-24', 'present'),
(215, 6, 5, '2026-07-23', 'late'),
(216, 6, 5, '2026-07-22', 'present'),
(217, 6, 5, '2026-07-21', 'present'),
(218, 6, 5, '2026-07-20', 'present'),
(219, 6, 5, '2026-07-19', 'present'),
(220, 7, 2, '2026-08-10', 'present'),
(221, 7, 2, '2026-08-09', 'present'),
(222, 7, 2, '2026-08-08', 'late'),
(223, 7, 2, '2026-08-07', 'present'),
(224, 7, 2, '2026-08-06', 'present'),
(225, 7, 2, '2026-08-05', 'present'),
(226, 7, 2, '2026-08-04', 'present'),
(227, 7, 2, '2026-08-03', 'present'),
(228, 7, 2, '2026-08-02', 'present'),
(229, 7, 2, '2026-08-01', 'present'),
(230, 7, 2, '2026-07-31', 'late'),
(231, 7, 2, '2026-07-30', 'present'),
(232, 7, 2, '2026-07-29', 'present'),
(233, 7, 2, '2026-07-28', 'present'),
(234, 7, 2, '2026-07-27', 'present'),
(235, 7, 2, '2026-07-26', 'present'),
(236, 7, 2, '2026-07-25', 'present'),
(237, 7, 2, '2026-07-24', 'present'),
(238, 7, 2, '2026-07-23', 'late'),
(239, 7, 2, '2026-07-22', 'present'),
(240, 7, 2, '2026-07-21', 'present'),
(241, 7, 2, '2026-07-20', 'present'),
(242, 7, 2, '2026-07-19', 'present'),
(243, 7, 4, '2026-08-10', 'present'),
(244, 7, 4, '2026-08-09', 'present'),
(245, 7, 4, '2026-08-08', 'late'),
(246, 7, 4, '2026-08-07', 'present'),
(247, 7, 4, '2026-08-06', 'present'),
(248, 7, 4, '2026-08-05', 'present'),
(249, 7, 4, '2026-08-04', 'present'),
(250, 7, 4, '2026-08-03', 'present'),
(251, 7, 4, '2026-08-02', 'present'),
(252, 7, 4, '2026-08-01', 'present'),
(253, 7, 4, '2026-07-31', 'late'),
(254, 7, 4, '2026-07-30', 'present'),
(255, 7, 4, '2026-07-29', 'present'),
(256, 7, 4, '2026-07-28', 'present'),
(257, 7, 4, '2026-07-27', 'present'),
(258, 7, 4, '2026-07-26', 'present'),
(259, 7, 4, '2026-07-25', 'present'),
(260, 7, 4, '2026-07-24', 'present'),
(261, 7, 4, '2026-07-23', 'late'),
(262, 7, 4, '2026-07-22', 'present'),
(263, 7, 4, '2026-07-21', 'present'),
(264, 7, 4, '2026-07-20', 'present'),
(265, 7, 4, '2026-07-19', 'present'),
(266, 7, 5, '2026-08-10', 'present'),
(267, 7, 5, '2026-08-09', 'present'),
(268, 7, 5, '2026-08-08', 'late'),
(269, 7, 5, '2026-08-07', 'present'),
(270, 7, 5, '2026-08-06', 'present'),
(271, 7, 5, '2026-08-05', 'present'),
(272, 7, 5, '2026-08-04', 'present'),
(273, 7, 5, '2026-08-03', 'present'),
(274, 7, 5, '2026-08-02', 'present'),
(275, 7, 5, '2026-08-01', 'present'),
(276, 7, 5, '2026-07-31', 'late'),
(277, 7, 5, '2026-07-30', 'present'),
(278, 7, 5, '2026-07-29', 'present'),
(279, 7, 5, '2026-07-28', 'present'),
(280, 7, 5, '2026-07-27', 'present'),
(281, 7, 5, '2026-07-26', 'present'),
(282, 7, 5, '2026-07-25', 'present'),
(283, 7, 5, '2026-07-24', 'present'),
(284, 7, 5, '2026-07-23', 'late'),
(285, 7, 5, '2026-07-22', 'present'),
(286, 7, 5, '2026-07-21', 'present'),
(287, 7, 5, '2026-07-20', 'present'),
(288, 7, 5, '2026-07-19', 'present'),
(289, 8, 1, '2026-08-10', 'present'),
(290, 8, 1, '2026-08-09', 'present'),
(291, 8, 1, '2026-08-08', 'late'),
(292, 8, 1, '2026-08-07', 'present'),
(293, 8, 1, '2026-08-06', 'present'),
(294, 8, 1, '2026-08-05', 'absent'),
(295, 8, 1, '2026-08-04', 'present'),
(296, 8, 1, '2026-08-03', 'present'),
(297, 8, 1, '2026-08-02', 'present'),
(298, 8, 1, '2026-08-01', 'present'),
(299, 8, 1, '2026-07-31', 'late'),
(300, 8, 1, '2026-07-30', 'present'),
(301, 8, 1, '2026-07-29', 'present'),
(302, 8, 1, '2026-07-28', 'present'),
(303, 8, 1, '2026-07-27', 'present'),
(304, 8, 1, '2026-07-26', 'present'),
(305, 8, 1, '2026-07-25', 'absent'),
(306, 8, 1, '2026-07-24', 'present'),
(307, 8, 1, '2026-07-23', 'late'),
(308, 8, 1, '2026-07-22', 'present'),
(309, 8, 1, '2026-07-21', 'present'),
(310, 8, 1, '2026-07-20', 'present'),
(311, 8, 1, '2026-07-19', 'present'),
(312, 8, 2, '2026-08-10', 'present'),
(313, 8, 2, '2026-08-09', 'present'),
(314, 8, 2, '2026-08-08', 'late'),
(315, 8, 2, '2026-08-07', 'present'),
(316, 8, 2, '2026-08-06', 'present'),
(317, 8, 2, '2026-08-05', 'absent'),
(318, 8, 2, '2026-08-04', 'present'),
(319, 8, 2, '2026-08-03', 'present'),
(320, 8, 2, '2026-08-02', 'present'),
(321, 8, 2, '2026-08-01', 'present'),
(322, 8, 2, '2026-07-31', 'late'),
(323, 8, 2, '2026-07-30', 'present'),
(324, 8, 2, '2026-07-29', 'present'),
(325, 8, 2, '2026-07-28', 'present'),
(326, 8, 2, '2026-07-27', 'present'),
(327, 8, 2, '2026-07-26', 'present'),
(328, 8, 2, '2026-07-25', 'absent'),
(329, 8, 2, '2026-07-24', 'present'),
(330, 8, 2, '2026-07-23', 'late'),
(331, 8, 2, '2026-07-22', 'present'),
(332, 8, 2, '2026-07-21', 'present'),
(333, 8, 2, '2026-07-20', 'present'),
(334, 8, 2, '2026-07-19', 'present'),
(335, 8, 3, '2026-08-10', 'present'),
(336, 8, 3, '2026-08-09', 'present'),
(337, 8, 3, '2026-08-08', 'late'),
(338, 8, 3, '2026-08-07', 'present'),
(339, 8, 3, '2026-08-06', 'present'),
(340, 8, 3, '2026-08-05', 'absent'),
(341, 8, 3, '2026-08-04', 'present'),
(342, 8, 3, '2026-08-03', 'present'),
(343, 8, 3, '2026-08-02', 'present'),
(344, 8, 3, '2026-08-01', 'present'),
(345, 8, 3, '2026-07-31', 'late'),
(346, 8, 3, '2026-07-30', 'present'),
(347, 8, 3, '2026-07-29', 'present'),
(348, 8, 3, '2026-07-28', 'present'),
(349, 8, 3, '2026-07-27', 'present'),
(350, 8, 3, '2026-07-26', 'present'),
(351, 8, 3, '2026-07-25', 'absent'),
(352, 8, 3, '2026-07-24', 'present'),
(353, 8, 3, '2026-07-23', 'late'),
(354, 8, 3, '2026-07-22', 'present'),
(355, 8, 3, '2026-07-21', 'present'),
(356, 8, 3, '2026-07-20', 'present'),
(357, 8, 3, '2026-07-19', 'present'),
(358, 9, 3, '2026-08-10', 'present'),
(359, 9, 3, '2026-08-09', 'present'),
(360, 9, 3, '2026-08-08', 'late'),
(361, 9, 3, '2026-08-07', 'present'),
(362, 9, 3, '2026-08-06', 'present'),
(363, 9, 3, '2026-08-05', 'present'),
(364, 9, 3, '2026-08-04', 'present'),
(365, 9, 3, '2026-08-03', 'present'),
(366, 9, 3, '2026-08-02', 'present'),
(367, 9, 3, '2026-08-01', 'present'),
(368, 9, 3, '2026-07-31', 'late'),
(369, 9, 3, '2026-07-30', 'present'),
(370, 9, 3, '2026-07-29', 'present'),
(371, 9, 3, '2026-07-28', 'present'),
(372, 9, 3, '2026-07-27', 'present'),
(373, 9, 3, '2026-07-26', 'present'),
(374, 9, 3, '2026-07-25', 'present'),
(375, 9, 3, '2026-07-24', 'present'),
(376, 9, 3, '2026-07-23', 'late'),
(377, 9, 3, '2026-07-22', 'present'),
(378, 9, 3, '2026-07-21', 'present'),
(379, 9, 3, '2026-07-20', 'present'),
(380, 9, 3, '2026-07-19', 'present'),
(381, 9, 4, '2026-08-10', 'present'),
(382, 9, 4, '2026-08-09', 'present'),
(383, 9, 4, '2026-08-08', 'late'),
(384, 9, 4, '2026-08-07', 'present'),
(385, 9, 4, '2026-08-06', 'present'),
(386, 9, 4, '2026-08-05', 'present'),
(387, 9, 4, '2026-08-04', 'present'),
(388, 9, 4, '2026-08-03', 'present'),
(389, 9, 4, '2026-08-02', 'present'),
(390, 9, 4, '2026-08-01', 'present'),
(391, 9, 4, '2026-07-31', 'late'),
(392, 9, 4, '2026-07-30', 'present'),
(393, 9, 4, '2026-07-29', 'present'),
(394, 9, 4, '2026-07-28', 'present'),
(395, 9, 4, '2026-07-27', 'present'),
(396, 9, 4, '2026-07-26', 'present'),
(397, 9, 4, '2026-07-25', 'present'),
(398, 9, 4, '2026-07-24', 'present'),
(399, 9, 4, '2026-07-23', 'late'),
(400, 9, 4, '2026-07-22', 'present'),
(401, 9, 4, '2026-07-21', 'present'),
(402, 9, 4, '2026-07-20', 'present'),
(403, 9, 4, '2026-07-19', 'present'),
(404, 9, 5, '2026-08-10', 'present'),
(405, 9, 5, '2026-08-09', 'present'),
(406, 9, 5, '2026-08-08', 'late'),
(407, 9, 5, '2026-08-07', 'present'),
(408, 9, 5, '2026-08-06', 'present'),
(409, 9, 5, '2026-08-05', 'present'),
(410, 9, 5, '2026-08-04', 'present'),
(411, 9, 5, '2026-08-03', 'present'),
(412, 9, 5, '2026-08-02', 'present'),
(413, 9, 5, '2026-08-01', 'present'),
(414, 9, 5, '2026-07-31', 'late'),
(415, 9, 5, '2026-07-30', 'present'),
(416, 9, 5, '2026-07-29', 'present'),
(417, 9, 5, '2026-07-28', 'present'),
(418, 9, 5, '2026-07-27', 'present'),
(419, 9, 5, '2026-07-26', 'present'),
(420, 9, 5, '2026-07-25', 'present'),
(421, 9, 5, '2026-07-24', 'present'),
(422, 9, 5, '2026-07-23', 'late'),
(423, 9, 5, '2026-07-22', 'present'),
(424, 9, 5, '2026-07-21', 'present'),
(425, 9, 5, '2026-07-20', 'present'),
(426, 9, 5, '2026-07-19', 'present'),
(427, 5, 5, '2026-08-15', 'present'),
(428, 5, 5, '2026-08-14', 'present'),
(429, 5, 5, '2026-08-13', 'present'),
(430, 5, 5, '2026-08-12', 'present'),
(431, 5, 5, '2026-08-11', 'present'),
(432, 5, 5, '2026-08-10', 'present'),
(433, 5, 5, '2026-08-09', 'present'),
(434, 5, 5, '2026-08-08', 'late'),
(435, 5, 5, '2026-08-07', 'present'),
(436, 5, 5, '2026-08-06', 'present'),
(437, 5, 5, '2026-08-05', 'present'),
(438, 5, 5, '2026-08-04', 'present'),
(439, 5, 5, '2026-08-03', 'present'),
(440, 5, 5, '2026-08-02', 'present'),
(441, 5, 5, '2026-08-01', 'present'),
(442, 5, 5, '2026-07-31', 'late'),
(443, 5, 5, '2026-07-30', 'present'),
(444, 5, 5, '2026-07-29', 'present'),
(445, 5, 5, '2026-07-28', 'present'),
(446, 5, 5, '2026-07-27', 'present'),
(447, 5, 5, '2026-07-26', 'present'),
(448, 5, 5, '2026-07-25', 'present'),
(449, 5, 5, '2026-07-24', 'present'),
(450, 5, 5, '2026-07-23', 'late'),
(451, 5, 5, '2026-07-22', 'present'),
(452, 5, 5, '2026-07-21', 'present'),
(453, 5, 5, '2026-07-20', 'present'),
(454, 5, 5, '2026-07-19', 'present');

-- --------------------------------------------------------

--
-- Table structure for table `classes`
--

CREATE TABLE `classes` (
  `id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`id`, `course_id`, `name`) VALUES
(1, 1, 'CS101-A'),
(2, 2, 'MATH201-B'),
(3, 3, 'HIST110-A'),
(4, 4, 'CS201-A'),
(5, 5, 'STAT101-A');

-- --------------------------------------------------------

--
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `email` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `email`, `message`, `created_at`) VALUES
(1, 'Parent Visitor', 'parent@example.com', 'Could you share office hours for Linear Algebra?', '2026-08-16 11:16:35'),
(2, 'Smoke Visitor', 'visitor@example.com', 'This is a smoke-test contact message.', '2026-08-16 11:50:51'),
(3, 'Smoke Visitor', 'visitor@example.com', 'This is a smoke-test contact message.', '2026-08-16 15:13:55'),
(4, 'Smoke Visitor', 'visitor@example.com', 'This is a smoke-test contact message.', '2026-08-16 15:16:04'),
(5, 'Ram', 'rsamy2426@gmail.com', 'Hibjbkbkjj', '2026-08-16 16:37:13');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `category` varchar(80) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `schedule` varchar(255) NOT NULL,
  `rating` float NOT NULL,
  `syllabus` text NOT NULL,
  `school_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `title`, `description`, `category`, `teacher_id`, `schedule`, `rating`, `syllabus`, `school_id`) VALUES
(1, 'Introduction to Python', 'Write programs, work with data, and build small apps in Python.', 'Computer Science', 2, 'Mon / Wed 10:00–11:30', 4.8, '1. Syntax\n2. Data structures\n3. Functions\n4. Files\n5. Mini project', 1),
(2, 'Linear Algebra', 'Vectors, matrices, and linear transformations for STEM majors.', 'Mathematics', 3, 'Tue / Thu 09:00–10:30', 4.6, '1. Vectors\n2. Matrices\n3. Determinants\n4. Eigenvalues\n5. Applications', 1),
(3, 'World History: 1900–Present', 'Political, social, and economic change across the twentieth century.', 'Humanities', 4, 'Fri 13:00–16:00', 4.4, '1. World wars\n2. Cold War\n3. Decolonization\n4. Globalization', 1),
(4, 'Data Structures', 'Arrays, trees, graphs, and complexity analysis.', 'Computer Science', 2, 'Mon / Wed 14:00–15:30', 4.7, '1. Arrays & lists\n2. Stacks & queues\n3. Trees\n4. Graphs\n5. Hashing', 1),
(5, 'Statistics for Decision Making', 'Descriptive stats, probability, and inference for real datasets.', 'Mathematics', 3, 'Tue / Thu 11:00–12:30', 4.3, '1. Descriptive stats\n2. Probability\n3. Sampling\n4. Hypothesis tests', 1);

-- --------------------------------------------------------

--
-- Table structure for table `enrollments`
--

CREATE TABLE `enrollments` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `enrolled_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `enrollments`
--

INSERT INTO `enrollments` (`id`, `student_id`, `course_id`, `enrolled_at`) VALUES
(1, 5, 1, '2026-08-16 11:16:35'),
(2, 5, 2, '2026-08-16 11:16:35'),
(3, 5, 4, '2026-08-16 11:16:35'),
(4, 6, 1, '2026-08-16 11:16:35'),
(5, 6, 3, '2026-08-16 11:16:35'),
(6, 6, 5, '2026-08-16 11:16:35'),
(7, 7, 2, '2026-08-16 11:16:35'),
(8, 7, 4, '2026-08-16 11:16:35'),
(9, 7, 5, '2026-08-16 11:16:35'),
(10, 8, 1, '2026-08-16 11:16:35'),
(11, 8, 2, '2026-08-16 11:16:35'),
(12, 8, 3, '2026-08-16 11:16:35'),
(13, 9, 3, '2026-08-16 11:16:35'),
(14, 9, 4, '2026-08-16 11:16:35'),
(15, 9, 5, '2026-08-16 11:16:35'),
(19, 5, 5, '2026-08-16 12:37:10');

-- --------------------------------------------------------

--
-- Table structure for table `exams`
--

CREATE TABLE `exams` (
  `id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `title` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `max_marks` float NOT NULL,
  `questions_json` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `exams`
--

INSERT INTO `exams` (`id`, `class_id`, `title`, `date`, `max_marks`, `questions_json`) VALUES
(1, 1, 'Introduction to Python Midterm', '2026-08-06', 100, '[{\"prompt\": \"Which Python type is mutable?\", \"options\": [\"tuple\", \"str\", \"list\", \"int\"], \"correct\": 2}, {\"prompt\": \"What does `len({1, 1, 2})` return?\", \"options\": [\"3\", \"2\", \"1\", \"It raises TypeError\"], \"correct\": 1}, {\"prompt\": \"The best way to open a text file for reading is:\", \"options\": [\"open(path, \'w\')\", \"with open(path, encoding=\'utf-8\') as handle:\", \"file = path.read()\", \"eval(path)\"], \"correct\": 1}, {\"prompt\": \"A function should return a value when you need to:\", \"options\": [\"Print a message only\", \"Reuse the result in later code\", \"Crash the program\", \"Skip the next line\"], \"correct\": 1}]'),
(2, 2, 'Linear Algebra Midterm', '2026-08-06', 100, '[{\"prompt\": \"A 2\\u00d73 matrix times a 3\\u00d71 vector yields a:\", \"options\": [\"3\\u00d72 matrix\", \"2\\u00d71 vector\", \"3\\u00d73 matrix\", \"scalar only\"], \"correct\": 1}, {\"prompt\": \"The determinant of a 2\\u00d72 matrix [[a, b], [c, d]] is:\", \"options\": [\"a + d\", \"ad \\u2212 bc\", \"ab \\u2212 cd\", \"ac + bd\"], \"correct\": 1}, {\"prompt\": \"Eigenvectors of A satisfy:\", \"options\": [\"Av = 0 only\", \"Av = \\u03bbv for some scalar \\u03bb\", \"A = v\\u03bb\", \"v must be the zero vector\"], \"correct\": 1}, {\"prompt\": \"Two vectors are orthogonal when their dot product is:\", \"options\": [\"1\", \"\\u22121\", \"0\", \"undefined\"], \"correct\": 2}]'),
(3, 3, 'World History: 1900–Present Midterm', '2026-08-06', 100, '[{\"prompt\": \"World War I ended in:\", \"options\": [\"1914\", \"1918\", \"1939\", \"1945\"], \"correct\": 1}, {\"prompt\": \"The Cold War is best described as:\", \"options\": [\"A direct US\\u2013USSR land war in Europe\", \"A long rivalry short of full-scale war between blocs\", \"The alliance that defeated Napoleon\", \"A trade pact limited to East Asia\"], \"correct\": 1}, {\"prompt\": \"Decolonization after 1945 mainly meant:\", \"options\": [\"European empires expanding in Africa\", \"Colonies gaining independence from imperial powers\", \"The end of all nation-states\", \"A return to medieval kingdoms\"], \"correct\": 1}, {\"prompt\": \"Late-20th-century globalization is associated with:\", \"options\": [\"Closed national markets only\", \"Faster trade, capital, and information flows\", \"The invention of agriculture\", \"The fall of the Roman Empire\"], \"correct\": 1}]'),
(4, 4, 'Data Structures Midterm', '2026-08-06', 100, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(5, 5, 'Statistics for Decision Making Midterm', '2026-08-06', 100, '[{\"prompt\": \"The median is:\", \"options\": [\"The most frequent value\", \"The middle value of ordered data\", \"The sum of values divided by n\", \"Always equal to the mean\"], \"correct\": 1}, {\"prompt\": \"A p-value is:\", \"options\": [\"The probability the null is true\", \"The chance of data at least this extreme if the null is true\", \"The sample size\", \"The confidence interval width\"], \"correct\": 1}, {\"prompt\": \"A larger random sample usually:\", \"options\": [\"Increases sampling error\", \"Reduces sampling error\", \"Removes all bias\", \"Makes the mean undefined\"], \"correct\": 1}, {\"prompt\": \"A histogram is most useful for:\", \"options\": [\"Showing the shape of a numeric distribution\", \"Listing every raw row\", \"Replacing a hypothesis test\", \"Computing a p-value directly\"], \"correct\": 0}]'),
(6, 4, 'Smoke Exam', '2026-08-16', 50, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(7, 4, 'Smoke Exam', '2026-08-16', 50, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(8, 1, 'Introduction to Python Checkpoint', '2026-07-27', 100, '[{\"prompt\": \"Which Python type is mutable?\", \"options\": [\"tuple\", \"str\", \"list\", \"int\"], \"correct\": 2}, {\"prompt\": \"What does `len({1, 1, 2})` return?\", \"options\": [\"3\", \"2\", \"1\", \"It raises TypeError\"], \"correct\": 1}, {\"prompt\": \"The best way to open a text file for reading is:\", \"options\": [\"open(path, \'w\')\", \"with open(path, encoding=\'utf-8\') as handle:\", \"file = path.read()\", \"eval(path)\"], \"correct\": 1}, {\"prompt\": \"A function should return a value when you need to:\", \"options\": [\"Print a message only\", \"Reuse the result in later code\", \"Crash the program\", \"Skip the next line\"], \"correct\": 1}]'),
(9, 2, 'Linear Algebra Checkpoint', '2026-07-27', 100, '[{\"prompt\": \"A 2\\u00d73 matrix times a 3\\u00d71 vector yields a:\", \"options\": [\"3\\u00d72 matrix\", \"2\\u00d71 vector\", \"3\\u00d73 matrix\", \"scalar only\"], \"correct\": 1}, {\"prompt\": \"The determinant of a 2\\u00d72 matrix [[a, b], [c, d]] is:\", \"options\": [\"a + d\", \"ad \\u2212 bc\", \"ab \\u2212 cd\", \"ac + bd\"], \"correct\": 1}, {\"prompt\": \"Eigenvectors of A satisfy:\", \"options\": [\"Av = 0 only\", \"Av = \\u03bbv for some scalar \\u03bb\", \"A = v\\u03bb\", \"v must be the zero vector\"], \"correct\": 1}, {\"prompt\": \"Two vectors are orthogonal when their dot product is:\", \"options\": [\"1\", \"\\u22121\", \"0\", \"undefined\"], \"correct\": 2}]'),
(10, 3, 'World History: 1900–Present Checkpoint', '2026-07-27', 100, '[{\"prompt\": \"World War I ended in:\", \"options\": [\"1914\", \"1918\", \"1939\", \"1945\"], \"correct\": 1}, {\"prompt\": \"The Cold War is best described as:\", \"options\": [\"A direct US\\u2013USSR land war in Europe\", \"A long rivalry short of full-scale war between blocs\", \"The alliance that defeated Napoleon\", \"A trade pact limited to East Asia\"], \"correct\": 1}, {\"prompt\": \"Decolonization after 1945 mainly meant:\", \"options\": [\"European empires expanding in Africa\", \"Colonies gaining independence from imperial powers\", \"The end of all nation-states\", \"A return to medieval kingdoms\"], \"correct\": 1}, {\"prompt\": \"Late-20th-century globalization is associated with:\", \"options\": [\"Closed national markets only\", \"Faster trade, capital, and information flows\", \"The invention of agriculture\", \"The fall of the Roman Empire\"], \"correct\": 1}]'),
(11, 4, 'Data Structures Checkpoint', '2026-07-27', 100, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(12, 5, 'Statistics for Decision Making Checkpoint', '2026-07-27', 100, '[{\"prompt\": \"The median is:\", \"options\": [\"The most frequent value\", \"The middle value of ordered data\", \"The sum of values divided by n\", \"Always equal to the mean\"], \"correct\": 1}, {\"prompt\": \"A p-value is:\", \"options\": [\"The probability the null is true\", \"The chance of data at least this extreme if the null is true\", \"The sample size\", \"The confidence interval width\"], \"correct\": 1}, {\"prompt\": \"A larger random sample usually:\", \"options\": [\"Increases sampling error\", \"Reduces sampling error\", \"Removes all bias\", \"Makes the mean undefined\"], \"correct\": 1}, {\"prompt\": \"A histogram is most useful for:\", \"options\": [\"Showing the shape of a numeric distribution\", \"Listing every raw row\", \"Replacing a hypothesis test\", \"Computing a p-value directly\"], \"correct\": 0}]'),
(13, 1, 'Introduction to Python Practice Quiz', '2026-08-16', 100, '[{\"prompt\": \"Which Python type is mutable?\", \"options\": [\"tuple\", \"str\", \"list\", \"int\"], \"correct\": 2}, {\"prompt\": \"What does `len({1, 1, 2})` return?\", \"options\": [\"3\", \"2\", \"1\", \"It raises TypeError\"], \"correct\": 1}, {\"prompt\": \"The best way to open a text file for reading is:\", \"options\": [\"open(path, \'w\')\", \"with open(path, encoding=\'utf-8\') as handle:\", \"file = path.read()\", \"eval(path)\"], \"correct\": 1}, {\"prompt\": \"A function should return a value when you need to:\", \"options\": [\"Print a message only\", \"Reuse the result in later code\", \"Crash the program\", \"Skip the next line\"], \"correct\": 1}]'),
(14, 2, 'Linear Algebra Practice Quiz', '2026-08-16', 100, '[{\"prompt\": \"A 2\\u00d73 matrix times a 3\\u00d71 vector yields a:\", \"options\": [\"3\\u00d72 matrix\", \"2\\u00d71 vector\", \"3\\u00d73 matrix\", \"scalar only\"], \"correct\": 1}, {\"prompt\": \"The determinant of a 2\\u00d72 matrix [[a, b], [c, d]] is:\", \"options\": [\"a + d\", \"ad \\u2212 bc\", \"ab \\u2212 cd\", \"ac + bd\"], \"correct\": 1}, {\"prompt\": \"Eigenvectors of A satisfy:\", \"options\": [\"Av = 0 only\", \"Av = \\u03bbv for some scalar \\u03bb\", \"A = v\\u03bb\", \"v must be the zero vector\"], \"correct\": 1}, {\"prompt\": \"Two vectors are orthogonal when their dot product is:\", \"options\": [\"1\", \"\\u22121\", \"0\", \"undefined\"], \"correct\": 2}]'),
(15, 3, 'World History: 1900–Present Practice Quiz', '2026-08-16', 100, '[{\"prompt\": \"World War I ended in:\", \"options\": [\"1914\", \"1918\", \"1939\", \"1945\"], \"correct\": 1}, {\"prompt\": \"The Cold War is best described as:\", \"options\": [\"A direct US\\u2013USSR land war in Europe\", \"A long rivalry short of full-scale war between blocs\", \"The alliance that defeated Napoleon\", \"A trade pact limited to East Asia\"], \"correct\": 1}, {\"prompt\": \"Decolonization after 1945 mainly meant:\", \"options\": [\"European empires expanding in Africa\", \"Colonies gaining independence from imperial powers\", \"The end of all nation-states\", \"A return to medieval kingdoms\"], \"correct\": 1}, {\"prompt\": \"Late-20th-century globalization is associated with:\", \"options\": [\"Closed national markets only\", \"Faster trade, capital, and information flows\", \"The invention of agriculture\", \"The fall of the Roman Empire\"], \"correct\": 1}]'),
(16, 4, 'Data Structures Practice Quiz', '2026-08-16', 100, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(17, 5, 'Statistics for Decision Making Practice Quiz', '2026-08-16', 100, '[{\"prompt\": \"The median is:\", \"options\": [\"The most frequent value\", \"The middle value of ordered data\", \"The sum of values divided by n\", \"Always equal to the mean\"], \"correct\": 1}, {\"prompt\": \"A p-value is:\", \"options\": [\"The probability the null is true\", \"The chance of data at least this extreme if the null is true\", \"The sample size\", \"The confidence interval width\"], \"correct\": 1}, {\"prompt\": \"A larger random sample usually:\", \"options\": [\"Increases sampling error\", \"Reduces sampling error\", \"Removes all bias\", \"Makes the mean undefined\"], \"correct\": 1}, {\"prompt\": \"A histogram is most useful for:\", \"options\": [\"Showing the shape of a numeric distribution\", \"Listing every raw row\", \"Replacing a hypothesis test\", \"Computing a p-value directly\"], \"correct\": 0}]'),
(18, 4, 'Smoke Exam', '2026-08-16', 50, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(19, 4, 'Live Quiz', '2026-08-16', 40, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(20, 4, 'Smoke Exam', '2026-08-16', 50, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]'),
(21, 4, 'Live Quiz', '2026-08-16', 40, '[{\"prompt\": \"Which structure is LIFO?\", \"options\": [\"Queue\", \"Stack\", \"Hash set\", \"B-tree\"], \"correct\": 1}, {\"prompt\": \"Average-case lookup in a well-sized hash table is:\", \"options\": [\"O(n)\", \"O(log n)\", \"O(1)\", \"O(n log n)\"], \"correct\": 2}, {\"prompt\": \"A binary search tree\\u2019s in-order traversal visits keys:\", \"options\": [\"In random order\", \"In sorted order\", \"Level by level only\", \"From the leaves first\"], \"correct\": 1}, {\"prompt\": \"BFS on an unweighted graph finds:\", \"options\": [\"A longest path\", \"A shortest path in number of edges\", \"The minimum spanning tree\", \"All topological sorts\"], \"correct\": 1}]');

-- --------------------------------------------------------

--
-- Table structure for table `exam_analysis`
--

CREATE TABLE `exam_analysis` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `ai_summary` text NOT NULL,
  `weak_topics` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `exam_analysis`
--

INSERT INTO `exam_analysis` (`id`, `student_id`, `exam_id`, `ai_summary`, `weak_topics`, `created_at`) VALUES
(1, 5, 1, 'Rohan Sharma scored 62/100 on Introduction to Python Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(2, 6, 1, 'Ananya Iyer scored 70/100 on Introduction to Python Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(3, 8, 1, 'Meera Joshi scored 78/100 on Introduction to Python Midterm.', 'Minor gaps in advanced applications', '2026-08-16 11:16:35'),
(4, 5, 2, 'Rohan Sharma scored 62/100 on Linear Algebra Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(5, 7, 2, 'Vikram Patel scored 70/100 on Linear Algebra Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(6, 8, 2, 'Meera Joshi scored 78/100 on Linear Algebra Midterm.', 'Minor gaps in advanced applications', '2026-08-16 11:16:35'),
(7, 6, 3, 'Ananya Iyer scored 62/100 on World History: 1900–Present Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(8, 8, 3, 'Meera Joshi scored 70/100 on World History: 1900–Present Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(9, 9, 3, 'Sahil Khan scored 78/100 on World History: 1900–Present Midterm.', 'Minor gaps in advanced applications', '2026-08-16 11:16:35'),
(10, 5, 4, 'Rohan Sharma scored 62/100 on Data Structures Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(11, 7, 4, 'Vikram Patel scored 70/100 on Data Structures Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(12, 9, 4, 'Sahil Khan scored 78/100 on Data Structures Midterm.', 'Minor gaps in advanced applications', '2026-08-16 11:16:35'),
(13, 6, 5, 'Ananya Iyer scored 62/100 on Statistics for Decision Making Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(14, 7, 5, 'Vikram Patel scored 70/100 on Statistics for Decision Making Midterm.', 'Proof writing; applied word problems', '2026-08-16 11:16:35'),
(15, 9, 5, 'Sahil Khan scored 78/100 on Statistics for Decision Making Midterm.', 'Minor gaps in advanced applications', '2026-08-16 11:16:35'),
(16, 5, 7, 'Rohan Sharma scored 41.0 out of 50.0 (82.0%), showing a strong overall performance in the Smoke Exam in Data Structures. The student appears to have a solid grasp of the core concepts, with some room for improvement to reach top accuracy.', 'Topic-level data not provided;Minor mistakes in core data structures concepts', '2026-08-16 12:32:21'),
(17, 5, 18, 'Rohan Sharma performed well on the Smoke Exam in Data Structures, scoring 41.0 out of 50.0 (82.0%). This indicates a strong overall grasp of the material, with some room for improvement to reach top performance. A topic-level breakdown was not provided, so weaknesses can only be identified at a general level.', 'Topic-level weaknesses not available;Review missed questions;Focus on higher-accuracy problem solving', '2026-08-16 15:16:25'),
(18, 5, 19, 'Rohan Sharma scored 20.0 out of 40.0 (50.0%). This indicates a moderate performance with clear room for improvement. Focus on revising core data structures concepts and practicing more quiz-style questions to strengthen accuracy and confidence.', 'Topic-level weaknesses not available from overall score alone', '2026-08-16 15:16:36'),
(19, 5, 20, 'Strong overall performance on the Smoke Exam in Data Structures with a score of 41.0/50.0 (82.0%). The student appears to have a good grasp of the material, but specific weak areas cannot be identified from the total score alone.', 'Insufficient topic-level data', '2026-08-16 15:17:10'),
(20, 5, 21, 'Scored 20.0 out of 40.0 (50.0%) in the Live Quiz in Data Structures. This indicates an average performance with clear room for improvement. More question-level detail is needed to identify precise concept gaps.', 'Insufficient data to identify specific weak topics', '2026-08-16 15:17:18'),
(21, 5, 16, 'Rohan Sharma scored 25.0/100.0 (25.0%) in the Data Structures Practice Quiz, indicating significant gaps in overall understanding and a need for focused revision of core concepts.', 'data structures fundamentals; overall concept clarity; topic-level breakdown unavailable', '2026-08-16 15:56:09');

-- --------------------------------------------------------

--
-- Table structure for table `exam_attempts`
--

CREATE TABLE `exam_attempts` (
  `id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `answers_json` text NOT NULL,
  `score` float NOT NULL,
  `submitted_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `exam_attempts`
--

INSERT INTO `exam_attempts` (`id`, `exam_id`, `student_id`, `answers_json`, `score`, `submitted_at`) VALUES
(1, 19, 5, '[1, 1, 1, 1]', 20, '2026-08-16 15:16:25'),
(2, 21, 5, '[1, 1, 1, 1]', 20, '2026-08-16 15:17:10'),
(3, 16, 5, '[0, 1, 1, 1]', 25, '2026-08-16 15:56:03');

-- --------------------------------------------------------

--
-- Table structure for table `faqs`
--

CREATE TABLE `faqs` (
  `id` int(11) NOT NULL,
  `question` varchar(255) NOT NULL,
  `answer` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `faqs`
--

INSERT INTO `faqs` (`id`, `question`, `answer`) VALUES
(1, 'How do I enroll in a course?', 'Open Course Details and use Enroll Now. You must be logged in as a student.'),
(2, 'Who can mark attendance?', 'Teachers mark attendance for classes they own. Students can view their own records.'),
(3, 'Where do AI recommendations come from?', 'The AI Engine uses attendance, assignments, exams, and grades to generate insights.'),
(4, 'How do I contact support?', 'Use the Contact form on the Contact page. An admin will follow up by email.');

-- --------------------------------------------------------

--
-- Table structure for table `grades`
--

CREATE TABLE `grades` (
  `id` int(11) NOT NULL,
  `exam_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `marks_obtained` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `grades`
--

INSERT INTO `grades` (`id`, `exam_id`, `student_id`, `marks_obtained`) VALUES
(1, 1, 5, 62),
(2, 1, 6, 70),
(3, 1, 8, 78),
(4, 2, 5, 62),
(5, 2, 7, 70),
(6, 2, 8, 78),
(7, 3, 6, 62),
(8, 3, 8, 70),
(9, 3, 9, 78),
(10, 4, 5, 62),
(11, 4, 7, 70),
(12, 4, 9, 78),
(13, 5, 6, 62),
(14, 5, 7, 70),
(15, 5, 9, 78),
(16, 6, 5, 41),
(17, 7, 5, 41),
(18, 8, 5, 58),
(19, 8, 6, 65),
(20, 8, 8, 72),
(21, 9, 5, 58),
(22, 9, 7, 65),
(23, 9, 8, 72),
(24, 10, 6, 58),
(25, 10, 8, 65),
(26, 10, 9, 72),
(27, 11, 5, 58),
(28, 11, 7, 65),
(29, 11, 9, 72),
(30, 12, 6, 58),
(31, 12, 7, 65),
(32, 12, 9, 72),
(33, 12, 5, 79),
(34, 18, 5, 41),
(35, 19, 5, 20),
(36, 20, 5, 41),
(37, 21, 5, 20),
(38, 16, 5, 25);

-- --------------------------------------------------------

--
-- Table structure for table `practice_question_sets`
--

CREATE TABLE `practice_question_sets` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `subject` varchar(300) NOT NULL,
  `questions_json` text NOT NULL,
  `source` varchar(32) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `practice_question_sets`
--

INSERT INTO `practice_question_sets` (`id`, `student_id`, `subject`, `questions_json`, `source`, `created_at`) VALUES
(1, 5, 'Linear Algebra', '[\"Let A and B be n\\u00d7n matrices. Prove that if A and B are invertible, then AB is invertible.\", \"A factory uses two machines to make two products. Write a system of linear equations to model the total hours and total output, then solve for how many hours each machine ran.\", \"Prove that if vectors v1, v2, and v3 are linearly dependent, then one of them can be written as a linear combination of the other two.\", \"A mixture problem leads to the equations x + y = 10 and 2x + 5y = 31. Interpret what x and y could represent in a real situation, then solve the system.\"]', 'model', '2026-08-16 09:47:52');

-- --------------------------------------------------------

--
-- Table structure for table `schools`
--

CREATE TABLE `schools` (
  `id` int(11) NOT NULL,
  `name` varchar(160) NOT NULL,
  `slug` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `schools`
--

INSERT INTO `schools` (`id`, `name`, `slug`) VALUES
(1, 'KIT Campus', 'kit-campus'),
(2, 'Riverside Academy', 'riverside');

-- --------------------------------------------------------

--
-- Table structure for table `study_tips`
--

CREATE TABLE `study_tips` (
  `id` int(11) NOT NULL,
  `content` text NOT NULL,
  `source` varchar(32) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `study_tips`
--

INSERT INTO `study_tips` (`id`, `content`, `source`, `created_at`) VALUES
(26, 'Plan your week every Sunday by listing assignments, exams, and study blocks in one calendar.', 'model', '2026-08-16 10:46:30'),
(27, 'Break large tasks into 25-minute focus sessions and take a 5-minute break between them.', 'model', '2026-08-16 10:46:30'),
(28, 'Study with active recall by closing your notes and testing yourself on key ideas from memory.', 'model', '2026-08-16 10:46:30'),
(29, 'Keep your phone on silent and out of reach while you study to reduce interruptions.', 'model', '2026-08-16 10:46:30'),
(30, 'End each study session by writing the next small step so it is easier to start again later.', 'model', '2026-08-16 10:46:30');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(120) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('student','teacher','admin') NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  `school_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `created_at`, `is_active`, `school_id`) VALUES
(1, 'Asha Menon', 'admin@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'admin', '2026-08-16 11:16:35', 1, 1),
(2, 'Dr. Priya Nair', 'priya.nair@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'teacher', '2026-08-16 11:16:35', 1, 1),
(3, 'Prof. Arjun Mehta', 'arjun.mehta@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'teacher', '2026-08-16 11:16:35', 1, 1),
(4, 'Ms. Kavya Reddy', 'kavya.reddy@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'teacher', '2026-08-16 11:16:35', 1, 1),
(5, 'Rohan Sharma', 'rohan.sharma@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'student', '2026-08-16 11:16:35', 1, 1),
(6, 'Ananya Iyer', 'ananya.iyer@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'student', '2026-08-16 11:16:35', 1, 1),
(7, 'Vikram Patel', 'vikram.patel@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'student', '2026-08-16 11:16:35', 1, 1),
(8, 'Meera Joshi', 'meera.joshi@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'student', '2026-08-16 11:16:35', 1, 1),
(9, 'Sahil Khan', 'sahil.khan@edu.example.com', '$2b$12$nArLsL6PlyX1/CNrUD76JuWo9npW3jbV.5zCEp99URRddxeqWj24C', 'student', '2026-08-16 11:16:35', 1, 1),
(10, 'Temp Student', 'temp.student@edu.example.com', '$2b$12$NYnelGvGOtEeojFM9jZXOuXPYXj2JY5mB8sh.FqNfyVl4Y6Ap4ibC', 'student', '2026-08-16 12:05:56', 1, 1),
(11, 'Temp Student', 'temp.student.9f25b592@edu.example.com', '$2b$12$qoCMcwCszuOjdOnnCAEWzuzmHrQHxd28NoTJ4gUVM44gbiVbYIJi6', 'student', '2026-08-16 12:32:50', 1, 1),
(12, 'Temp Student', 'temp.student.1430f79d@edu.example.com', '$2b$12$qnuim2Krw2.Fv6YWEqokne51F8sewxN1Fog5aaj7.jAh7vI1wa8dq', 'student', '2026-08-16 12:55:57', 1, 1),
(13, 'Temp Student', 'temp.student.20b9c07b@edu.example.com', '$2b$12$R2CNbLIPttB47jb7qgT9VubM84fTG7aheswXMcY5MaVTK0JhYkggy', 'student', '2026-08-16 13:37:00', 1, 1),
(14, 'Verify Smoke', 'verify.smoke.c048cc7f78@edu.example.com', '$2b$12$ll1xNR.MPB.SOlPvKc9Ueep8PskAfBFO3cjpn7VcSPDGGj69LqHkS', 'student', '2026-08-16 15:16:08', 1, 1),
(15, 'Temp Student', 'temp.student.c5c022e5@edu.example.com', '$2b$12$9JHJUM6OoO7iSrjOeSE1fOKHJMJ98cIPBiUD5.lWnKe5sS/VRJIyC', 'student', '2026-08-16 15:17:22', 1, 1),
(16, 'Register Smoke', 'register.smoke.5ea4140d53@edu.example.com', '$2b$12$f0w7nSzXjevC/wcmDevJge8pIxW2yXOqoR/3kJjAkVVBHDHX87zGG', 'student', '2026-08-16 15:32:23', 1, 1),
(17, 'Ram', 'rsamy2426@gmail.com', '$2b$12$//ggGNIr9o9WDOEFwfOYtez1JUGwTNFvrs/ygp6TEyj0/zGaslucO', 'student', '2026-08-16 15:42:54', 1, 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ai_insights`
--
ALTER TABLE `ai_insights`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_ai_insights_class_id` (`class_id`),
  ADD KEY `ix_ai_insights_student_id` (`student_id`),
  ADD KEY `ix_ai_insights_type` (`type`);

--
-- Indexes for table `announcements`
--
ALTER TABLE `announcements`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `assignments`
--
ALTER TABLE `assignments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_assignments_class_id` (`class_id`);

--
-- Indexes for table `assignment_submissions`
--
ALTER TABLE `assignment_submissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_assignment_submissions_assignment_id` (`assignment_id`),
  ADD KEY `ix_assignment_submissions_student_id` (`student_id`);

--
-- Indexes for table `assistant_messages`
--
ALTER TABLE `assistant_messages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_assistant_messages_student_id` (`student_id`);

--
-- Indexes for table `assistant_rate_hits`
--
ALTER TABLE `assistant_rate_hits`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_assistant_rate_hits_created_at` (`created_at`),
  ADD KEY `ix_assistant_rate_hits_student_id` (`student_id`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_attendance_student_class_date` (`student_id`,`class_id`,`date`),
  ADD KEY `ix_attendance_student_id` (`student_id`),
  ADD KEY `ix_attendance_class_id` (`class_id`);

--
-- Indexes for table `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_classes_course_id` (`course_id`);

--
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_courses_category` (`category`),
  ADD KEY `ix_courses_teacher_id` (`teacher_id`);

--
-- Indexes for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_enrollment_student_course` (`student_id`,`course_id`),
  ADD KEY `ix_enrollments_course_id` (`course_id`),
  ADD KEY `ix_enrollments_student_id` (`student_id`);

--
-- Indexes for table `exams`
--
ALTER TABLE `exams`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_exams_class_id` (`class_id`);

--
-- Indexes for table `exam_analysis`
--
ALTER TABLE `exam_analysis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_exam_analysis_exam_id` (`exam_id`),
  ADD KEY `ix_exam_analysis_student_id` (`student_id`);

--
-- Indexes for table `exam_attempts`
--
ALTER TABLE `exam_attempts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_exam_attempt_student` (`exam_id`,`student_id`),
  ADD KEY `ix_exam_attempts_exam_id` (`exam_id`),
  ADD KEY `ix_exam_attempts_student_id` (`student_id`);

--
-- Indexes for table `faqs`
--
ALTER TABLE `faqs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `grades`
--
ALTER TABLE `grades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_grades_exam_id` (`exam_id`),
  ADD KEY `ix_grades_student_id` (`student_id`);

--
-- Indexes for table `practice_question_sets`
--
ALTER TABLE `practice_question_sets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_practice_student_subject` (`student_id`,`subject`),
  ADD KEY `ix_practice_question_sets_student_id` (`student_id`);

--
-- Indexes for table `schools`
--
ALTER TABLE `schools`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_schools_slug` (`slug`);

--
-- Indexes for table `study_tips`
--
ALTER TABLE `study_tips`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD KEY `ix_users_role` (`role`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ai_insights`
--
ALTER TABLE `ai_insights`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT for table `announcements`
--
ALTER TABLE `announcements`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `assignments`
--
ALTER TABLE `assignments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `assignment_submissions`
--
ALTER TABLE `assignment_submissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `assistant_messages`
--
ALTER TABLE `assistant_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `assistant_rate_hits`
--
ALTER TABLE `assistant_rate_hits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=455;

--
-- AUTO_INCREMENT for table `classes`
--
ALTER TABLE `classes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `courses`
--
ALTER TABLE `courses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `enrollments`
--
ALTER TABLE `enrollments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `exams`
--
ALTER TABLE `exams`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `exam_analysis`
--
ALTER TABLE `exam_analysis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `exam_attempts`
--
ALTER TABLE `exam_attempts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `faqs`
--
ALTER TABLE `faqs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `grades`
--
ALTER TABLE `grades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `practice_question_sets`
--
ALTER TABLE `practice_question_sets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `schools`
--
ALTER TABLE `schools`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `study_tips`
--
ALTER TABLE `study_tips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ai_insights`
--
ALTER TABLE `ai_insights`
  ADD CONSTRAINT `ai_insights_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `ai_insights_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Constraints for table `assignments`
--
ALTER TABLE `assignments`
  ADD CONSTRAINT `assignments_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Constraints for table `assignment_submissions`
--
ALTER TABLE `assignment_submissions`
  ADD CONSTRAINT `assignment_submissions_ibfk_1` FOREIGN KEY (`assignment_id`) REFERENCES `assignments` (`id`),
  ADD CONSTRAINT `assignment_submissions_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `assistant_messages`
--
ALTER TABLE `assistant_messages`
  ADD CONSTRAINT `assistant_messages_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `assistant_rate_hits`
--
ALTER TABLE `assistant_rate_hits`
  ADD CONSTRAINT `assistant_rate_hits_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Constraints for table `classes`
--
ALTER TABLE `classes`
  ADD CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`);

--
-- Constraints for table `exams`
--
ALTER TABLE `exams`
  ADD CONSTRAINT `exams_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Constraints for table `exam_analysis`
--
ALTER TABLE `exam_analysis`
  ADD CONSTRAINT `exam_analysis_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `exam_analysis_ibfk_2` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`);

--
-- Constraints for table `exam_attempts`
--
ALTER TABLE `exam_attempts`
  ADD CONSTRAINT `exam_attempts_ibfk_1` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  ADD CONSTRAINT `exam_attempts_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `grades`
--
ALTER TABLE `grades`
  ADD CONSTRAINT `grades_ibfk_1` FOREIGN KEY (`exam_id`) REFERENCES `exams` (`id`),
  ADD CONSTRAINT `grades_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `practice_question_sets`
--
ALTER TABLE `practice_question_sets`
  ADD CONSTRAINT `practice_question_sets_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
