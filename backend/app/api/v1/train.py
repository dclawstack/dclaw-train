"""
DClaw Train v1.2 API Router — all endpoints for courses, lessons, quizzes, progress,
AI tutor, analytics, learning paths, live sessions, certifications, badges,
skills assessment, discussion forums, SCORM/xAPI, and video summarization.
"""
import math
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.train import (
    CourseRepository, LessonRepository, ResourceRepository,
    QuizRepository, QuestionRepository, QuizAttemptRepository,
    EnrollmentRepository, LearnerProgressRepository,
    LiveSessionRepository, CertificateRepository, BadgeRepository,
    SkillAssessmentRepository,
    ForumTopicRepository, ForumReplyRepository,
    ScormPackageRepository, XApiStatementRepository,
)
from app.schemas.train import (
    CourseCreate, CourseUpdate, CourseResponse,
    LessonCreate, LessonUpdate, LessonResponse, LessonReorder,
    ResourceCreate, ResourceResponse,
    QuizCreate, QuizUpdate, QuizResponse,
    QuestionCreate, QuestionResponse,
    QuizGenerateRequest, QuizGenerateResponse,
    QuizAttemptCreate, QuizAttemptResponse,
    EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse,
    LearnerProgressCreate, LearnerProgressUpdate, LearnerProgressResponse,
    LearningPathRequest, LearningPathResponse, RecommendedCourse,
    LiveSessionCreate, LiveSessionUpdate, LiveSessionResponse,
    CertificateResponse, CertificateGenerateRequest,
    BadgeResponse, BadgeCreate,
    SkillAssessmentCreate, SkillAssessmentResponse, SkillsGapResponse,
    ForumTopicCreate, ForumTopicResponse,
    ForumReplyCreate, ForumReplyResponse,
    TutorRequest, TutorResponse,
    AnalyticsOverview, LearnerAnalytics, CourseAnalytics,
    VideoSummaryRequest, VideoSummaryResponse,
    ScormImportRequest, ScormPackageResponse,
    XApiStatementCreate,
    PaginatedResponse,
)
from app.services import (
    tutor_ai, quiz_ai, analytics, learning_path,
    course_builder, certifications, skills, forum,
    live_sessions as live_sessions_svc, scorm as scorm_svc,
    video_ai,
)

router = APIRouter()


# ────────────────────────────────────────────────────────────
#  Utility
# ────────────────────────────────────────────────────────────

def paginate(items: list, total: int, page: int, page_size: int) -> dict:
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": math.ceil(total / page_size) if page_size and total else 0,
    }


# ────────────────────────────────────────────────────────────
#  Courses
# ────────────────────────────────────────────────────────────

@router.post("/courses", response_model=CourseResponse, status_code=201)
async def create_course(payload: CourseCreate, db: AsyncSession = Depends(get_db)):
    repo = CourseRepository(db)
    course = CourseRepository.model(
        title=payload.title,
        description=payload.description,
        format=payload.format,
        thumbnail_url=payload.thumbnail_url,
        category=payload.category,
        tags=payload.tags,
        is_published=payload.is_published,
    )
    course = await repo.create(course)
    return CourseResponse(
        id=course.id,
        title=course.title,
        description=course.description,
        format=course.format.value if hasattr(course.format, 'value') else course.format,
        thumbnail_url=course.thumbnail_url,
        category=course.category,
        tags=course.tags,
        is_published=course.is_published,
        created_at=course.created_at,
        updated_at=course.updated_at,
    )


@router.get("/courses", response_model=PaginatedResponse)
async def list_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    published_only: bool = False,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    repo = CourseRepository(db)
    lesson_repo = LessonRepository(db)
    enrollment_repo = EnrollmentRepository(db)

    if search:
        items, total = await repo.search(search, limit=page_size, offset=(page - 1) * page_size)
    elif published_only:
        items, total = await repo.list_published(limit=page_size, offset=(page - 1) * page_size)
    else:
        items, total = await repo.list_all(limit=page_size, offset=(page - 1) * page_size)

    result = []
    for c in items:
        lesson_count = await lesson_repo.count_by_course(c.id)
        enrollment_count = await enrollment_repo.count_by_course(c.id)
        result.append(CourseResponse(
            id=c.id,
            title=c.title,
            description=c.description,
            format=c.format.value if hasattr(c.format, 'value') else c.format,
            thumbnail_url=c.thumbnail_url,
            category=c.category,
            tags=c.tags,
            is_published=c.is_published,
            created_at=c.created_at,
            updated_at=c.updated_at,
            lesson_count=lesson_count,
            enrollment_count=enrollment_count,
        ))
    return paginate(result, total, page, page_size)


