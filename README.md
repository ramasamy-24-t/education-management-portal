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
      deps.py        JWT + role guards
      main.py
      models/
      schemas/
      routers/       auth, courses, classes, enrollments, teachers
      services/
    seed.py
    .env.example
```

## What this step added

- JWT auth: register (student/teacher), user login, admin login, `/auth/me`, logout
- Role/ownership guards on every mutating course, class, and enrollment endpoint
- Course search/filter/categories/top-rated, class CRUD, student enroll, top teachers
- Frontend auth context (token in memory, not `localStorage`), protected routes, login pages
- Live Courses + Course Details + Enroll Now, plus Manage Courses & Classes for teachers/admins

## Assumptions

- **Announcements** are stored in an `announcements` table (Home Page box) even though they were not in the original table list.
- **`courses.syllabus`** holds Course Details syllabus text.
- **Course `rating`** is a denormalized float used for Top Rated Courses. Top Teachers is the average rating of courses taught by that teacher (no separate teacher-rating table).
- **`schedule`** is a human-readable string (e.g. `Mon / Wed 10:00–11:30`).
- **Exam grades** live in `grades`; **assignment grades** live on `assignment_submissions`.
- **`ai_insights.student_id` / `class_id`** are nullable so class-level insights (Admin monitoring) do not require a student.
- Academic Flow screens (Attendance, Assignments, Exams & Grades) will be nested under User / Admin dashboards in later prompts; this step only registered the listed public/user/admin/report routes.
- Seed accounts all use password `password123` (local demo only).
- JWT is **stateless** and stored **only in React memory**. Refreshing the browser logs the user out. `POST /auth/logout` tells the client to discard the token; there is no server-side blacklist.
- Public registration is **student/teacher only**. Admin accounts are seeded (or created in the database). User login rejects admin accounts; Admin Login rejects student/teacher accounts.
- Top Teachers are ranked by **average course rating**, then distinct enrolled-student count.
- A course/class cannot be deleted while it still has attendance, assignments, or exams.
- Demo emails use `@edu.local`. Request validation accepts these (strict RFC email validators reject `.local`).

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
| `SECRET_KEY` | JWT signing secret |
| `JWT_ALGORITHM` | JWT algorithm (default `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime (default `480` = 8 hours) |
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

## Auth flow and roles

1. **Student / Teacher** — `POST /auth/register` (role `student` or `teacher`) or `POST /auth/login`. Frontend: `/login`.
2. **Admin** — `POST /auth/admin/login`. Frontend: `/admin/login`. Admins cannot self-register.
3. Client stores `{ access_token, user }` in `AuthContext` (memory only) and sends `Authorization: Bearer <token>`.
4. `GET /auth/me` returns the current user. `POST /auth/logout` requires a valid token and is a no-op on the server.
5. `ProtectedRoute` sends anonymous users to `/login` or `/admin/login`, and wrong-role users to `/`.

| Role | Can do |
| --- | --- |
| student | Enroll in a course; view public catalog; see own enrollments |
| teacher | Create/update/delete **own** courses and their classes |
| admin | Create/update/delete **any** course/class; must set `teacher_id` on create |

A teacher cannot edit another teacher's course (403). A student cannot create courses or enroll someone else.

### Example: register

```http
POST /auth/register
Content-Type: application/json

{
  "name": "New Student",
  "email": "new.student@edu.local",
  "password": "password123",
  "role": "student"
}
```

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 10,
    "name": "New Student",
    "email": "new.student@edu.local",
    "role": "student",
    "created_at": "2026-08-16T06:00:00"
  }
}
```

### Example: login

```http
POST /auth/login
{"email": "rohan.sharma@edu.local", "password": "password123"}
```

Admin equivalent: `POST /auth/admin/login` with `admin@edu.local`.

### Example: list + enroll

```http
GET /courses?search=python&category=Computer%20Science
GET /courses/top-rated?limit=5
GET /teachers/top?limit=5
POST /enrollments
Authorization: Bearer <token>
{"course_id": 1}
```

### Course / class endpoints

| Method | Path | Who |
| --- | --- | --- |
| GET | `/courses`, `/courses/top-rated`, `/courses/categories`, `/courses/{id}` | Public (optional JWT marks `enrolled`) |
| POST | `/courses` | teacher, admin |
| PATCH / DELETE | `/courses/{id}` | owner teacher or admin |
| GET | `/courses/{id}/classes` | Public |
| POST | `/courses/{id}/classes` | owner teacher or admin |
| PATCH / DELETE | `/classes/{id}` | owner teacher or admin |
| POST | `/enrollments` | student (self only) |
| GET | `/enrollments/me` | student |
| GET | `/teachers`, `/teachers/top` | Public |

## Frontend routes

Protected: `/dashboard` and `/progress` (student/teacher), `/manage/courses` (teacher/admin), `/admin` (admin), `/reports` (any signed-in role).

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

- [x] User Login / Register — Account Access
- [x] User Login / Register — Role Selection (Student / Teacher)
- [x] User Dashboard — Profile
- [x] User Dashboard — My Courses
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

- [x] Admin Login — Secure Access
- [ ] Admin Dashboard — Manage Students
- [ ] Admin Dashboard — Manage Teachers
- [x] Admin Dashboard — Manage Courses & Classes
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
