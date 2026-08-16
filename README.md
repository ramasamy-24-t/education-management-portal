# Education Management Portal

A full-stack education management system. Public course pages, academic workflows (attendance, assignments, exams), role-based dashboards for students, teachers, and admins, and an AI engine powered by Azure AI Foundry for performance insights, at-risk detection, study recommendations, practice questions, and a study assistant.

The architecture diagram is the source of truth. Every box is implemented and wired: public pages do not require login; course details enroll into the academic flow; dashboards send learning data into the AI Engine; My Progress, Reports, and Admin all open the shared Performance Reports & Summary.

**Stack:** React 18 + Tailwind CSS (Vite) · FastAPI · SQLAlchemy · MySQL (XAMPP) · Azure AI Foundry Model Router

## User interface

The interface is a **simple, easy-to-use UI**. Screens use clear headings, short labels, and the same layout on every page so students, teachers, and admins can move around without training. Public pages, dashboards, and admin tools share one navigation bar.

It is built to be **accessible**: semantic HTML, labeled form fields, keyboard-friendly controls, visible focus outlines, a skip-to-content link, and `lang="en"` on the document. Contrast stays readable on a light background. The study assistant is announced to screen readers. Print and PDF reports keep the same information as the on-screen summary.

---

## Quick Start (from zero)

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL (XAMPP recommended) running on localhost:3306
- Azure AI Foundry account (the portal also runs with local AI fallbacks if Azure is not configured)

### 1. Clone and configure

```bash
git clone <repo-url>
cd "8 Hours Hackathon"
git config core.hooksPath hooks
```

### 2. Backend setup

Create a virtual environment named `venv` or `.venv`, then activate it. Examples below use `venv` (Windows).

```bash
cd backend
python -m venv venv
venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with MySQL credentials and Azure AI keys
python seed.py
uvicorn app.main:app --reload --port 8000
```

Install packages into the same virtualenv that uvicorn uses.

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Vite proxies `/api` to `http://127.0.0.1:8000`, so the browser only talks to port 5173.

### 4. Access the app

| What | URL |
| --- | --- |
| App | http://localhost:5173 |
| API docs (Swagger) | http://127.0.0.1:8000/docs |
| Health | http://127.0.0.1:8000/health |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

### Demo logins (password: `password123`)

Either domain works. Accounts are stored as `@edu.example.com`; login also accepts `@edu.local`.

| Role | Email |
| --- | --- |
| Admin | `admin@edu.example.com` or `admin@edu.local` |
| Teacher | `priya.nair@edu.example.com` or `priya.nair@edu.local` |
| Student | `rohan.sharma@edu.example.com` or `rohan.sharma@edu.local` |

Register as a student or teacher from **Login / Register**. Pick a school (KIT Campus or Riverside Academy). Registration signs you in immediately and opens the dashboard.

**Admin Login** is a separate screen (`/admin/login`) and only accepts the admin role.

### Demo notes (judges)

Log in as `rohan.sharma@edu.example.com`, open **My Progress**, and click the **black robot button** (bottom right). That is the Study Assistant. Ask “Why is my attendance flagged?” or “What should I study first?” Then generate practice questions on a weak subject, download the PDF on **Reports**, and open **Admin → AI Insights** to see risk trend.

---

## How the diagram is wired

| Diagram box | Route / UI | Backend |
| --- | --- | --- |
| Home Page | `/` · `frontend/src/pages/Home.jsx` | `/announcements`, `/courses/top-rated`, `/teachers/top`, `/ai/study-tips` |
| Courses Page | `/courses` · `Courses.jsx` | `/courses`, `/courses/categories`, `/courses/top-rated` |
| Course Details | `/courses/:courseId` · `CourseDetails.jsx` | `/courses/{id}`, `/courses/{id}/classes`, `POST /enrollments` |
| Contact Page | `/contact` · `Contact.jsx` | `/contact/info`, `/faqs`, `POST /contact` |
| User Login / Register | `/login` · `LoginRegister.jsx` | `POST /auth/login`, `POST /auth/register`, `GET /schools` |
| User Dashboard | `/dashboard` · `UserDashboard.jsx` + student/teacher dashboards | `GET /users/me/dashboard` |
| My Progress | `/progress` · `MyProgress.jsx` | `GET /users/me/progress-overview`, `POST /ai/refresh`, practice questions |
| Attendance | `/attendance` · `Attendance.jsx` | `/attendance/mark`, `/attendance`, `/attendance/summary` |
| Assignments | `/assignments` · `Assignments.jsx` | `/assignments`, submissions + file download |
| Exams & Grades | `/exams` · `Exams.jsx` | `/exams`, `/exams/{id}/paper`, `/exams/{id}/attempts`, grades |
| AI Engine | Azure + `app/services/ai_engine.py` | `/ai/*` |
| Reports & Insights | `/reports` · `PerformanceReports.jsx` | `/reports/me`, class, comparative, admin summary, PDF |
| Admin Login | `/admin/login` · `AdminLogin.jsx` | `POST /auth/admin/login` |
| Admin Dashboard | `/admin` · `AdminDashboard.jsx` | `/admin/users`, `/ai/monitoring`, links into academic + reports |

