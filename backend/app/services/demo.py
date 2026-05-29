"""Demo seed / reset for the landing page (REMOVABLE feature).

Every entity written here carries a stable `DEMO ` title prefix (or a
`demo-` learner_id prefix for learner-scoped rows). `reset_demo()` uses
those markers as the only delete predicates — so even if the flag is
flipped on against a populated instance, this cannot touch real data.

This app has no user/auth model (learners are external string IDs), so
the demo exposes no login credentials — `credentials` is always null.

The seed exercises the real LMS feature set:
  • Courses (published) with ordered Lessons
  • A Quiz with Questions on a lesson
  • Learner Enrollments in mixed states with LearnerProgress
  • An upcoming LiveSession
  • A ForumTopic with a reply
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import utc_now
from app.models.train import (
    Course, Lesson, Quiz, Question, Enrollment, LearnerProgress,
    LiveSession, ForumTopic, ForumReply, Certificate, Badge,
    TrainingFormat, EnrollmentStatus, QuestionType, DifficultyLevel,
    SessionStatus, BadgeType,
)

DEMO_PREFIX = "DEMO "
# Demo learners (external string IDs) all start with this so learner-scoped
# rows (badges, certificates) can be cleaned up precisely.
DEMO_LEARNER_PREFIX = "demo-learner"


@dataclass
class DemoStatus:
    enabled: bool
    seeded: bool
    counts: dict[str, int]
    credentials: None = None


async def _demo_course_ids(db: AsyncSession) -> list:
    rows = await db.execute(select(Course.id).where(Course.title.like(f"{DEMO_PREFIX}%")))
    return [r[0] for r in rows.all()]


async def gather_status(db: AsyncSession, *, enabled: bool) -> DemoStatus:
    course_ids = await _demo_course_ids(db)
    if not course_ids:
        return DemoStatus(enabled=enabled, seeded=False, counts={})

    lessons = (await db.execute(
        select(Lesson.id).where(Lesson.course_id.in_(course_ids))
    )).all()
    enrollments = (await db.execute(
        select(Enrollment.id).where(Enrollment.course_id.in_(course_ids))
    )).all()
    sessions = (await db.execute(
        select(LiveSession.id).where(LiveSession.course_id.in_(course_ids))
    )).all()
    topics = (await db.execute(
        select(ForumTopic.id).where(ForumTopic.course_id.in_(course_ids))
    )).all()

    counts = {
        "courses": len(course_ids),
        "lessons": len(lessons),
        "enrollments": len(enrollments),
        "live_sessions": len(sessions),
        "forum_topics": len(topics),
    }
    return DemoStatus(enabled=enabled, seeded=True, counts=counts)


async def seed_demo(db: AsyncSession) -> DemoStatus:
    """Idempotent: wipe any existing demo data, then seed a fresh set."""
    await reset_demo(db)
    now = utc_now()

    # ── Course 1: published, with lessons + a quiz ──────────────────────
    c1 = Course(
        title=f"{DEMO_PREFIX}Onboarding 101",
        description="Get new hires up to speed on tools, culture, and process.",
        format=TrainingFormat.VIDEO,
        category="Onboarding",
        tags="onboarding,basics,culture",
        is_published=True,
    )
    c1.lessons.append(Lesson(
        title="Welcome & Company Values", order=0, is_published=True,
        duration_minutes=8,
        content="An intro to who we are and how we work.",
        video_url="https://example.com/demo/welcome.mp4",
    ))
    l_tools = Lesson(
        title="Your Toolbox", order=1, is_published=True, duration_minutes=12,
        content="A tour of the tools you'll use every day.",
        video_url="https://example.com/demo/tools.mp4",
    )
    c1.lessons.append(l_tools)
    c1.lessons.append(Lesson(
        title="Security Basics", order=2, is_published=True, duration_minutes=10,
        content="Passwords, phishing, and keeping data safe.",
    ))
    db.add(c1)
    await db.flush()

    quiz = Quiz(
        lesson_id=l_tools.id,
        title=f"{DEMO_PREFIX}Toolbox Check",
        description="A quick check on the daily tools.",
        passing_score=70.0,
        is_published=True,
    )
    quiz.questions.append(Question(
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=DifficultyLevel.EASY,
        text="Which tool do we use for version control?",
        options='["Git", "Email", "Spreadsheets", "Sticky notes"]',
        correct_answer="Git",
        explanation="We track all code changes in Git.",
        points=1.0, order=0,
    ))
    quiz.questions.append(Question(
        question_type=QuestionType.TRUE_FALSE,
        difficulty=DifficultyLevel.EASY,
        text="You should reuse the same password everywhere.",
        options='["True", "False"]',
        correct_answer="False",
        explanation="Always use unique passwords.",
        points=1.0, order=1,
    ))
    db.add(quiz)

    # ── Course 2: published video course ────────────────────────────────
    c2 = Course(
        title=f"{DEMO_PREFIX}Advanced Python for Data",
        description="Level up your Python for data engineering workloads.",
        format=TrainingFormat.WORKSHOP,
        category="Engineering",
        tags="python,data,advanced",
        is_published=True,
    )
    c2.lessons.append(Lesson(
        title="Async & Concurrency", order=0, is_published=True, duration_minutes=20,
        content="asyncio, tasks, and when to reach for threads.",
    ))
    c2.lessons.append(Lesson(
        title="Profiling & Performance", order=1, is_published=True, duration_minutes=18,
        content="Find and fix the slow parts of your code.",
    ))
    db.add(c2)

    # ── Course 3: draft (unpublished) ───────────────────────────────────
    c3 = Course(
        title=f"{DEMO_PREFIX}Leadership Foundations",
        description="A draft course on first-time management skills.",
        format=TrainingFormat.DOCUMENT,
        category="Leadership",
        tags="leadership,management",
        is_published=False,
    )
    c3.lessons.append(Lesson(
        title="Giving Feedback", order=0, is_published=False, duration_minutes=15,
        content="Frameworks for clear, kind feedback.",
    ))
    db.add(c3)
    await db.flush()

    # ── Enrollments + progress (mixed states) ───────────────────────────
    e_done = Enrollment(
        course_id=c1.id, learner_id=f"{DEMO_LEARNER_PREFIX}-alice",
        status=EnrollmentStatus.COMPLETED, progress_percentage=100.0,
        enrolled_at=now - timedelta(days=14), completed_at=now - timedelta(days=2),
    )
    e_progress = Enrollment(
        course_id=c1.id, learner_id=f"{DEMO_LEARNER_PREFIX}-bob",
        status=EnrollmentStatus.IN_PROGRESS, progress_percentage=40.0,
        enrolled_at=now - timedelta(days=5),
    )
    e_new = Enrollment(
        course_id=c2.id, learner_id=f"{DEMO_LEARNER_PREFIX}-carol",
        status=EnrollmentStatus.ENROLLED, progress_percentage=0.0,
        enrolled_at=now - timedelta(days=1),
    )
    db.add_all([e_done, e_progress, e_new])
    await db.flush()

    # A couple of progress rows for the in-progress learner.
    c1_lessons = sorted(c1.lessons, key=lambda l: l.order)
    db.add(LearnerProgress(
        enrollment_id=e_progress.id, lesson_id=c1_lessons[0].id,
        status="Completed", time_spent_seconds=480,
        completed_at=now - timedelta(days=4),
    ))
    db.add(LearnerProgress(
        enrollment_id=e_progress.id, lesson_id=c1_lessons[1].id,
        status="In Progress", time_spent_seconds=120,
    ))

    # ── Upcoming live session ───────────────────────────────────────────
    db.add(LiveSession(
        course_id=c2.id,
        title=f"{DEMO_PREFIX}Live Q&A: Python Performance",
        description="Bring your slow code — we'll profile it together.",
        session_url="https://meet.example.com/demo-python",
        status=SessionStatus.SCHEDULED,
        scheduled_at=now + timedelta(days=3),
        duration_minutes=60,
        max_participants=50,
    ))

    # ── Forum topic + reply ─────────────────────────────────────────────
    topic = ForumTopic(
        course_id=c1.id, learner_id=f"{DEMO_LEARNER_PREFIX}-bob",
        title=f"{DEMO_PREFIX}How do I set up my dev environment?",
        content="I'm stuck on the toolbox lesson — any tips for the initial setup?",
    )
    topic.replies.append(ForumReply(
        learner_id=f"{DEMO_LEARNER_PREFIX}-alice",
        content="Follow the Toolbox lesson step by step and ping #help if you get stuck!",
    ))
    topic.replies.append(ForumReply(
        learner_id="ai-tutor",
        content="Great question! Start by installing Git and signing in to the tools listed in the lesson.",
        is_ai_response=True,
    ))
    db.add(topic)

    # ── A badge + certificate for the completed learner ─────────────────
    db.add(Badge(
        learner_id=f"{DEMO_LEARNER_PREFIX}-alice",
        badge_type=BadgeType.COMPLETION,
        course_id=c1.id,
        title=f"{DEMO_PREFIX}Onboarding Graduate",
        description="Completed the Onboarding 101 course.",
    ))
    db.add(Certificate(
        course_id=c1.id,
        learner_id=f"{DEMO_LEARNER_PREFIX}-alice",
        certificate_url="https://example.com/demo/cert-alice.pdf",
    ))

    await db.commit()
    return await gather_status(db, enabled=True)


async def reset_demo(db: AsyncSession) -> DemoStatus:
    """Delete only rows whose markers identify them as demo data.

    Deleting the demo courses cascades lessons, quizzes, questions,
    enrollments, progress, live sessions, and forum topics/replies.
    Learner-scoped rows (badges, certificates) are deleted by the
    demo-learner prefix because they may outlive their course
    (course_id is SET NULL for badges).
    """
    course_ids = await _demo_course_ids(db)
    if course_ids:
        await db.execute(delete(Course).where(Course.id.in_(course_ids)))

    await db.execute(
        delete(Badge).where(Badge.learner_id.like(f"{DEMO_LEARNER_PREFIX}%"))
    )
    await db.execute(
        delete(Certificate).where(Certificate.learner_id.like(f"{DEMO_LEARNER_PREFIX}%"))
    )
    await db.commit()
    return await gather_status(db, enabled=True)
