from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ────────────────────────────── Course ──────────────────────────────

class CourseBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    format: str = "Video"  # Video, Quiz, Workshop, Document, Assignment
    thumbnail_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_published: bool = False


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    format: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class CourseResponse(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime
    updated_at: datetime
    lesson_count: Optional[int] = 0
    enrollment_count: Optional[int] = 0


# ────────────────────────────── Lesson ──────────────────────────────

class LessonBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    video_transcript: Optional[str] = None
    video_summary: Optional[str] = None
    video_chapters: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: int = 0
    is_published: bool = False


class LessonCreate(LessonBase):
    course_id: UUID


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    video_transcript: Optional[str] = None
    video_summary: Optional[str] = None
    video_chapters: Optional[str] = None
    duration_minutes: Optional[int] = None
    order: Optional[int] = None
    is_published: Optional[bool] = None


class LessonResponse(LessonBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    course_id: UUID
    created_at: datetime
    updated_at: datetime


class LessonReorder(BaseModel):
    lesson_ids: List[UUID]  # ordered list of lesson IDs


# ────────────────────────────── Lesson Resource ──────────────────────────────

class ResourceBase(BaseModel):
    title: str = Field(..., max_length=255)
    resource_type: str  # pdf, link, image, file
    url: str


class ResourceCreate(ResourceBase):
    lesson_id: UUID


class ResourceResponse(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    lesson_id: UUID
    created_at: datetime


# ────────────────────────────── Quiz ──────────────────────────────

class QuizBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    passing_score: float = 70.0
    time_limit_minutes: Optional[int] = None
    is_published: bool = False


class QuizCreate(QuizBase):
    lesson_id: UUID


class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    passing_score: Optional[float] = None
    time_limit_minutes: Optional[int] = None
    is_published: Optional[bool] = None


class QuizResponse(QuizBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    lesson_id: UUID
    question_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime


# ────────────────────────────── Question ──────────────────────────────

class QuestionBase(BaseModel):
    question_type: str = "multiple_choice"  # multiple_choice, true_false, short_answer, essay
    difficulty: str = "medium"  # easy, medium, hard
    text: str
    options: Optional[str] = None  # JSON array string
    correct_answer: str
    explanation: Optional[str] = None
    points: float = 1.0
    order: int = 0


class QuestionCreate(QuestionBase):
    quiz_id: UUID


class QuestionResponse(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    quiz_id: UUID
    created_at: datetime


class QuizGenerateRequest(BaseModel):
    lesson_id: UUID
    num_questions: int = 5
    difficulty: str = "medium"
    question_types: Optional[List[str]] = None  # e.g., ["multiple_choice", "true_false"]


class QuizGenerateResponse(BaseModel):
    quiz_id: UUID
    questions: List[QuestionResponse]


# ────────────────────────────── Quiz Attempt ──────────────────────────────

class Answer(BaseModel):
    question_id: UUID
    answer: str


class QuizAttemptCreate(BaseModel):
    quiz_id: UUID
    learner_id: str
    answers: List[Answer]


class QuizAttemptResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    quiz_id: UUID
    learner_id: str
    score: float
    total_points: float
    passed: bool
    started_at: datetime
    completed_at: Optional[datetime] = None


# ────────────────────────────── Enrollment ──────────────────────────────

class EnrollmentCreate(BaseModel):
    course_id: UUID
    learner_id: str


class EnrollmentUpdate(BaseModel):
    status: Optional[str] = None


class EnrollmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    course_id: UUID
    learner_id: str
    status: str
    progress_percentage: float
    enrolled_at: datetime
    completed_at: Optional[datetime] = None
    last_accessed_at: datetime


# ────────────────────────────── Learner Progress ──────────────────────────────

class LearnerProgressCreate(BaseModel):
    enrollment_id: UUID
    lesson_id: UUID
    status: str = "Not Started"
    time_spent_seconds: int = 0
    score: Optional[float] = None


class LearnerProgressUpdate(BaseModel):
    status: Optional[str] = None
    time_spent_seconds: Optional[int] = None
    score: Optional[float] = None


class LearnerProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    enrollment_id: UUID
    lesson_id: UUID
    status: str
    time_spent_seconds: int
    score: Optional[float] = None
    completed_at: Optional[datetime] = None
    last_accessed_at: datetime


# ────────────────────────────── Learning Path ──────────────────────────────

class LearningPathRequest(BaseModel):
    learner_id: str
    role: Optional[str] = None
    career_goals: Optional[List[str]] = None


class RecommendedCourse(BaseModel):
    course_id: UUID
    title: str
    reason: str
    priority: int  # 1=highest


class LearningPathResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    learner_id: str
    recommended_courses: Optional[List[RecommendedCourse]] = None
    skills_gap: Optional[dict] = None
    reasoning: Optional[str] = None
    generated_at: datetime


# ────────────────────────────── Live Session ──────────────────────────────

class LiveSessionCreate(BaseModel):
    course_id: Optional[UUID] = None
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    session_url: Optional[str] = None
    scheduled_at: datetime
    duration_minutes: int = 60
    max_participants: Optional[int] = None


class LiveSessionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    session_url: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    recording_url: Optional[str] = None
    transcript: Optional[str] = None


class LiveSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    course_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    session_url: Optional[str] = None
    status: str
    scheduled_at: datetime
    duration_minutes: int
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    max_participants: Optional[int] = None
    created_at: datetime


# ────────────────────────────── Certificate ──────────────────────────────

class CertificateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    course_id: UUID
    learner_id: str
    certificate_url: Optional[str] = None
    issued_at: datetime
    expires_at: Optional[datetime] = None


class CertificateGenerateRequest(BaseModel):
    course_id: UUID
    learner_id: str
    learner_name: str


# ────────────────────────────── Badge ──────────────────────────────

class BadgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    learner_id: str
    badge_type: str
    course_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    earned_at: datetime


class BadgeCreate(BaseModel):
    learner_id: str
    badge_type: str
    course_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    icon_url: Optional[str] = None


# ────────────────────────────── AI Tutor ──────────────────────────────

class TutorRequest(BaseModel):
    learner_id: str
    lesson_id: Optional[UUID] = None
    course_id: Optional[UUID] = None
    message: str


class TutorResponse(BaseModel):
    reply: str
    conversation_id: UUID
    suggested_questions: Optional[List[str]] = None


# ────────────────────────────── AI Video ──────────────────────────────

class VideoSummaryRequest(BaseModel):
    lesson_id: UUID
    video_url: Optional[str] = None


class VideoSummaryResponse(BaseModel):
    lesson_id: UUID
    summary: str
    chapters: Optional[List[dict]] = None  # [{title, timestamp}]
    transcript: Optional[str] = None


# ────────────────────────────── Analytics ──────────────────────────────

class AnalyticsOverview(BaseModel):
    total_courses: int
    total_enrollments: int
    total_completions: int
    average_completion_rate: float
    average_score: float
    at_risk_learners: int


class LearnerAnalytics(BaseModel):
    learner_id: str
    courses_enrolled: int
    courses_completed: int
    total_time_spent_hours: float
    average_score: float
    engagement_score: float  # 0-100
    at_risk: bool


class CourseAnalytics(BaseModel):
    course_id: UUID
    title: str
    enrollment_count: int
    completion_count: int
    completion_rate: float
    average_score: float
    average_time_to_complete_days: float


# ────────────────────────────── Skills ──────────────────────────────

class SkillAssessmentCreate(BaseModel):
    learner_id: str
    assessment_type: str  # pre, post
    course_id: Optional[UUID] = None
    skills_data: dict  # {skill_name: score}
    overall_score: float = 0.0


class SkillAssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    learner_id: str
    assessment_type: str
    course_id: Optional[UUID] = None
    skills_data: str  # JSON string
    overall_score: float
    completed_at: datetime


class SkillsGapResponse(BaseModel):
    learner_id: str
    pre_assessment: Optional[dict] = None
    post_assessment: Optional[dict] = None
    improvements: Optional[dict] = None  # {skill_name: improvement_pct}
    gaps: Optional[dict] = None  # {skill_name: gap_to_target}


# ────────────────────────────── Forum ──────────────────────────────

class ForumTopicCreate(BaseModel):
    course_id: UUID
    learner_id: str
    title: str = Field(..., max_length=255)
    content: str


class ForumTopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    course_id: UUID
    learner_id: str
    title: str
    content: str
    is_pinned: bool
    reply_count: Optional[int] = 0
    created_at: datetime
    updated_at: datetime


class ForumReplyCreate(BaseModel):
    topic_id: UUID
    learner_id: str
    content: str


class ForumReplyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    topic_id: UUID
    learner_id: str
    content: str
    is_ai_response: bool
    created_at: datetime


# ────────────────────────────── SCORM ──────────────────────────────

class ScormImportRequest(BaseModel):
    title: str
    version: str = "1.2"
    manifest_xml: Optional[str] = None
    course_id: Optional[UUID] = None


class ScormPackageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    version: str
    course_id: Optional[UUID] = None
    imported_at: datetime


class XApiStatementCreate(BaseModel):
    learner_id: str
    verb: str
    object_id: str
    result: Optional[dict] = None
    context: Optional[dict] = None


# ────────────────────────────── Pagination ──────────────────────────────

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    pages: int
