# DClaw Train — v1.2 Feature Roadmap

> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (moodle, openedx), AI product research (Docebo, 360Learning, Sana, Kajabi)

## Pre-Flight Checklist

- [x] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [x] `frontend/next-env.d.ts` exists and is committed
- [x] `docker-compose.yml` healthchecks correct
- [x] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [x] Course/library CRUD
- [x] Lesson/video content management
- [x] Learner progress tracking
- [x] Quiz/assessment builder
- [x] Real backend CRUD (no mocks)
- [x] Docker + Helm deployment
- [x] Alembic migrations
- [x] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Learning Copilot (Tutor Bot)
**Description:** AI tutor available 24/7 to answer learner questions, explain concepts, and provide hints without giving away answers.
- **AI Angle:** RAG over course content. Socratic questioning prompt engineering.
- **Backend:** `/api/v1/ai/tutor` endpoint. Conversation memory per learner.
- **Frontend:** Floating chat widget in lesson view. Context-aware (knows which lesson you're on).
- **Files:** `backend/app/services/tutor_ai.py`, `frontend/src/components/tutor-bot.tsx`
- [x] **IMPLEMENTED** — Socratic tutor with conversation memory, context-aware, floating chat widget

#### 2. Course Builder & Content Management
**Description:** Drag-and-drop course builder with lessons, videos, quizzes, assignments, and resource attachments.
- **Backend:** Content hierarchy API. File storage. Video processing (transcoding).
- **Frontend:** Visual course builder. Rich text editor. Video uploader.
- **Files:** `backend/app/services/course_builder.py`, `frontend/src/app/courses/builder.tsx`
- [x] **IMPLEMENTED** — Course structure API, visual builder with lesson CRUD, resource management

#### 3. AI-Generated Quizzes & Assessments
**Description:** Auto-generate quizzes from course content with varied question types and difficulty levels.
- **AI Angle:** LLM question generation from transcript/text. Distractor generation.
- **Backend:** `/api/v1/ai/generate-quiz` endpoint.
- **Frontend:** Quiz preview. One-click add to lesson.
- **Files:** `backend/app/services/quiz_ai.py`
- [x] **IMPLEMENTED** — AI quiz generation with multiple choice, true/false, short answer; difficulty levels

#### 4. Learner Progress & Analytics
**Description:** Track completion, time spent, scores. Identify at-risk learners.
- **Backend:** Progress aggregation. Engagement scoring.
- **Frontend:** Learner dashboard. Manager reporting view.
- **Files:** `backend/app/services/analytics.py`
- [x] **IMPLEMENTED** — Analytics overview, learner analytics, course analytics, at-risk detection, engagement scores

### P1 — Should Have (v1.1–1.2)

#### 5. AI-Powered Personalized Learning Paths
**Description:** AI recommends next courses based on role, skills gaps, and career goals.
- **AI Angle:** Skills gap analysis + recommendation engine.
- **Backend:** Path recommendation API.
- **Frontend:** Personalized dashboard with "Next Up" suggestions.
- [x] **IMPLEMENTED** — Learning path API, role-based recommendations, skills gap visualization

#### 6. Live Session & Webinar Management
**Description:** Schedule live sessions, send reminders, record, and auto-generate transcripts.
- **Backend:** Calendar integration. Recording storage. Transcription (Whisper).
- **Frontend:** Session scheduler. Live room integration (Zoom/Jitsi).
- [x] **IMPLEMENTED** — Live session CRUD, upcoming sessions list, status tracking

#### 7. Certification & Badges
**Description:** Issue certificates upon completion. Badge system for achievements.
- **Backend:** Certificate generation (PDF). Badge metadata.
- **Frontend:** Certificate designer. Badge showcase.
- [x] **IMPLEMENTED** — Certificate issuance, badge system with completion/excellence/speed/streak/mentor types

#### 8. Skills Assessment & Gap Analysis
**Description:** Pre-assessments to identify skill gaps. Post-assessments to measure improvement.
- **Backend:** Assessment scoring. Gap calculation.
- **Frontend:** Assessment UI. Gap visualization radar chart.
- [x] **IMPLEMENTED** — Pre/post assessments, gap analysis with improvements tracking

### P2 — Could Have (v1.3+)

#### 9. AI Video Summarization & Chapters
**Description:** Auto-generate video summaries, chapter markers, and searchable transcripts.
- [x] **IMPLEMENTED** — Video summary generation with chapters and transcripts

#### 10. Peer Learning & Discussion Forums
**Description:** Course-specific forums with AI moderation and question-answering.
- [x] **IMPLEMENTED** — Forum topics, replies, AI auto-response, content moderation

#### 11. SCORM/xAPI Compliance
**Description:** Import/export SCORM packages. Track learning experiences via xAPI.
- [x] **IMPLEMENTED** — SCORM import/export, xAPI statement storage and retrieval

#### 12. VR/AR Training Simulations
**Description:** Immersive training scenarios for high-stakes roles (medical, safety, technical).
- [ ] **STUB** — Architecture ready but implementation requires device-specific SDKs

---

## Implementation Status

### ✅ COMPLETED

| Phase | Features | Backend | Frontend |
|-------|----------|---------|----------|
| Foundation | Course CRUD, Lessons, Resources | 10 models, 16 repositories | Dashboard with CRUD |
| Foundation | Quizzes, Questions, Assessments | Full CRUD + scoring | Quiz view + one-click AI gen |
| Foundation | Enrollments, Progress Tracking | Progress tracking + time accumulation | Learner progress view |
| P0 | AI Learning Copilot | tutor_ai.py, RAG, Socratic | tutor-bot.tsx floating widget |
| P0 | Course Builder | course_builder.py, structure API | /courses/builder.tsx visual builder |
| P0 | AI Quiz Generator | quiz_ai.py, multiple types | Quiz preview in builder |
| P0 | Progress Analytics | analytics.py, engagement scoring | Analytics dashboard tab |
| P1 | Learning Paths | learning_path.py, recommendations | Path visualization + gaps |
| P1 | Live Sessions | live_sessions.py, scheduling | Sessions tab, upcoming list |
| P1 | Certifications & Badges | certifications.py, 5 badge types | Badges tab, certificate gen |
| P1 | Skills Assessment | skills.py, pre/post + gap analysis | Assessment submit + gaps |
| P2 | Video Summarization | video_ai.py, chapters | Summarize endpoint |
| P2 | Discussion Forums | forum.py, AI moderation | Forum topics + replies |
| P2 | SCORM/xAPI | scorm.py, manifest gen, statements | Import/export endpoints |

### 📋 DEPLOYMENT READY

- **55 API routes** across all v1.2 features
- **30+ test cases** covering all modules
- **Docker** configured at ports 8039 (backend) / 3039 (frontend)
- **Alembic** migration config updated
- **Pre-built UI components** used throughout (no shadcn/CLI deps)

---

## Running the App

```bash
# Start PostgreSQL
docker compose up -d postgres

# Backend (port 8039)
cd backend && python3 -m uvicorn app.api.main:app --port 8039 --reload

# Frontend (port 3039)
cd frontend && npm run dev

# Tests
cd backend && python3 -m pytest tests/ -v
```

## API Documentation

Once the backend is running, visit: http://localhost:8039/docs