**Learning data → AI Engine:** the student dashboard and My Progress load attendance, assignments, exams, and grades. `dashboard.student_progress` calls `ai_engine.list_student_insight_texts(..., refresh=True)`, which writes `ai_insights` and returns weak subjects, tips, at-risk trend, and recommendations.

**Enroll / Access:** Course Details **Enroll now** creates an enrollment. After login, that course appears under My Courses and unlocks attendance, assignments, and exams for that class.

**Performance Reports & Summary** is reachable from login (after auth), My Progress, Reports in the nav, and the Admin Dashboard. Students download a PDF; teachers and admins print the page and can download a per-student PDF from the class table.

---

## Feature Overview

### Public Pages (no login)

- **Home:** Hero/banner, announcements, featured courses (catalog rating, not student reviews), top teachers, AI study tips (cached; Azure refresh is admin/teacher-only; local tips if Azure is down), CTA **Explore courses**
- **Courses:** Search, category filter, course listing, featured sidebar (same catalog rating)
- **Course Details:** Course info, syllabus, teacher info, schedule/classes, **Enroll now** (students; guests are sent to login and returned here)
- **Contact:** Contact info, contact form stored in the database, FAQ accordion, support email. Admins review messages on the Admin Dashboard (no outbound email).

### Academic Flow

- **Attendance:** Teachers and admins mark a class for a date. Students view their own records and a percent-present summary.
- **Assignments:** Teachers/admins create assignments with due dates. Students submit text and an optional file (PDF, PNG, JPG, TXT, DOC, DOCX, up to 5 MB). Teachers grade with feedback. **AI feedback** is written when a submission is graded.
- **Exams & Grades:** Students take a multiple-choice paper (`GET /exams/{id}/paper`, `POST /exams/{id}/attempts`). Teachers can also enter marks. Grade history and **exam analysis** (AI summary + weak topics) are stored with the grade.
- Seed data includes a **Practice Quiz** dated today so a student can take an exam during a demo.

### User Area (Student / Teacher)

- **Login / Register:** Account access, role selection (student or teacher), school selection. JWT is kept in `sessionStorage` and restored with `GET /auth/me` after refresh.
- **Student dashboard:** Profile, my courses, my assignments (submit from the dashboard), attendance, grades, AI recommendations, progress overview, shortcuts to academic pages and reports.
- **Teacher dashboard:** Profile, my classes, mark attendance, assignments, exams & marks, link to performance reports and manage courses.
- **My Progress:** Performance overview, at-risk trend (14-day vs prior 14-day), weak subjects with practice questions, improvement tips, AI insights. Study assistant is the floating robot on every student page.

### Admin Area

- **Admin Login:** Separate, admin-only credential check.
- **Admin Dashboard:** Manage students and teachers (create, deactivate), review contact-form messages, manage courses & classes, assignments, exams & grades, attendance, reports & analytics, **AI Insights & Monitoring** (refresh class insights, see risk trend on at-risk rows).

### AI Engine (Azure AI Foundry)

- **Performance analysis** from attendance + grades
- **At-risk student detection** when attendance is below 70% or exam average is below 60%, with a model explanation
- **Risk trend:** `improving` / `worsening` / `stable`, or “Not enough data yet”. Windows are `TREND_WINDOW_DAYS = 14` (recent `[today-14, today]`, prior `[today-28, today-14)`). Stored on the `at_risk` insight row.
- **Weak subject identification** from grade patterns
- **Study recommendations** per student
- **Class insights** for teachers and admins
- **AI study tips** on Home (`GET /ai/study-tips` reads cache; `POST /ai/study-tips/refresh` for teachers/admins)
- **Assignment AI feedback** and **exam analysis**
- **Practice questions** generated and stored per weak subject
- **Study assistant chat** persisted per student, rate-limited, scoped to that student’s academics
- Insights refresh when older than `INSIGHT_STALE_MINUTES` (default 10). Force refresh from My Progress or Admin monitoring.
- If Azure is unreachable, the engine writes local fallbacks so pages still load.

