# DClaw Train — v1.2 Feature Roadmap

> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (moodle, openedx), AI product research (Docebo, 360Learning, Sana, Kajabi)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Course/library CRUD
- [ ] Lesson/video content management
- [ ] Learner progress tracking
- [ ] Quiz/assessment builder
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Learning Copilot (Tutor Bot)
**Description:** AI tutor available 24/7 to answer learner questions, explain concepts, and provide hints without giving away answers.
- **AI Angle:** RAG over course content. Socratic questioning prompt engineering.
- **Backend:** `/api/v1/ai/tutor` endpoint. Conversation memory per learner.
- **Frontend:** Floating chat widget in lesson view. Context-aware (knows which lesson you're on).
- **Files:** `backend/app/services/tutor_ai.py`, `frontend/src/components/tutor-bot.tsx`

#### 2. Course Builder & Content Management
**Description:** Drag-and-drop course builder with lessons, videos, quizzes, assignments, and resource attachments.
- **Backend:** Content hierarchy API. File storage. Video processing (transcoding).
- **Frontend:** Visual course builder. Rich text editor. Video uploader.
- **Files:** `backend/app/services/course_builder.py`, `frontend/src/app/courses/builder.tsx`

#### 3. AI-Generated Quizzes & Assessments
**Description:** Auto-generate quizzes from course content with varied question types and difficulty levels.
- **AI Angle:** LLM question generation from transcript/text. Distractor generation.
- **Backend:** `/api/v1/ai/generate-quiz` endpoint.
- **Frontend:** Quiz preview. One-click add to lesson.
- **Files:** `backend/app/services/quiz_ai.py`

#### 4. Learner Progress & Analytics
**Description:** Track completion, time spent, scores. Identify at-risk learners.
- **Backend:** Progress aggregation. Engagement scoring.
- **Frontend:** Learner dashboard. Manager reporting view.
- **Files:** `backend/app/services/analytics.py`

### P1 — Should Have (v1.1–1.2)

#### 5. AI-Powered Personalized Learning Paths
**Description:** AI recommends next courses based on role, skills gaps, and career goals.
- **AI Angle:** Skills gap analysis + recommendation engine.
- **Backend:** Path recommendation API.
- **Frontend:** Personalized dashboard with "Next Up" suggestions.

#### 6. Live Session & Webinar Management
**Description:** Schedule live sessions, send reminders, record, and auto-generate transcripts.
- **Backend:** Calendar integration. Recording storage. Transcription (Whisper).
- **Frontend:** Session scheduler. Live room integration (Zoom/Jitsi).

#### 7. Certification & Badges
**Description:** Issue certificates upon completion. Badge system for achievements.
- **Backend:** Certificate generation (PDF). Badge metadata.
- **Frontend:** Certificate designer. Badge showcase.

#### 8. Skills Assessment & Gap Analysis
**Description:** Pre-assessments to identify skill gaps. Post-assessments to measure improvement.
- **Backend:** Assessment scoring. Gap calculation.
- **Frontend:** Assessment UI. Gap visualization radar chart.

### P2 — Could Have (v1.3+)

#### 9. AI Video Summarization & Chapters
**Description:** Auto-generate video summaries, chapter markers, and searchable transcripts.

#### 10. Peer Learning & Discussion Forums
**Description:** Course-specific forums with AI moderation and question-answering.

#### 11. SCORM/xAPI Compliance
**Description:** Import/export SCORM packages. Track learning experiences via xAPI.

#### 12. VR/AR Training Simulations
**Description:** Immersive training scenarios for high-stakes roles (medical, safety, technical).

---

## Implementation Priority

1. **Week 1–2:** AI Learning Copilot (P0.1) + Course Builder (P0.2)
2. **Week 3–4:** AI Quiz Generator (P0.3) + Progress Analytics (P0.4)
3. **Week 5–6:** Personalized Paths (P1.5) + Live Sessions (P1.6)
4. **Week 7–8:** Certifications (P1.7) + Skills Assessment (P1.8)