@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = CourseRepository(db)
    lesson_repo = LessonRepository(db)
    enrollment_repo = EnrollmentRepository(db)

    c = await repo.get_by_id(course_id)
    if not c:
        raise HTTPException(404, "Course not found")

    return CourseResponse(
        id=c.id,
        title=c.title,
        description=c.description,
        format=c.format.value if hasattr(c.format, 'value') else c.format,
        thumbnail_url=c.thumbnail_url,
        category=c.category,
        tags=c.tags,
        is_published=c.is_published,
        created_at=c.created_at,
        updated_at=c.updated_at,
        lesson_count=await lesson_repo.count_by_course(c.id),
        enrollment_count=await enrollment_repo.count_by_course(c.id),
    )


@router.patch("/courses/{course_id}", response_model=CourseResponse)
async def update_course(course_id: UUID, payload: CourseUpdate, db: AsyncSession = Depends(get_db)):
    repo = CourseRepository(db)
    c = await repo.get_by_id(course_id)
    if not c:
        raise HTTPException(404, "Course not found")
    update_data = payload.model_dump(exclude_unset=True)
    if "format" in update_data and isinstance(update_data["format"], str):
        from app.models.train import TrainingFormat
        update_data["format"] = TrainingFormat(update_data["format"])
    c = await repo.update(course_id, **update_data)
    return CourseResponse(
        id=c.id, title=c.title, description=c.description,
        format=c.format.value if hasattr(c.format, 'value') else c.format,
        thumbnail_url=c.thumbnail_url, category=c.category, tags=c.tags,
        is_published=c.is_published, created_at=c.created_at, updated_at=c.updated_at,
    )