### Reports & Performance Summary

- **Student report:** academic summary, weak areas, risk analysis, AI recommendations, grade history, **Download PDF** and **Print**
- **Class report:** class averages, at-risk list, student table, per-student PDF download
- **Comparative report:** cross-class comparison and AI recommendations rollup
- **Admin insights summary:** insight counts and recent generated content

### Schools

Users and courses belong to a school (`school_id`). Registration requires a school. Logged-in students and teachers see courses for their school. Public course browse still lists the catalog.

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env`. Never commit `.env`.

| Variable | Purpose | Default |
| --- | --- | --- |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `root` |
| `DB_PASSWORD` | MySQL password | (empty) |
| `DB_NAME` | Database name | `education_portal` |
| `SECRET_KEY` | JWT signing secret | `dev-only-change-me` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `480` (8 hours) |
| `AZURE_AI_ENDPOINT` | Full Azure AI Foundry URL (`.../protocols/openai/responses`) | |
| `AZURE_AI_KEY` | Azure API key | |
| `AZURE_AI_MODEL` | Deployment name | `model-router` |
| `AZURE_AI_API_VERSION` | API version | `v1` |
| `AZURE_AI_TIMEOUT_SECONDS` | HTTP timeout to Azure | `20` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `PUBLIC_APP_URL` | Public frontend URL | `http://localhost:5173` |
| `INSIGHT_STALE_MINUTES` | Minutes before stored insights refresh | `10` |

---

## Azure AI Foundry Setup

