# Education Management Portal

A full-stack education management system built for an 8-hour hackathon. Features public course pages, academic workflows (attendance, assignments, exams), role-based dashboards for students/teachers/admins, and an AI engine powered by Azure AI Foundry that generates performance insights, at-risk detection, and personalized recommendations.

**Stack:** React 18 + Tailwind CSS (Vite) · FastAPI · SQLAlchemy · MySQL (XAMPP) · Azure AI Foundry Model Router

## Quick Start (from zero)

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL (XAMPP recommended) running on localhost:3306
- Azure AI Foundry account (optional — fallbacks work without it)

### 1. Clone and configure

```bash
git clone <repo-url>
cd "8 Hours Hackathon"
git config core.hooksPath hooks   # Strips Cursor co-author trailers
```

### 2. Backend setup

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your MySQL credentials and Azure AI keys
python seed.py                    # Creates DB + demo data
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Access the app

- **Frontend:** http://localhost:5173
- **API Docs:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

### Demo logins (password: `password123`)

| Role | Email |
| --- | --- |
| Admin | `admin@edu.local` |
| Teacher | `priya.nair@edu.local` |
| Student | `rohan.sharma@edu.local` |

## Demo notes (judges)

The live wow-moment is **My Progress → “Ask about your progress”**. Log in as `rohan.sharma@edu.local`, open My Progress, and ask something like “Why is my attendance flagged?” or “What should I study first?” The assistant only sees that student’s attendance, grades, exam analysis, weak subjects, and assignment AI feedback. Off-topic questions get a polite redirect.

Then optionally show **Generate practice questions** on a weak subject, and **Refresh insights** on the admin dashboard.

---

## Feature Overview

### Public Pages
- **Home:** Hero banner, announcements, featured courses, top teachers, AI study tips (static rotating list)
- **Courses:** Search, filter by category, course listing, top-rated sidebar
- **Course Details:** Full info, syllabus, teacher info, schedule, enroll button
- **Contact:** Contact form (stored in DB), FAQ, support info

### Academic Flow
- **Attendance:** Teachers mark per-class; students view own records + summary percentages
- **Assignments:** Create with due dates, student submissions, teacher grading with feedback
- **Exams & Grades:** Create exams, record marks per student, grade history view
- **AI Feedback:** Auto-generated when teacher grades a submission
- **Exam Analysis:** AI summary + weak topics written when marks are recorded

### User Dashboards
- **Student:** Profile, enrolled courses, assignments with submissions, attendance, grades, AI recommendations, progress overview
- **Teacher:** Profile, owned courses and classes, links to academic management
- **My Progress (student):** Performance metrics, **Ask about your progress** chat, weak subjects with practice questions, improvement tips, AI insights, at-risk trend

### Admin Dashboard
- **User Management:** List/create/deactivate students and teachers
- **Quick Links:** Manage courses, assignments, exams, attendance
- **AI Insights & Monitoring:** View/refresh stored insights across all classes, including at-risk trend arrows

### Reports & Performance Summary
- **Student Report:** Own academic summary, weak areas, risk analysis, AI recommendations, print/download
- **Class Report:** Teacher/admin view of class performance, at-risk students, student table
- **Comparative Report:** Cross-class comparison, total stats, AI recommendations rollup
- **Admin Insights Summary:** Insight counts and recent AI-generated content

### AI Engine (Azure AI Foundry)
- **Performance Analysis:** Narrative summary from attendance + grades data
- **At-Risk Detection:** Flags students with attendance < 70% or exam avg < 60%; model explains why. Includes a **risk trend** (improving / worsening / stable) comparing the last 3 days with the 3 days before that.
- **Weak Subject Identification:** Identifies subjects needing improvement from grade patterns
- **Study Recommendations:** Personalized tips per student
- **Class Insights:** Teacher/admin-facing summaries per class
- All insights stored in `ai_insights` table (6-hour cache, refresh on demand)