@router.delete("/courses/{course_id}", status_code=204)
async def delete_course(course_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = CourseRepository(db)
    c = await repo.get_by_id(course_id)
    if not c:
        raise HTTPException(404, "Course not found")
    await repo.delete(c)


# ────────────────────────────────────────────────────────────
#  Course Structure (Builder endpoint)
# ────────────────────────────────────────────────────────────

@router.get("/courses/{course_id}/structure")
async def get_course_structure(course_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await course_builder.get_course_structure(db, course_id)
    if not result:
        raise HTTPException(404, "Course not found")
    return result


@router.post("/courses/build")
async def build_course_with_lessons(
    title: str,
    description: Optional[str] = None,
    format: str = "Video",
    category: Optional[str] = None,
    tags: Optional[str] = None,
    lessons_data: list[dict] = [],
    db: AsyncSession = Depends(get_db),
):
    return await course_builder.create_course_with_lessons(
        db, title=title, description=description, format=format,
        lessons_data=lessons_data, category=category, tags=tags,
    )


# ────────────────────────────────────────────────────────────
#  Lessons
# ────────────────────────────────────────────────────────────

@router.post("/lessons", response_model=LessonResponse, status_code=201)
async def create_lesson(payload: LessonCreate, db: AsyncSession = Depends(get_db)):
    repo = LessonRepository(db)
    course_repo = CourseRepository(db)

    course = await course_repo.get_by_id(payload.course_id)
    if not course:
        raise HTTPException(404, "Course not found")

    lesson = LessonRepository.model(
        course_id=payload.course_id,
        title=payload.title,
        description=payload.description,
        content=payload.content,
        video_url=payload.video_url,
        duration_minutes=payload.duration_minutes,
        order=payload.order,
        is_published=payload.is_published,
    )
    lesson = await repo.create(lesson)
    return LessonResponse(
        id=lesson.id, course_id=lesson.course_id, title=lesson.title,
        description=lesson.description, content=lesson.content,
        video_url=lesson.video_url, video_transcript=lesson.video_transcript,
        video_summary=lesson.video_summary, video_chapters=lesson.video_chapters,
        duration_minutes=lesson.duration_minutes, order=lesson.order,
        is_published=lesson.is_published, created_at=lesson.created_at,
        updated_at=lesson.updated_at,
    )


@router.get("/courses/{course_id}/lessons", response_model=list[LessonResponse])
async def list_lessons(course_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = LessonRepository(db)
    lessons = await repo.list_by_course(course_id)
    return [
        LessonResponse(
            id=l.id, course_id=l.course_id, title=l.title, description=l.description,
            content=l.content, video_url=l.video_url, video_transcript=l.video_transcript,
            video_summary=l.video_summary, video_chapters=l.video_chapters,
            duration_minutes=l.duration_minutes, order=l.order, is_published=l.is_published,
            created_at=l.created_at, updated_at=l.updated_at,
        ) for l in lessons
    ]


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = LessonRepository(db)
    l = await repo.get_by_id(lesson_id)
    if not l:
        raise HTTPException(404, "Lesson not found")
    return LessonResponse(
        id=l.id, course_id=l.course_id, title=l.title, description=l.description,
        content=l.content, video_url=l.video_url, video_transcript=l.video_transcript,
        video_summary=l.video_summary, video_chapters=l.video_chapters,
        duration_minutes=l.duration_minutes, order=l.order, is_published=l.is_published,
        created_at=l.created_at, updated_at=l.updated_at,
    )


@router.patch("/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(lesson_id: UUID, payload: LessonUpdate, db: AsyncSession = Depends(get_db)):
    repo = LessonRepository(db)
    l = await repo.get_by_id(lesson_id)
    if not l:
        raise HTTPException(404, "Lesson not found")
    update_data = payload.model_dump(exclude_unset=True)
    l = await repo.update(lesson_id, **update_data)
    return LessonResponse(
        id=l.id, course_id=l.course_id, title=l.title, description=l.description,
        content=l.content, video_url=l.video_url, video_transcript=l.video_transcript,
        video_summary=l.video_summary, video_chapters=l.video_chapters,
        duration_minutes=l.duration_minutes, order=l.order, is_published=l.is_published,
        created_at=l.created_at, updated_at=l.updated_at,
    )


@router.delete("/lessons/{lesson_id}", status_code=204)
async def delete_lesson(lesson_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = LessonRepository(db)
    l = await repo.get_by_id(lesson_id)
    if not l:
        raise HTTPException(404, "Lesson not found")
    await repo.delete(l)


@router.post("/courses/{course_id}/lessons/reorder")
async def reorder_lessons(course_id: UUID, payload: LessonReorder, db: AsyncSession = Depends(get_db)):
    repo = LessonRepository(db)
    await repo.reorder(course_id, payload.lesson_ids)
    return {"status": "ok"}


# ────────────────────────────────────────────────────────────
#  Lesson Resources
# ────────────────────────────────────────────────────────────

@router.post("/resources", response_model=ResourceResponse, status_code=201)
async def add_resource(payload: ResourceCreate, db: AsyncSession = Depends(get_db)):
    repo = ResourceRepository(db)
    resource = ResourceRepository.model(
        lesson_id=payload.lesson_id, title=payload.title,
        resource_type=payload.resource_type, url=payload.url,
    )
    resource = await repo.create(resource)
    return ResourceResponse(
        id=resource.id, lesson_id=resource.lesson_id, title=resource.title,
        resource_type=resource.resource_type, url=resource.url,
        created_at=resource.created_at,
    )


@router.get("/lessons/{lesson_id}/resources", response_model=list[ResourceResponse])
async def list_resources(lesson_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = ResourceRepository(db)
    resources = await repo.list_by_lesson(lesson_id)
    return [
        ResourceResponse(
            id=r.id, lesson_id=r.lesson_id, title=r.title,
            resource_type=r.resource_type, url=r.url, created_at=r.created_at,
        ) for r in resources
    ]


# ────────────────────────────────────────────────────────────
#  Quizzes
# ────────────────────────────────────────────────────────────

@router.post("/quizzes", response_model=QuizResponse, status_code=201)
async def create_quiz(payload: QuizCreate, db: AsyncSession = Depends(get_db)):
    repo = QuizRepository(db)
    quiz = QuizRepository.model(
        lesson_id=payload.lesson_id, title=payload.title,
        description=payload.description, passing_score=payload.passing_score,
        time_limit_minutes=payload.time_limit_minutes, is_published=payload.is_published,
    )
    quiz = await repo.create(quiz)
    return QuizResponse(
        id=quiz.id, lesson_id=quiz.lesson_id, title=quiz.title,
        description=quiz.description, passing_score=quiz.passing_score,
        time_limit_minutes=quiz.time_limit_minutes, is_published=quiz.is_published,
        created_at=quiz.created_at, updated_at=quiz.updated_at,
    )


@router.get("/lessons/{lesson_id}/quizzes", response_model=list[QuizResponse])
async def list_quizzes(lesson_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = QuizRepository(db)
    q_repo = QuestionRepository(db)
    quizzes = await repo.list_by_lesson(lesson_id)
    result = []
    for quiz in quizzes:
        q_count = await q_repo.count_by_quiz(quiz.id)
        result.append(QuizResponse(
            id=quiz.id, lesson_id=quiz.lesson_id, title=quiz.title,
            description=quiz.description, passing_score=quiz.passing_score,
            time_limit_minutes=quiz.time_limit_minutes, is_published=quiz.is_published,
            question_count=q_count, created_at=quiz.created_at, updated_at=quiz.updated_at,
        ))
    return result


@router.patch("/quizzes/{quiz_id}", response_model=QuizResponse)
async def update_quiz(quiz_id: UUID, payload: QuizUpdate, db: AsyncSession = Depends(get_db)):
    repo = QuizRepository(db)
    quiz = await repo.get_by_id(quiz_id)
    if not quiz:
        raise HTTPException(404, "Quiz not found")
    update_data = payload.model_dump(exclude_unset=True)
    quiz = await repo.update(quiz_id, **update_data)
    return QuizResponse(
        id=quiz.id, lesson_id=quiz.lesson_id, title=quiz.title,
        description=quiz.description, passing_score=quiz.passing_score,
        time_limit_minutes=quiz.time_limit_minutes, is_published=quiz.is_published,
        created_at=quiz.created_at, updated_at=quiz.updated_at,
    )


# ────────────────────────────────────────────────────────────
#  AI Quiz Generation (P0.3)
# ────────────────────────────────────────────────────────────

@router.post("/ai/generate-quiz", response_model=QuizGenerateResponse)
async def generate_quiz(payload: QuizGenerateRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await quiz_ai.generate_quiz_from_lesson(
            db, payload.lesson_id, payload.num_questions,
            payload.difficulty, payload.question_types,
        )
        return QuizGenerateResponse(**result)
    except ValueError as e:
        raise HTTPException(400, str(e))


# ────────────────────────────────────────────────────────────
#  Questions
# ────────────────────────────────────────────────────────────

@router.post("/questions", response_model=QuestionResponse, status_code=201)
async def add_question(payload: QuestionCreate, db: AsyncSession = Depends(get_db)):
    repo = QuestionRepository(db)
    q = QuestionRepository.model(
        quiz_id=payload.quiz_id, question_type=payload.question_type,
        difficulty=payload.difficulty, text=payload.text,
        options=payload.options, correct_answer=payload.correct_answer,
        explanation=payload.explanation, points=payload.points, order=payload.order,
    )
    q = await repo.create(q)
    return QuestionResponse(
        id=q.id, quiz_id=q.quiz_id, question_type=q.question_type.value if hasattr(q.question_type, 'value') else q.question_type,
        difficulty=q.difficulty.value if hasattr(q.difficulty, 'value') else q.difficulty,
        text=q.text, options=q.options, correct_answer=q.correct_answer,
        explanation=q.explanation, points=q.points, order=q.order, created_at=q.created_at,
    )


@router.get("/quizzes/{quiz_id}/questions", response_model=list[QuestionResponse])
async def list_questions(quiz_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = QuestionRepository(db)
    questions = await repo.list_by_quiz(quiz_id)
    return [
        QuestionResponse(
            id=q.id, quiz_id=q.quiz_id,
            question_type=q.question_type.value if hasattr(q.question_type, 'value') else q.question_type,
            difficulty=q.difficulty.value if hasattr(q.difficulty, 'value') else q.difficulty,
            text=q.text, options=q.options,
            # Don't expose correct_answer in list view for students
            correct_answer="[hidden]",
            explanation=q.explanation, points=q.points, order=q.order, created_at=q.created_at,
        ) for q in questions
    ]


# ────────────────────────────────────────────────────────────
#  Quiz Attempts
# ────────────────────────────────────────────────────────────

@router.post("/quiz-attempts", response_model=QuizAttemptResponse, status_code=201)
async def submit_quiz_attempt(payload: QuizAttemptCreate, db: AsyncSession = Depends(get_db)):
    quiz_repo = QuizRepository(db)
    question_repo = QuestionRepository(db)
    attempt_repo = QuizAttemptRepository(db)

    quiz = await quiz_repo.get_by_id(payload.quiz_id)
    if not quiz:
        raise HTTPException(404, "Quiz not found")

    questions = await question_repo.list_by_quiz(payload.quiz_id)
    total_points = sum(q.points for q in questions)
    score = 0.0

    # Score the attempt
    answers_map = {str(a.question_id): a.answer for a in payload.answers}
    for q in questions:
        if str(q.id) in answers_map:
            if answers_map[str(q.id)].strip().lower() == q.correct_answer.strip().lower():
                score += q.points

    passed = score >= (quiz.passing_score / 100 * total_points) if total_points > 0 else False

    import json
    from datetime import datetime

    attempt = QuizAttemptRepository.model(
        quiz_id=payload.quiz_id, learner_id=payload.learner_id,
        score=score, total_points=total_points, passed=passed,
        answers=json.dumps(payload.model_dump()["answers"]),
        completed_at=datetime.utcnow(),
    )
    attempt = await attempt_repo.create(attempt)

    # Update learner progress if there's an enrollment
    # (simplified — in production, link via enrollment_id)

    return QuizAttemptResponse(
        id=attempt.id, quiz_id=attempt.quiz_id, learner_id=attempt.learner_id,
        score=attempt.score, total_points=attempt.total_points, passed=attempt.passed,
        started_at=attempt.started_at, completed_at=attempt.completed_at,
    )


@router.get("/learners/{learner_id}/quiz-attempts")
async def list_quiz_attempts(
    learner_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = QuizAttemptRepository(db)
    items, total = await repo.list_by_learner(learner_id, limit=page_size, offset=(page - 1) * page_size)
    result = [
        QuizAttemptResponse(
            id=a.id, quiz_id=a.quiz_id, learner_id=a.learner_id,
            score=a.score, total_points=a.total_points, passed=a.passed,
            started_at=a.started_at, completed_at=a.completed_at,
        ) for a in items
    ]
    return paginate(result, total, page, page_size)


# ────────────────────────────────────────────────────────────
#  Enrollments
# ────────────────────────────────────────────────────────────

@router.post("/enrollments", response_model=EnrollmentResponse, status_code=201)
async def enroll(payload: EnrollmentCreate, db: AsyncSession = Depends(get_db)):
    repo = EnrollmentRepository(db)
    course_repo = CourseRepository(db)

    course = await course_repo.get_by_id(payload.course_id)
    if not course:
        raise HTTPException(404, "Course not found")

    existing = await repo.get_by_course_and_learner(payload.course_id, payload.learner_id)
    if existing:
        return EnrollmentResponse(
            id=existing.id, course_id=existing.course_id, learner_id=existing.learner_id,
            status=existing.status.value if hasattr(existing.status, 'value') else existing.status,
            progress_percentage=existing.progress_percentage,
            enrolled_at=existing.enrolled_at, completed_at=existing.completed_at,
            last_accessed_at=existing.last_accessed_at,
        )

    enrollment = EnrollmentRepository.model(
        course_id=payload.course_id, learner_id=payload.learner_id,
    )
    enrollment = await repo.create(enrollment)
    return EnrollmentResponse(
        id=enrollment.id, course_id=enrollment.course_id, learner_id=enrollment.learner_id,
        status=enrollment.status.value if hasattr(enrollment.status, 'value') else enrollment.status,
        progress_percentage=enrollment.progress_percentage,
        enrolled_at=enrollment.enrolled_at, completed_at=enrollment.completed_at,
        last_accessed_at=enrollment.last_accessed_at,
    )


@router.get("/courses/{course_id}/enrollments", response_model=list[EnrollmentResponse])
async def list_enrollments(course_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = EnrollmentRepository(db)
    enrollments = await repo.list_by_course(course_id)
    return [
        EnrollmentResponse(
            id=e.id, course_id=e.course_id, learner_id=e.learner_id,
            status=e.status.value if hasattr(e.status, 'value') else e.status,
            progress_percentage=e.progress_percentage,
            enrolled_at=e.enrolled_at, completed_at=e.completed_at,
            last_accessed_at=e.last_accessed_at,
        ) for e in enrollments
    ]


@router.get("/learners/{learner_id}/enrollments", response_model=list[EnrollmentResponse])
async def list_learner_enrollments(learner_id: str, db: AsyncSession = Depends(get_db)):
    repo = EnrollmentRepository(db)
    enrollments = await repo.list_by_learner(learner_id)
    return [
        EnrollmentResponse(
            id=e.id, course_id=e.course_id, learner_id=e.learner_id,
            status=e.status.value if hasattr(e.status, 'value') else e.status,
            progress_percentage=e.progress_percentage,
            enrolled_at=e.enrolled_at, completed_at=e.completed_at,
            last_accessed_at=e.last_accessed_at,
        ) for e in enrollments
    ]


@router.patch("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(enrollment_id: UUID, payload: EnrollmentUpdate, db: AsyncSession = Depends(get_db)):
    repo = EnrollmentRepository(db)
    e = await repo.get_by_id(enrollment_id)
    if not e:
        raise HTTPException(404, "Enrollment not found")
    update_data = payload.model_dump(exclude_unset=True)
    e = await repo.update(enrollment_id, **update_data)
    return EnrollmentResponse(
        id=e.id, course_id=e.course_id, learner_id=e.learner_id,
        status=e.status.value if hasattr(e.status, 'value') else e.status,
        progress_percentage=e.progress_percentage,
        enrolled_at=e.enrolled_at, completed_at=e.completed_at,
        last_accessed_at=e.last_accessed_at,
    )


# ────────────────────────────────────────────────────────────
#  Learner Progress
# ────────────────────────────────────────────────────────────

@router.post("/progress", response_model=LearnerProgressResponse, status_code=201)
async def record_progress(payload: LearnerProgressCreate, db: AsyncSession = Depends(get_db)):
    repo = LearnerProgressRepository(db)
    enrollment_repo = EnrollmentRepository(db)

    enrollment = await enrollment_repo.get_by_id(payload.enrollment_id)
    if not enrollment:
        raise HTTPException(404, "Enrollment not found")

    # Check for existing progress record
    existing = await repo.get_by_enrollment_and_lesson(payload.enrollment_id, payload.lesson_id)
    if existing:
        # Update existing
        from datetime import datetime
        update_data = {"last_accessed_at": datetime.utcnow()}
        if payload.status:
            update_data["status"] = payload.status
        if payload.time_spent_seconds > 0:
            update_data["time_spent_seconds"] = existing.time_spent_seconds + payload.time_spent_seconds
        if payload.score is not None:
            update_data["score"] = payload.score
        if payload.status == "Completed":
            update_data["completed_at"] = datetime.utcnow()
        p = await repo.update(existing.id, **update_data)
        return LearnerProgressResponse(
            id=p.id, enrollment_id=p.enrollment_id, lesson_id=p.lesson_id,
            status=p.status, time_spent_seconds=p.time_spent_seconds,
            score=p.score, completed_at=p.completed_at, last_accessed_at=p.last_accessed_at,
        )

    p = LearnerProgressRepository.model(
        enrollment_id=payload.enrollment_id, lesson_id=payload.lesson_id,
        status=payload.status, time_spent_seconds=payload.time_spent_seconds,
        score=payload.score,
    )
    p = await repo.create(p)
    return LearnerProgressResponse(
        id=p.id, enrollment_id=p.enrollment_id, lesson_id=p.lesson_id,
        status=p.status, time_spent_seconds=p.time_spent_seconds,
        score=p.score, completed_at=p.completed_at, last_accessed_at=p.last_accessed_at,
    )


@router.get("/enrollments/{enrollment_id}/progress", response_model=list[LearnerProgressResponse])
async def list_progress(enrollment_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = LearnerProgressRepository(db)
    progress_list = await repo.list_by_enrollment(enrollment_id)
    return [
        LearnerProgressResponse(
            id=p.id, enrollment_id=p.enrollment_id, lesson_id=p.lesson_id,
            status=p.status, time_spent_seconds=p.time_spent_seconds,
            score=p.score, completed_at=p.completed_at, last_accessed_at=p.last_accessed_at,
        ) for p in progress_list
    ]


# ────────────────────────────────────────────────────────────
#  AI Tutor (P0.1)
# ────────────────────────────────────────────────────────────

@router.post("/ai/tutor", response_model=TutorResponse)
async def ask_tutor(payload: TutorRequest, db: AsyncSession = Depends(get_db)):
    result = await tutor_ai.get_tutor_response(
        db, payload.learner_id, payload.message,
        payload.lesson_id, payload.course_id,
    )
    return TutorResponse(**result)


# ────────────────────────────────────────────────────────────
#  Analytics (P0.4)
# ────────────────────────────────────────────────────────────

@router.get("/analytics/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(db: AsyncSession = Depends(get_db)):
    return await analytics.get_analytics_overview(db)


@router.get("/analytics/learners/{learner_id}", response_model=LearnerAnalytics)
async def get_learner_analytics(learner_id: str, db: AsyncSession = Depends(get_db)):
    return await analytics.get_learner_analytics(db, learner_id)


@router.get("/analytics/courses/{course_id}", response_model=CourseAnalytics)
async def get_course_analytics(course_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await analytics.get_course_analytics(db, course_id)
    if not result:
        raise HTTPException(404, "Course not found")
    return result


@router.get("/analytics/at-risk")
async def list_at_risk_learners(db: AsyncSession = Depends(get_db)):
    repo = LearnerProgressRepository(db)
    at_risk = await repo.get_at_risk_learners()
    return {"at_risk_learner_ids": at_risk, "count": len(at_risk)}


# ────────────────────────────────────────────────────────────
#  Learning Paths (P1.5)
# ────────────────────────────────────────────────────────────

@router.post("/learning-paths", response_model=LearningPathResponse)
async def generate_learning_path(payload: LearningPathRequest, db: AsyncSession = Depends(get_db)):
    result = await learning_path.generate_learning_path(
        db, payload.learner_id, payload.role, payload.career_goals,
    )
    return LearningPathResponse(**result)


@router.get("/learners/{learner_id}/learning-path", response_model=LearningPathResponse)
async def get_learning_path(learner_id: str, db: AsyncSession = Depends(get_db)):
    from app.repositories.train import LearningPathRepository
    repo = LearningPathRepository(db)
    import json
    path = await repo.get_latest_for_learner(learner_id)
    if not path:
        raise HTTPException(404, "No learning path found")
    recommended = json.loads(path.reasoning) if path.reasoning else []
    skills_gap = json.loads(path.skills_gap) if path.skills_gap else None
    return LearningPathResponse(
        id=path.id, learner_id=path.learner_id,
        recommended_courses=recommended, skills_gap=skills_gap,
        reasoning=path.reasoning, generated_at=path.generated_at,
    )


# ────────────────────────────────────────────────────────────
#  Live Sessions (P1.6)
# ────────────────────────────────────────────────────────────

@router.post("/live-sessions", response_model=LiveSessionResponse, status_code=201)
async def schedule_session(payload: LiveSessionCreate, db: AsyncSession = Depends(get_db)):
    result = await live_sessions_svc.schedule_session(
        db, payload.course_id, payload.title, payload.description,
        payload.session_url, payload.scheduled_at,
        payload.duration_minutes, payload.max_participants,
    )
    return LiveSessionResponse(
        id=UUID(result["id"]), course_id=UUID(result["course_id"]) if result["course_id"] else None,
        title=result["title"], description=None,
        session_url=result["session_url"], status="Scheduled",
        scheduled_at=payload.scheduled_at, duration_minutes=result["duration_minutes"],
    )


@router.get("/courses/{course_id}/sessions", response_model=list[LiveSessionResponse])
async def list_course_sessions(course_id: UUID, db: AsyncSession = Depends(get_db)):
    sessions = await live_sessions_svc.list_sessions_by_course(db, course_id)
    return [
        LiveSessionResponse(
            id=UUID(s["id"]), course_id=UUID(s["course_id"]) if s["course_id"] else None,
            title=s["title"], description=s.get("description"),
            session_url=s["session_url"], status=s["status"],
            scheduled_at=s["scheduled_at"], duration_minutes=s["duration_minutes"],
            recording_url=s.get("recording_url"), transcript=s.get("transcript"),
            max_participants=s.get("max_participants"), created_at=None,
        ) for s in sessions
    ]


@router.get("/live-sessions/upcoming", response_model=list[LiveSessionResponse])
async def list_upcoming_sessions(limit: int = Query(10, le=50), db: AsyncSession = Depends(get_db)):
    sessions = await live_sessions_svc.list_upcoming_sessions(db, limit)
    return [
        LiveSessionResponse(
            id=UUID(s["id"]), course_id=UUID(s["course_id"]) if s.get("course_id") else None,
            title=s["title"], description=None,
            session_url=s["session_url"], status="Scheduled",
            scheduled_at=s["scheduled_at"], duration_minutes=s["duration_minutes"],
        ) for s in sessions
    ]


@router.patch("/live-sessions/{session_id}", response_model=LiveSessionResponse)
async def update_session(session_id: UUID, payload: LiveSessionUpdate, db: AsyncSession = Depends(get_db)):
    repo = LiveSessionRepository(db)
    s = await repo.get_by_id(session_id)
    if not s:
        raise HTTPException(404, "Session not found")
    update_data = payload.model_dump(exclude_unset=True)
    s = await repo.update(session_id, **update_data)
    return LiveSessionResponse(
        id=s.id, course_id=s.course_id, title=s.title, description=s.description,
        session_url=s.session_url,
        status=s.status.value if hasattr(s.status, 'value') else s.status,
        scheduled_at=s.scheduled_at, duration_minutes=s.duration_minutes,
        recording_url=s.recording_url, transcript=s.transcript,
        max_participants=s.max_participants, created_at=s.created_at,
    )


# ────────────────────────────────────────────────────────────
#  Certifications & Badges (P1.7)
# ────────────────────────────────────────────────────────────

@router.post("/certificates/generate", response_model=CertificateResponse)
async def generate_certificate(payload: CertificateGenerateRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await certifications.issue_certificate(
            db, payload.course_id, payload.learner_id, payload.learner_name,
        )
        return CertificateResponse(
            id=UUID(result["id"]), course_id=UUID(result["course_id"]),
            learner_id=result["learner_id"], certificate_url=result["certificate_url"],
            issued_at=result["issued_at"], expires_at=result.get("expires_at"),
        )
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/learners/{learner_id}/certificates", response_model=list[CertificateResponse])
async def list_certificates(learner_id: str, db: AsyncSession = Depends(get_db)):
    certs = await certifications.get_learner_certificates(db, learner_id)
    return [
        CertificateResponse(
            id=UUID(c["id"]), course_id=UUID(c["course_id"]),
            learner_id=c["learner_id"], certificate_url=c["certificate_url"],
            issued_at=c["issued_at"], expires_at=c.get("expires_at"),
        ) for c in certs
    ]


@router.post("/badges", response_model=BadgeResponse, status_code=201)
async def award_badge_endpoint(payload: BadgeCreate, db: AsyncSession = Depends(get_db)):
    result = await certifications.award_badge(
        db, payload.learner_id, payload.badge_type,
        payload.course_id, payload.title, payload.description, payload.icon_url,
    )
    return BadgeResponse(
        id=UUID(result["id"]), learner_id=result["learner_id"],
        badge_type=result["badge_type"], course_id=UUID(result["course_id"]) if result.get("course_id") else None,
        title=result["title"], description=result.get("description"),
        icon_url=result.get("icon_url"), earned_at=result["earned_at"],
    )


@router.get("/learners/{learner_id}/badges", response_model=list[BadgeResponse])
async def list_badges(learner_id: str, db: AsyncSession = Depends(get_db)):
    badges = await certifications.get_learner_badges(db, learner_id)
    return [
        BadgeResponse(
            id=UUID(b["id"]), learner_id=b["learner_id"], badge_type=b["badge_type"],
            course_id=UUID(b["course_id"]) if b.get("course_id") else None,
            title=b["title"], description=b.get("description"),
            icon_url=b.get("icon_url"), earned_at=b["earned_at"],
        ) for b in badges
    ]


# ────────────────────────────────────────────────────────────
#  Skills Assessment (P1.8)
# ────────────────────────────────────────────────────────────

@router.post("/skills/assessment", response_model=SkillAssessmentResponse, status_code=201)
async def submit_assessment(payload: SkillAssessmentCreate, db: AsyncSession = Depends(get_db)):
    result = await skills.submit_assessment(
        db, payload.learner_id, payload.assessment_type,
        payload.skills_data, payload.course_id,
    )
    return SkillAssessmentResponse(
        id=UUID(result["id"]), learner_id=result["learner_id"],
        assessment_type=result["assessment_type"],
        course_id=payload.course_id,
        skills_data=str(result["skills_data"]),
        overall_score=result["overall_score"],
        completed_at=result["completed_at"],
    )


@router.get("/learners/{learner_id}/skills/gap", response_model=SkillsGapResponse)
async def get_skills_gap(
    learner_id: str,
    course_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db),
):
    result = await skills.get_skills_gap_analysis(db, learner_id, course_id)
    return SkillsGapResponse(**result)


# ────────────────────────────────────────────────────────────
#  Discussion Forums (P2.10)
# ────────────────────────────────────────────────────────────

@router.post("/forum/topics", response_model=ForumTopicResponse, status_code=201)
async def create_forum_topic(payload: ForumTopicCreate, db: AsyncSession = Depends(get_db)):
    result = await forum.create_topic(
        db, payload.course_id, payload.learner_id,
        payload.title, payload.content,
    )
    return ForumTopicResponse(
        id=UUID(result["id"]), course_id=payload.course_id,
        learner_id=result["learner_id"], title=result["title"],
        content=payload.content, is_pinned=False,
        created_at=None, updated_at=None,
    )


@router.get("/courses/{course_id}/forum/topics", response_model=list[ForumTopicResponse])
async def list_forum_topics(course_id: UUID, db: AsyncSession = Depends(get_db)):
    topics = await forum.list_topics_by_course(db, course_id)
    return [
        ForumTopicResponse(
            id=UUID(t["id"]), course_id=course_id,
            learner_id=t["learner_id"], title=t["title"],
            content=t["content"], is_pinned=t.get("is_pinned", False),
            reply_count=t.get("reply_count", 0),
            created_at=None, updated_at=None,
        ) for t in topics
    ]


@router.get("/forum/topics/{topic_id}")
async def get_forum_topic(topic_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await forum.get_topic_with_replies(db, topic_id)
    if not result:
        raise HTTPException(404, "Topic not found")
    return result


@router.post("/forum/replies", response_model=ForumReplyResponse, status_code=201)
async def reply_to_topic(payload: ForumReplyCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await forum.reply_to_topic(
            db, payload.topic_id, payload.learner_id, payload.content,
        )
        return ForumReplyResponse(
            id=UUID(result["id"]), topic_id=payload.topic_id,
            learner_id=result["learner_id"], content=payload.content,
            is_ai_response=False, created_at=result["created_at"],
        )
    except ValueError as e:
        raise HTTPException(404, str(e))


# ────────────────────────────────────────────────────────────
#  AI Video Summarization (P2.9)
# ────────────────────────────────────────────────────────────

@router.post("/ai/summarize-video", response_model=VideoSummaryResponse)
async def summarize_video(payload: VideoSummaryRequest, db: AsyncSession = Depends(get_db)):
    try:
        result = await video_ai.summarize_video(db, payload.lesson_id, payload.video_url)
        return VideoSummaryResponse(**result)
    except ValueError as e:
        raise HTTPException(400, str(e))


# ────────────────────────────────────────────────────────────
#  SCORM/xAPI (P2.11)
# ────────────────────────────────────────────────────────────

@router.post("/scorm/import", response_model=ScormPackageResponse, status_code=201)
async def import_scorm(payload: ScormImportRequest, db: AsyncSession = Depends(get_db)):
    result = await scorm_svc.import_scorm_package(
        db, payload.title, payload.version, payload.manifest_xml, payload.course_id,
    )
    return ScormPackageResponse(
        id=UUID(result["id"]), title=result["title"], version=result["version"],
        course_id=UUID(result["course_id"]) if result.get("course_id") else None,
        imported_at=result["imported_at"],
    )


@router.post("/scorm/export/{course_id}")
async def export_scorm(course_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await scorm_svc.export_scorm_package(db, course_id)
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/xapi/statements")
async def store_xapi_statement(payload: XApiStatementCreate, db: AsyncSession = Depends(get_db)):
    result = await scorm_svc.store_xapi_statement(
        db, payload.learner_id, payload.verb, payload.object_id,
        payload.result, payload.context,
    )
    return result


@router.get("/learners/{learner_id}/xapi/statements")
async def get_xapi_statements(
    learner_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    return await scorm_svc.get_xapi_statements(db, learner_id, page_size, (page - 1) * page_size)