1. Open [Azure AI Foundry](https://ai.azure.com) and your project
2. Deploy **Model Router** (or an agent that uses the OpenAI Responses protocol)
3. Put the full POST URL in `AZURE_AI_ENDPOINT` (example: `.../protocols/openai/responses`)
4. Put the key in `AZURE_AI_KEY`
5. Set `AZURE_AI_API_VERSION=v1` (or `2025-11-15-preview`)
6. Restart uvicorn after changing `.env`

The AI Engine always persists a useful result. Model failures use local fallbacks so Home tips, insights, feedback, practice questions, and the assistant stay available.

---

## API Endpoints

Interactive docs: http://127.0.0.1:8000/docs

### Health & public

| Method | Path | Access |
| --- | --- | --- |
| GET | `/health` | Public |
| GET | `/announcements` | Public |
| GET | `/faqs` | Public |
| GET | `/contact/info` | Public |
| POST | `/contact` | Public |
| GET | `/contact/messages` | Admin |
| GET | `/teachers/top` | Public |
| GET | `/schools` | Public |

### Authentication

| Method | Path | Access |
| --- | --- | --- |
| POST | `/auth/register` | Public (student/teacher; returns token and signs in) |
| POST | `/auth/login` | Public (student/teacher) |
| POST | `/auth/admin/login` | Public (admin only) |
| GET | `/auth/me` | Authenticated |
| POST | `/auth/logout` | Authenticated |

### Courses, classes, enrollments

| Method | Path | Access |
| --- | --- | --- |
| GET | `/courses`, `/courses/top-rated`, `/courses/categories` | Public |
| GET | `/courses/{id}` | Public (extra fields if logged in) |
| GET | `/courses/{id}/classes` | Public |
| POST | `/courses` | Teacher, Admin |
| PATCH / DELETE | `/courses/{id}` | Owner teacher, Admin |
| POST | `/courses/{id}/classes` | Owner teacher, Admin |
| POST | `/enrollments` | Student (self) |

### Academic

| Method | Path | Access |
| --- | --- | --- |
| GET | `/academic/classes` | Authenticated |
| GET | `/academic/classes/{id}/students` | Class members |
| POST | `/attendance/mark` | Owner teacher, Admin |
| GET | `/attendance`, `/attendance/summary` | Class members |
| POST | `/assignments` | Owner teacher, Admin |
| GET | `/assignments`, `/assignments/{id}` | Class members |
| POST | `/assignments/{id}/submissions` | Enrolled student (multipart: `content`, optional `file`) |
| GET | `/assignments/{id}/submissions` | Class members |
| GET | `/submissions/me` | Student |
| GET | `/submissions/{id}/file` | Owner student, teacher, admin |
| PATCH | `/submissions/{id}` | Owner teacher, Admin |
| POST | `/exams` | Owner teacher, Admin |
| GET | `/exams`, `/exams/{id}` | Class members |
| GET | `/exams/{id}/paper` | Student |
| POST | `/exams/{id}/attempts` | Student |
| PUT | `/exams/{id}/grades` | Owner teacher, Admin |
| GET | `/exams/{id}/grades` | Class members |
| GET | `/grades/me` | Student |

### Dashboards

| Method | Path | Access |
| --- | --- | --- |
| GET | `/users/me/dashboard` | Student, Teacher |
| GET | `/users/me/progress-overview` | Student |

### AI

| Method | Path | Access |
| --- | --- | --- |
| GET | `/ai/status` | Public |
| GET | `/ai/study-tips` | Public (cached read only) |
| POST | `/ai/study-tips/refresh` | Teacher, Admin |
| GET | `/ai/me` | Student |
| POST | `/ai/refresh` | Student |
| GET / POST | `/ai/practice-questions/{student_id}` | Student (self only) |
| GET / POST | `/ai/assistant/{student_id}` | Student (self only) |
| GET | `/ai/monitoring` | Teacher, Admin |
| POST | `/ai/monitoring/refresh` | Teacher, Admin |

### Reports

| Method | Path | Access |
| --- | --- | --- |
| GET | `/reports/me` | Student |
| GET | `/reports/me/pdf` | Student |
| GET | `/reports/student/{id}` | Teacher (own classes), Admin |
| GET | `/reports/student/{id}/pdf` | Teacher (own classes), Admin |
| GET | `/reports/class/{id}` | Teacher, Admin |
| GET | `/reports/comparative` | Teacher, Admin |
| GET | `/reports/admin/summary` | Admin |

### Admin

| Method | Path | Access |
| --- | --- | --- |
| GET | `/admin/users?role=` | Admin |
| POST | `/admin/users` | Admin |
| PATCH | `/admin/users/{id}` | Admin |

---

## Folder Structure

```
/
├── README.md
├── .gitignore
├── hooks/                      # Git hook: no Cursor co-author trailers
├── frontend/                   # Vite + React + Tailwind
│   └── src/
│       ├── App.jsx             # Routes (public, user, academic, admin, reports)
│       ├── api/client.js       # JSON, multipart, and file-download helpers
│       ├── context/            # Auth (sessionStorage JWT) + toasts
│       ├── pages/              # One page per diagram box
│       ├── dashboards/         # Student, teacher, admin panels
│       ├── components/         # Layout, cards, assistant, risk trend
│       └── data/studyTips.js   # Local Home tips if Azure is down
└── backend/
    ├── .env.example
    ├── requirements.txt
    ├── seed.py                 # Creates DB + demo users, courses, academic history
    ├── uploads/                # Assignment files (gitignored)
    ├── scripts/                # Smoke tests
    └── app/
        ├── main.py             # FastAPI app, CORS, routers, startup schema
        ├── config.py           # Settings from .env
        ├── constants.py        # Shared fallbacks (study tips, default exam questions)
        ├── database.py         # SQLAlchemy engine/session
        ├── db_bootstrap.py     # create_all + compatible ALTERs
        ├── deps.py             # JWT + role guards
        ├── routers/            # HTTP only
        ├── services/           # Business rules + AI + reports + uploads
        ├── models/             # SQLAlchemy tables
        └── schemas/            # Pydantic request/response models
```

---

## Code conventions 

Follow this layout so a new reader can find behavior without guessing.

1. **Routers stay thin.** Parse the request, check the role via `deps.py`, call a service, return a schema. Do not put SQL or Azure calls in routers.
2. **Services own rules.** Enrollment, ownership (`assert_can_manage_class`), file saves, insight generation, and PDF building live in `app/services/`.
3. **Models vs schemas.** Tables in `app/models/`. API shapes in `app/schemas/`. Serializers such as `exam_out` and `assignment_out` convert ORM rows to response models.
4. **Auth on every mutation.** Students act on their own enrollments and submissions. Teachers act on classes they own. Admins can manage all classes.
5. **AI is never a hard dependency.** `ai_engine.py` always stores a usable string; `ai_service.py` talks to Azure. Failures fall back locally.
6. **Frontend pages map to the diagram.** Public pages are unauthenticated. Academic pages use `ProtectedRoute`. `api()` is JSON; `apiForm()` is multipart (assignment files); `downloadFile()` is PDF/attachments.
7. **Secrets stay in `.env`.** Copy from `.env.example`. Do not commit keys.
8. **Schema changes.** Prefer SQLAlchemy models plus `ensure_schema()` in `db_bootstrap.py` so existing MySQL databases pick up new columns on startup. Application queries use the ORM.

Python package layout: `app` → `routers` (HTTP) → `services` (domain) → `models` (persistence).

---

## Diagram Coverage Checklist

### Public Pages (Main Navigation)

- [x] Home Page — Hero / Banner
- [x] Home Page — Announcements
- [x] Home Page — Featured Courses
- [x] Home Page — Top Teachers
- [x] Home Page — AI Study Tips (cached; Azure refresh from Admin; local fallback)
- [x] Home Page — CTA → Explore Courses
- [x] Courses Page — Search Courses
- [x] Courses Page — Filter
- [x] Courses Page — Categories
- [x] Courses Page — Course Listing
- [x] Courses Page — Featured Courses (catalog rating)
- [x] Course Details — Course Info
- [x] Course Details — Syllabus
- [x] Course Details — Teacher Info
- [x] Course Details — Schedule
- [x] Course Details — Enroll Now (bridges into Academic Flow)
- [x] Contact Page — Contact Info
- [x] Contact Page — Contact Form
- [x] Contact Page — FAQ
- [x] Contact Page — Support

### Academic Flow

- [x] Attendance — Mark Attendance
- [x] Attendance — View Attendance
- [x] Attendance — Attendance Summary
- [x] Assignments — Create / View
- [x] Assignments — Submit Assignments (text + optional file)
- [x] Assignments — Due Dates
- [x] Assignments — AI Feedback
- [x] Exams & Grades — Take Exams
- [x] Exams & Grades — View Grades
- [x] Exams & Grades — Grade History
- [x] Exams & Grades — Exam Analysis
- [x] AI Engine — Performance Analysis
- [x] AI Engine — At-Risk Student Detection
- [x] AI Engine — Weak Subject Identification
- [x] AI Engine — Study Recommendations
- [x] AI Engine — AI Insights & Reports
- [x] Reports & Insights — Student / Class / Comparative / AI recommendations

### User Area (Student / Teacher)

- [x] User Login / Register — Account Access
- [x] User Login / Register — Role Selection
- [x] User Dashboard — Profile
- [x] User Dashboard — My Courses
- [x] User Dashboard — My Assignments
- [x] User Dashboard — Attendance
- [x] User Dashboard — Grades
- [x] User Dashboard — AI Recommendations
- [x] User Dashboard — Progress Overview
- [x] My Progress — Performance Overview
- [x] My Progress — Weak Subjects
- [x] My Progress — Improvement Tips
- [x] My Progress — AI Insights
- [x] Learning Data (attendance, assignments, exams, grades) → AI Engine

### Admin Area

- [x] Admin Login — Secure Access
- [x] Admin Dashboard — Manage Students
- [x] Admin Dashboard — Manage Teachers
- [x] Admin Dashboard — Manage Courses & Classes
- [x] Admin Dashboard — Manage Assignments
- [x] Admin Dashboard — Manage Exams & Grades
- [x] Admin Dashboard — View Reports & Analytics
- [x] Admin Dashboard — AI Insights & Monitoring
- [x] Admin Dashboard — Contact messages (stored form submissions)

### Performance Reports & Summary

- [x] Academic Performance Summary
- [x] Weak Areas Identified
- [x] Risk Analysis
- [x] AI Recommendations
- [x] Download / Print Report
- [x] Fed from Login (after auth), My Progress, Reports & Insights, and Admin Dashboard

### Innovations( Add-ons )

| Add-on | What it does | Where |
| --- | --- | --- |
| **Risk Trend** | Compares two 14-day attendance/grade windows: improving / worsening / stable, or “not enough data yet”, with a one-line reason. | My Progress → At-risk trend. Admin/teacher: AI Insights & Monitoring. |
| **Practice Questions** | 3–4 questions for a weak subject from exam `weak_topics`. Latest set stored per subject. | My Progress → Weak subjects → Generate practice questions. |
| **Study Assistant Chat** | Q&A over that student’s own academics. History stored. Off-topic questions are redirected. | Black robot button, bottom right, on every student page. |

---

## Security

- Secrets live in `.env` (gitignored). `.env.example` has no real keys.
- CORS is the `CORS_ORIGINS` list.
- Mutating endpoints require a JWT plus role and ownership checks. Teachers can only open student reports for learners in their own classes. `GET /ai/study-tips` is a cache read.
- Application queries go through SQLAlchemy. Startup schema helpers in `db_bootstrap.py` may run compatibility `ALTER`s.
- Passwords are hashed with bcrypt.
- JWT access tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default 8 hours). The browser keeps the current tab session in `sessionStorage` (`emp.session`) so a refresh does not log you out.
- Assignment uploads are size- and type-checked and stored under `backend/uploads/`.
- The study assistant only sees that student’s attendance, grades, exam analysis, weak subjects, and assignment AI feedback.

---

## Credits

Built for an 8-hour hackathon. The architecture diagram is the source of truth for features and wiring.