**Risk trend windowing:** `ai_insights.trend` is `improving`, `worsening`, `stable`, or null. `trend_reason` is the one-line explanation. Windows are `TREND_WINDOW_DAYS = 3`: recent = `[today-3, today]`, prior = `[today-6, today-3)`. The model (via `ai_service.py`) sees both windows; if Azure fails, a ±5 percentage-point rule on attendance (and exam average when both windows have exams) is the fallback. Stored on the existing `at_risk` row — no extra table.

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env`:

| Variable | Purpose | Default |
| --- | --- | --- |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `root` |
| `DB_PASSWORD` | MySQL password | (empty) |
| `DB_NAME` | Database name | `education_portal` |
| `SECRET_KEY` | JWT signing secret | `dev-only-change-me` |
| `AZURE_AI_ENDPOINT` | Full Azure AI Foundry URL (`.../protocols/openai/responses`) | |
| `AZURE_AI_KEY` | Azure API key (never commit!) | |
| `AZURE_AI_MODEL` | Deployment name | `model-router` |
| `AZURE_AI_API_VERSION` | API version | `v1` |

---

## Azure AI Foundry Setup

1. Go to [Azure AI Foundry](https://ai.azure.com) and open your project
2. Deploy **Model Router** or an agent exposing the OpenAI Responses protocol
3. Copy the full POST URL into `AZURE_AI_ENDPOINT` (e.g., `.../protocols/openai/responses`)
4. Copy the key into `AZURE_AI_KEY`
5. Set `AZURE_AI_API_VERSION=v1` (or `2025-11-15-preview`)
6. Restart uvicorn after changing `.env`

**Note:** If Azure is unavailable, the AI Engine writes rule-based fallbacks. Pages never break due to AI failures.

---

## API Endpoints Summary

### Authentication
| Method | Path | Access |
| --- | --- | --- |
| POST | `/auth/register` | Public (student/teacher) |
| POST | `/auth/login` | Public |
| POST | `/auth/admin/login` | Public (admin only) |
| GET | `/auth/me` | Authenticated |
| POST | `/auth/logout` | Authenticated |

### Courses & Classes
| Method | Path | Access |
| --- | --- | --- |
| GET | `/courses`, `/courses/top-rated`, `/courses/categories` | Public |
| POST | `/courses` | Teacher, Admin |
| PATCH/DELETE | `/courses/{id}` | Owner teacher, Admin |
| POST | `/courses/{id}/classes` | Owner teacher, Admin |
| POST | `/enrollments` | Student (self) |

### Academic
| Method | Path | Access |
| --- | --- | --- |
| POST | `/attendance/mark` | Owner teacher, Admin |
| GET | `/attendance`, `/attendance/summary` | Class members |
| POST | `/assignments` | Owner teacher, Admin |
| POST | `/assignments/{id}/submissions` | Enrolled student |
| PATCH | `/submissions/{id}` | Owner teacher, Admin |
| POST | `/exams` | Owner teacher, Admin |
| PUT | `/exams/{id}/grades` | Owner teacher, Admin |

### AI & Reports
| Method | Path | Access |
| --- | --- | --- |
| GET | `/ai/status` | Public |
| GET | `/ai/me` | Student |
| POST | `/ai/refresh` | Student |
| POST | `/ai/practice-questions/{student_id}` | Student (self only) |
| POST | `/ai/assistant/{student_id}` | Student (self only) |
| GET | `/ai/monitoring` | Teacher, Admin |
| POST | `/ai/monitoring/refresh` | Teacher, Admin |
| GET | `/reports/me` | Student |
| GET | `/reports/student/{id}` | Teacher, Admin |
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
├── frontend/           # Vite + React + Tailwind
│   └── src/
│       ├── pages/      # Route components
│       ├── dashboards/ # Dashboard panels
│       ├── components/ # Reusable UI
│       └── context/    # Auth + Toast providers
├── backend/            # FastAPI + SQLAlchemy
│   ├── app/
│   │   ├── routers/    # API endpoints
│   │   ├── services/   # Business logic
│   │   ├── models/     # SQLAlchemy models
│   │   └── schemas/    # Pydantic schemas
│   ├── seed.py         # Database seeder
│   └── .env.example
└── hooks/              # Git hooks (no Cursor attribution)
```

---

## Diagram Coverage Checklist

### Public Pages (Main Navigation)
- [x] Home Page — Hero / Banner
- [x] Home Page — Announcements
- [x] Home Page — Featured Courses
- [x] Home Page — Top Teachers
- [x] Home Page — AI Study Tips *(static rotating list)*
- [x] Home Page — CTA → Explore Courses
- [x] Courses Page — Search Courses
- [x] Courses Page — Filter
- [x] Courses Page — Categories
- [x] Courses Page — Course Listing
- [x] Courses Page — Top Rated Courses
- [x] Course Details — Course Info
- [x] Course Details — Syllabus
- [x] Course Details — Teacher Info
- [x] Course Details — Schedule
- [x] Course Details — Enroll Now
- [x] Contact Page — Contact Info
- [x] Contact Page — Contact Form
- [x] Contact Page — FAQ
- [x] Contact Page — Support

