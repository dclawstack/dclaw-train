# DClaw Train

> **Employee Training & LMS Platform** — AI-powered learning management built on the DClaw Stack.
>
> **Author:** Ramsai Kamavaram — [kamavaram.ramsai@gmail.com](mailto:kamavaram.ramsai@gmail.com)

**Category:** L&D · **Version:** 0.1.0 · **Status:** Active Development
**Backend Port:** `8039` (FastAPI) · **Frontend Port:** `3039` (Next.js) · **Database:** `dclaw_train` (PostgreSQL)

---

## Features

### v1.0 — Core LMS (Current)

- [x] Course & library CRUD — create, organize, and manage training courses
- [x] Lesson & video content management — structured lessons with rich media
- [x] Learner progress tracking — per-user completion and time-spent tracking
- [x] Quiz & assessment builder — manual quiz creation with varied question types
- [x] Real backend CRUD — no mock data; everything persisted to PostgreSQL
- [x] Docker + Helm deployment — containerized with Kubernetes support
- [x] Alembic migrations — version-controlled database schema
- [x] Backend tests — pytest with async SQLAlchemy test fixtures

### P0 — Must Have (v1.2)

- [ ] **AI Learning Copilot (Tutor Bot)** — 24/7 AI tutor using RAG over course content. Socratic-style Q&A, context-aware per lesson. Floating chat widget in lesson view.
- [ ] **Course Builder & Content Management** — Drag-and-drop visual course builder with rich text editing, video upload/transcoding, and resource attachments.
- [ ] **AI-Generated Quizzes & Assessments** — LLM-powered auto-generation of questions with distractors from course transcripts. One-click add to lessons.
- [ ] **Learner Progress & Analytics** — Completion tracking, time spent, engagement scoring. At-risk learner identification. Manager reporting dashboard.

### P1 — Should Have (v1.1–v1.2)

- [ ] **AI-Powered Personalized Learning Paths** — Smart recommendations based on role, skills gaps, and career goals.
- [ ] **Live Session & Webinar Management** — Scheduling, reminders, recording, and auto-transcription (Whisper). Zoom/Jitsi integration.
- [ ] **Certification & Badges** — PDF certificate generation on completion. Gamified badge system for achievements.
- [ ] **Skills Assessment & Gap Analysis** — Pre/post assessments with radar-chart skill-gap visualization.

### P2 — Could Have (v1.3+)

- [ ] **AI Video Summarization & Chapters** — Auto-generated summaries, chapter markers, and searchable transcripts.
- [ ] **Peer Learning & Discussion Forums** — Course-specific forums with AI moderation and Q&A.
- [ ] **SCORM/xAPI Compliance** — Import/export SCORM packages. Track learning experiences via xAPI.
- [ ] **VR/AR Training Simulations** — Immersive scenarios for high-stakes roles (medical, safety, technical).

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI + SQLAlchemy 2.0 (async) + Pydantic v2 |
| **Frontend** | Next.js 14 (App Router) + Tailwind CSS |
| **Database** | PostgreSQL (via `dclaw_train`) |
| **AI/ML** | RAG pipeline, LLM integration (tutor bot, quiz gen, summarization) |
| **Infra** | Docker, docker-compose, Helm (Kubernetes) |
| **CI/CD** | GitHub Actions |
| **Migrations** | Alembic (async) |

---

## Getting Started

```bash
# Clone
git clone <repo-url> dclaw-train
cd dclaw-train

# Start services
docker compose up -d

# Backend runs on http://localhost:8039
# Frontend runs on http://localhost:3039
# API docs at http://localhost:8039/docs
```

### Environment

Copy `.env.example` to `.env` and configure:
- `DATABASE_URL` — PostgreSQL connection string
- `NEXT_PUBLIC_API_URL` — Backend URL for the frontend (default: `http://localhost:8039/api/v1`)

---

## Architecture Lock (Do Not Change)

These patterns are non-negotiable across all DClaw apps:

| Rule | Reason |
|------|--------|
| **`DeclarativeBase` from `app.models.base`** | Single metadata source; no `declarative_base()` elsewhere |
| **`Mapped[...]` + `mapped_column()`** | SQLAlchemy 2.0 typed model syntax |
| **`Depends(get_db)` for DI** | Never manually instantiate `AsyncSession` |
| **Repository pattern** | All DB access through `app/repositories/` |
| **No mock data** | No in-memory dicts; always real DB |
| **Pydantic v2** `ConfigDict(from_attributes=True)` | ORM mode for schemas |
| **`pytest-asyncio==0.24.0` pinned** | v1.3.0 breaks fixture scoping |
| **Pre-built UI components only** | Never install shadcn CLI or `@base-ui/react` |
| **`ARG NEXT_PUBLIC_API_URL` in Dockerfile** | Required before `npm run build` |

---

## Project Structure

```
Train/
├── backend/
│   ├── app/
│   │   ├── api/v1/           # App-specific routers
│   │   ├── core/             # config.py, database.py
│   │   ├── models/           # SQLAlchemy models (Base from models/base.py)
│   │   ├── repositories/     # CRUD layer
│   │   ├── schemas/          # Pydantic v2 schemas
│   │   └── services/         # Business logic + AI services
│   ├── alembic/              # Database migrations
│   └── tests/                # pytest (async, ASGITransport)
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/ui/    # Pre-built UI components
│   │   └── lib/              # api.ts, utils.ts
│   └── Dockerfile
├── docker-compose.yml
├── helm/                     # Kubernetes chart
└── .github/workflows/ci.yml  # CI pipeline
```

---

## Port Registry

| App | Backend | Frontend | Database |
|-----|---------|----------|----------|
| dclaw-chat | 8090 | 3000 | dclaw_chat |
| dclaw-med | 8092 | 3004 | dclaw_med |
| dclaw-learn | 8093 | 3003 | dclaw_learn |
| dclaw-code | 8094 | 3005 | dclaw_code |
| dclaw-legal | 8099 | 3013 | dclaw_legal |
| dclaw-crm | 8095 | 3006 | dclaw_crm |
| dclaw-finance | 8096 | 3007 | dclaw_finance |
| dclaw-hr | 8097 | 3008 | dclaw_hr |
| dclaw-inventory | 8098 | 3009 | dclaw_inventory |
| dclaw-project | 8100 | 3010 | dclaw_project |
| dclaw-support | 8101 | 3014 | dclaw_support |
| dclaw-marketing | 8102 | 3015 | dclaw_marketing |
| dclaw-real-estate | 8103 | 3016 | dclaw_real_estate |
| dclaw-sales | 8104 | 3017 | dclaw_sales |
| dclaw-recruit | 8105 | 3018 | dclaw_recruit |
| dclaw-vendor | 8106 | 3019 | dclaw_vendor |
| dclaw-doc | 8107 | 3020 | dclaw_doc |
| dclaw-calendar | 8108 | 3021 | dclaw_calendar |
| **dclaw-train** | **8039** | **3039** | **dclaw_train** |

---

## Author

**Ramsai Kamavaram**  
📧 [kamavaram.ramsai@gmail.com](mailto:kamavaram.ramsai@gmail.com)

Built on the [DClaw Stack](https://github.com/dclawstack) — AI-first vertical SaaS infrastructure.
