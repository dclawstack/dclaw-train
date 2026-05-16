from datetime import datetime, timezone
import uuid
from typing import Optional, List

from sqlalchemy import String, Integer, Float, Text, DateTime, ForeignKey, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import Base
from app.core.utils import utc_now


class TrainingFormat(str, enum.Enum):
    VIDEO = "Video"
    QUIZ = "Quiz"
    WORKSHOP = "Workshop"
    DOCUMENT = "Document"
    ASSIGNMENT = "Assignment"


class EnrollmentStatus(str, enum.Enum):
    ENROLLED = "Enrolled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    DROPPED = "Dropped"


class QuestionType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class SessionStatus(str, enum.Enum):
    SCHEDULED = "Scheduled"
    LIVE = "Live"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class BadgeType(str, enum.Enum):
    COMPLETION = "completion"
    EXCELLENCE = "excellence"
    SPEED = "speed"
    STREAK = "streak"
    MENTOR = "mentor"


# ────────────────────────────── Course ──────────────────────────────


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    format: Mapped[TrainingFormat] = mapped_column(SAEnum(TrainingFormat), default=TrainingFormat.VIDEO)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # comma-separated
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", back_populates="course", lazy="selectin",
        cascade="all, delete-orphan", order_by="Lesson.order"
    )
    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment", back_populates="course", lazy="selectin",
        cascade="all, delete-orphan"
    )
    live_sessions: Mapped[List["LiveSession"]] = relationship(
        "LiveSession", back_populates="course", lazy="selectin",
        cascade="all, delete-orphan"
    )
    forum_topics: Mapped[List["ForumTopic"]] = relationship(
        "ForumTopic", back_populates="course", lazy="selectin",
        cascade="all, delete-orphan"
    )


# ────────────────────────────── Lesson ──────────────────────────────


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Rich text / markdown
    video_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    video_transcript: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    video_chapters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    course: Mapped["Course"] = relationship("Course", back_populates="lessons")
    resources: Mapped[List["LessonResource"]] = relationship(
        "LessonResource", back_populates="lesson", lazy="selectin",
        cascade="all, delete-orphan"
    )
    quizzes: Mapped[List["Quiz"]] = relationship(
        "Quiz", back_populates="lesson", lazy="selectin",
        cascade="all, delete-orphan"
    )


# ────────────────────────────── LessonResource ──────────────────────────────


class LessonResource(Base):
    __tablename__ = "lesson_resources"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pdf, link, image, file
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="resources")


# ────────────────────────────── Quiz ──────────────────────────────


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    passing_score: Mapped[float] = mapped_column(Float, default=70.0)
    time_limit_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="quizzes")
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="quiz", lazy="selectin",
        cascade="all, delete-orphan", order_by="Question.order"
    )
    attempts: Mapped[List["QuizAttempt"]] = relationship(
        "QuizAttempt", back_populates="quiz", lazy="selectin",
        cascade="all, delete-orphan"
    )


# ────────────────────────────── Question ──────────────────────────────


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_type: Mapped[QuestionType] = mapped_column(SAEnum(QuestionType), default=QuestionType.MULTIPLE_CHOICE)
    difficulty: Mapped[DifficultyLevel] = mapped_column(SAEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of options
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    points: Mapped[float] = mapped_column(Float, default=1.0)
    order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    # Relationships
    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")


# ────────────────────────────── QuizAttempt ──────────────────────────────


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    quiz_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quizzes.id", ondelete="CASCADE"))
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)  # external user ID
    score: Mapped[float] = mapped_column(Float, default=0.0)
    total_points: Mapped[float] = mapped_column(Float, default=0.0)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    answers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    started_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="attempts")


# ────────────────────────────── Enrollment ──────────────────────────────


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[EnrollmentStatus] = mapped_column(SAEnum(EnrollmentStatus), default=EnrollmentStatus.ENROLLED)
    progress_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    course: Mapped["Course"] = relationship("Course", back_populates="enrollments")
    lesson_progress: Mapped[List["LearnerProgress"]] = relationship(
        "LearnerProgress", back_populates="enrollment", lazy="selectin",
        cascade="all, delete-orphan"
    )


# ────────────────────────────── LearnerProgress ──────────────────────────────


class LearnerProgress(Base):
    __tablename__ = "learner_progress"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    enrollment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("enrollments.id", ondelete="CASCADE"))
    lesson_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(String(50), default="Not Started")  # Not Started, In Progress, Completed
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    enrollment: Mapped["Enrollment"] = relationship("Enrollment", back_populates="lesson_progress")


# ────────────────────────────── LiveSession ──────────────────────────────


class LiveSession(Base):
    __tablename__ = "live_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    session_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)  # Zoom/Jitsi link
    status: Mapped[SessionStatus] = mapped_column(SAEnum(SessionStatus), default=SessionStatus.SCHEDULED)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    recording_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    transcript: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    max_participants: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    course: Mapped[Optional["Course"]] = relationship("Course", back_populates="live_sessions")


# ────────────────────────────── Certificate ──────────────────────────────


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    certificate_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    cert_metadata: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON


# ────────────────────────────── Badge ──────────────────────────────


class Badge(Base):
    __tablename__ = "badges"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    badge_type: Mapped[BadgeType] = mapped_column(SAEnum(BadgeType), nullable=False)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    earned_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


# ────────────────────────────── Skill / Assessment ──────────────────────────────


class SkillAssessment(Base):
    __tablename__ = "skill_assessments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    assessment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # pre, post
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    skills_data: Mapped[str] = mapped_column(Text, nullable=False)  # JSON: {skill_name: score}
    overall_score: Mapped[float] = mapped_column(Float, default=0.0)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


# ────────────────────────────── Forum ──────────────────────────────


class ForumTopic(Base):
    __tablename__ = "forum_topics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_ai_moderated: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    course: Mapped["Course"] = relationship("Course", back_populates="forum_topics")
    replies: Mapped[List["ForumReply"]] = relationship(
        "ForumReply", back_populates="topic", lazy="selectin",
        cascade="all, delete-orphan", order_by="ForumReply.created_at"
    )


class ForumReply(Base):
    __tablename__ = "forum_replies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("forum_topics.id", ondelete="CASCADE"))
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_ai_response: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    topic: Mapped["ForumTopic"] = relationship("ForumTopic", back_populates="replies")


# ────────────────────────────── AI Tutor Conversation ──────────────────────────────


class TutorConversation(Base):
    __tablename__ = "tutor_conversations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    lesson_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    messages: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array of {role, content}
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)


# ────────────────────────────── LearningPath ──────────────────────────────


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    recommended_course_ids: Mapped[str] = mapped_column(Text, nullable=False)  # JSON array of course UUIDs
    skills_gap: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


# ────────────────────────────── ScormPackage ──────────────────────────────


class ScormPackage(Base):
    __tablename__ = "scorm_packages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(20), default="1.2")  # SCORM 1.2 or 2004
    manifest_xml: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    course_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("courses.id", ondelete="SET NULL"), nullable=True)
    imported_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)


class XApiStatement(Base):
    __tablename__ = "xapi_statements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    verb: Mapped[str] = mapped_column(String(100), nullable=False)  # completed, attempted, experienced
    object_id: Mapped[str] = mapped_column(String(512), nullable=False)  # course/lesson URI
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    stored_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