### Academic Flow
- [x] Attendance — Mark Attendance
- [x] Attendance — View Attendance
- [x] Attendance — Attendance Summary
- [x] Assignments — Create / View
- [x] Assignments — Submit Assignments
- [x] Assignments — Due Dates
- [x] Assignments — AI Feedback
- [x] Exams & Grades — Take Exams *(record marks, not live quiz)*
- [x] Exams & Grades — View Grades
- [x] Exams & Grades — Grade History
- [x] Exams & Grades — Exam Analysis

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

### Admin Area
- [x] Admin Login — Secure Access
- [x] Admin Dashboard — Manage Students
- [x] Admin Dashboard — Manage Teachers
- [x] Admin Dashboard — Manage Courses & Classes
- [x] Admin Dashboard — Manage Assignments
- [x] Admin Dashboard — Manage Exams & Grades
- [x] Admin Dashboard — View Reports & Analytics
- [x] Admin Dashboard — AI Insights & Monitoring

### AI Engine
- [x] Performance Analysis
- [x] At-Risk Student Detection
- [x] Weak Subject Identification
- [x] Study Recommendations
- [x] AI Insights & Reports

### Reports & Insights
- [x] Student Performance Reports
- [x] Class Performance Reports
- [x] Comparative Reports
- [x] AI Recommendations Rollup

### Performance Reports & Summary
- [x] Academic Performance Summary
- [x] Weak Areas Identified
- [x] Risk Analysis
- [x] AI Recommendations
- [x] Download / Print Report

### Innovation Add-ons
- [x] **AI progress assistant (headline demo)** — My Progress chat: `POST /ai/assistant/{student_id}` with a free-text question. Context is **this student only** (attendance summary, grades, `exam_analysis.weak_topics`, stored weak subjects, assignment `ai_feedback`). Answers are 2–4 sentences. Off-topic questions are refused. Chat is **client-side only** (refresh clears it). Cap: 16 messages in the UI; last 6 turns sent as history. Rate limit: 12 questions / 5 minutes per student (in-memory, 429).
- [x] At-risk **risk trend** — improving / worsening / stable (or “not enough data yet”) on My Progress and Admin AI Insights & Monitoring
- [x] **Generate practice questions** — My Progress, per weak subject; 3–4 questions from the Model Router using that subject + `exam_analysis.weak_topics`. Questions are **not persisted**; each click (or retry) generates a fresh set.

---

## Known Limitations

1. **AI Study Tips on Home are static** — A rotating list in `frontend/src/data/studyTips.js`, not generated by Azure.

2. **JWT is memory-only** — Refreshing the browser logs you out. There's no refresh token or persistent session.

3. **"Take Exams" is mark entry** — Teachers record student marks; there's no live quiz-taking UI.

4. **No file uploads** — Assignment submissions are text-only; no attachments.

5. **Single-tenant design** — No multi-school/organization support.

6. **No email verification** — Registration succeeds immediately; no confirmation email.

7. **Demo data uses @edu.local** — Won't pass strict RFC email validators.

8. **Print/Download is browser print** — No server-side PDF generation.

9. **Insights cached 6 hours** — Manual "Refresh" required for fresh AI analysis.

10. **CORS locked to localhost:5173** — Change `main.py` for production deployment.

11. **Risk trend uses 3-day windows, not 2 weeks** — Seed attendance only covers 5 consecutive days (`today-1` through `today-5`) and seed exams sit 10 days back, so a 14-day vs prior-14-day split would always be empty. Trend compares **the last 3 calendar days** with **the 3 days before that**. Both windows need at least one attendance record; otherwise the UI shows “not enough data yet” and does not guess. Demo exam dates usually fall outside both windows, so the first demo trend is attendance-driven.

12. **Practice questions are not saved** — `POST /ai/practice-questions/{student_id}` generates 3–4 questions on each click from the weak subject plus `exam_analysis.weak_topics`. Refreshing the page clears them.

13. **Assistant chat is not saved** — Messages live in React state only. Rate limit is in-process memory (resets if uvicorn restarts).

---

## Security Notes

- All secrets in `.env` (gitignored)
- CORS restricted to frontend origin
- All mutating endpoints require authentication + role/ownership checks
- No raw SQL — all database access through SQLAlchemy ORM
- JWT tokens expire after 8 hours
- Passwords hashed with bcrypt

---

## Credits

Built during an 8-hour hackathon. Architecture diagram was the source of truth for all features.
