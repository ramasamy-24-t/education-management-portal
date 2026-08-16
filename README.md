# Education Management Portal

Hackathon project for students, teachers, and admins: public course pages, academic workflows (attendance, assignments, exams), role-based dashboards, and an AI engine that turns learning data into reports.

**Stack:** React + Tailwind (Vite) · FastAPI · SQLAlchemy · MySQL (XAMPP) · Azure AI Foundry Model Router (wired in later prompts)

## Folder structure

```
/
  README.md
  .gitignore
  frontend/          Vite + React + Tailwind + React Router
  backend/           FastAPI + SQLAlchemy models + seed script
    app/
      config.py
      database.py
      main.py
      models/        One module per domain (users, courses, academic, AI, …)
      routers/       HTTP routes (health only in this step)
      services/      Business logic (empty until later prompts)
    seed.py
    .env.example
```

## What this step added

- Full project scaffold (`frontend/`, `backend/`)
- Placeholder React routes for every top-level page in the architecture diagram
- SQLAlchemy models + MySQL tables for all entities implied by the diagram
- Seed data so dashboards have students, teachers, admin, courses, classes, attendance, assignments, exams, FAQs, announcements, and sample AI insights
- `.env` / `.env.example` for DB and secrets (`.env` is gitignored)

## Assumptions

- **Announcements** are stored in an `announcements` table (Home Page box) even though they were not in the original table list.
- **`courses.syllabus`** holds Course Details syllabus text.
- **Course `rating`** is a denormalized float used for Top Rated Courses. Top Teachers is the average rating of courses taught by that teacher (no separate teacher-rating table).
- **`schedule`** is a human-readable string (e.g. `Mon / Wed 10:00–11:30`).
- **Exam grades** live in `grades`; **assignment grades** live on `assignment_submissions`.
- **`ai_insights.student_id` / `class_id`** are nullable so class-level insights (Admin monitoring) do not require a student.
- Academic Flow screens (Attendance, Assignments, Exams & Grades) will be nested under User / Admin dashboards in later prompts; this step only registered the listed public/user/admin/report routes.
- Seed accounts all use password `password123` (local demo only).

## MySQL via XAMPP

1. Start **Apache** and **MySQL** in the XAMPP Control Panel.
2. Default local credentials are usually `root` with an empty password on `localhost:3306`.
3. You do **not** need to create the database by hand. `python seed.py` runs `CREATE DATABASE IF NOT EXISTS education_portal`.

To inspect tables later, open phpMyAdmin → `education_portal`.

## Environment variables

Copy `backend/.env.example` to `backend/.env` (already created locally) and set:

| Variable | Purpose |
| --- | --- |
| `DB_HOST` | MySQL host (default `localhost`) |
| `DB_PORT` | MySQL port (default `3306`) |
| `DB_USER` | MySQL user (default `root`) |
| `DB_PASSWORD` | MySQL password (often empty on XAMPP) |
| `DB_NAME` | Schema name (default `education_portal`) |
| `SECRET_KEY` | App secret for later JWT/auth |
| `AZURE_AI_ENDPOINT` | Azure AI Foundry Model Router URL (later prompts) |
| `AZURE_AI_API_KEY` | Azure key — never commit this |

## Run the backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

- API: http://127.0.0.1:8000
- Health: http://127.0.0.1:8000/health
- Docs: http://127.0.0.1:8000/docs

Demo logins after seed:

- Admin: `admin@edu.local`
- Teacher: `priya.nair@edu.local`
- Student: `rohan.sharma@edu.local`
- Password for all: `password123`

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173  
Vite proxies `/api` → `http://127.0.0.1:8000`.

## Placeholder routes

| Path | Diagram page |
| --- | --- |
| `/` | Home Page |
| `/courses` | Courses Page |
| `/courses/:courseId` | Course Details |
| `/contact` | Contact Page |
| `/login` | User Login / Register |
| `/dashboard` | User Dashboard |
| `/progress` | My Progress |
| `/admin/login` | Admin Login |
| `/admin` | Admin Dashboard |
| `/reports` | Performance Reports & Summary |

## Diagram coverage

Check off boxes as later prompts implement them (schema + placeholder routes only in this step).

### Public Pages (Main Navigation)

- [ ] Home Page — Hero / Banner
- [ ] Home Page — Announcements
- [ ] Home Page — Featured Courses
- [ ] Home Page — Top Teachers
- [ ] Home Page — AI Study Tips
- [ ] Home Page — CTA → Explore Courses
- [ ] Courses Page — Search Courses
- [ ] Courses Page — Filter
- [ ] Courses Page — Categories
- [ ] Courses Page — Course Listing
- [ ] Courses Page — Top Rated Courses
- [ ] Course Details — Course Info
- [ ] Course Details — Syllabus
- [ ] Course Details — Teacher Info
- [ ] Course Details — Schedule
- [ ] Course Details — Enroll Now
- [ ] Contact Page — Contact Info
- [ ] Contact Page — Contact Form
- [ ] Contact Page — FAQ
- [ ] Contact Page — Support

### Academic Flow

- [ ] Attendance — Mark Attendance
- [ ] Attendance — View Attendance
- [ ] Attendance — Attendance Summary
- [ ] Assignments — Create / View
- [ ] Assignments — Submit Assignments
- [ ] Assignments — Due Dates
- [ ] Assignments — AI Feedback
- [ ] Exams & Grades — Take Exams
- [ ] Exams & Grades — View Grades
- [ ] Exams & Grades — Grade History
- [ ] Exams & Grades — Exam Analysis

### User Area (Student / Teacher)

- [ ] User Login / Register — Account Access
- [ ] User Login / Register — Role Selection (Student / Teacher)
- [ ] User Dashboard — Profile
- [ ] User Dashboard — My Courses
- [ ] User Dashboard — My Assignments
- [ ] User Dashboard — Attendance
- [ ] User Dashboard — Grades
- [ ] User Dashboard — AI Recommendations
- [ ] User Dashboard — Progress Overview
- [ ] My Progress — Performance Overview
- [ ] My Progress — Weak Subjects
- [ ] My Progress — Improvement Tips
- [ ] My Progress — AI Insights

### Admin Area

- [ ] Admin Login — Secure Access
- [ ] Admin Dashboard — Manage Students
- [ ] Admin Dashboard — Manage Teachers
- [ ] Admin Dashboard — Manage Courses & Classes
- [ ] Admin Dashboard — Manage Assignments
- [ ] Admin Dashboard — Manage Exams & Grades
- [ ] Admin Dashboard — View Reports & Analytics
- [ ] Admin Dashboard — AI Insights & Monitoring

### AI Engine + Reports

- [ ] AI Engine — Performance Analysis
- [ ] AI Engine — At-Risk Student Detection
- [ ] AI Engine — Weak Subject Identification
- [ ] AI Engine — Study Recommendations
- [ ] AI Engine — AI Insights & Reports
- [ ] Reports & Insights — Student Performance
- [ ] Reports & Insights — Class Performance
- [ ] Reports & Insights — Comparative Reports
- [ ] Reports & Insights — AI Recommendations
- [ ] Performance Reports & Summary — Academic Performance Summary
- [ ] Performance Reports & Summary — Weak Areas Identified
- [ ] Performance Reports & Summary — Risk Analysis
- [ ] Performance Reports & Summary — AI Recommendations
- [ ] Performance Reports & Summary — Download / Print Report
