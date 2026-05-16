"""
Analytics service — progress aggregation, engagement scoring, at-risk detection.
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    CourseRepository, EnrollmentRepository, LearnerProgressRepository,
    QuizAttemptRepository,
)
from app.schemas.train import (
    AnalyticsOverview, LearnerAnalytics, CourseAnalytics,
)


async def get_analytics_overview(db: AsyncSession) -> AnalyticsOverview:
    """Get platform-wide analytics overview."""
    course_repo = CourseRepository(db)
    enrollment_repo = EnrollmentRepository(db)
    progress_repo = LearnerProgressRepository(db)

    total_courses = await course_repo.count()
    total_enrollments = await enrollment_repo.count_all()
    total_completions = await enrollment_repo.count_completed_all()
    avg_completion_rate = (total_completions / total_enrollments * 100) if total_enrollments > 0 else 0.0
    avg_score = await enrollment_repo.get_average_score()
    at_risk = await progress_repo.get_at_risk_learners()

    return AnalyticsOverview(
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_completions=total_completions,
        average_completion_rate=round(avg_completion_rate, 1),
        average_score=round(avg_score, 1),
        at_risk_learners=len(at_risk),
    )


async def get_learner_analytics(db: AsyncSession, learner_id: str) -> LearnerAnalytics:
    """Get analytics for a specific learner."""
    enrollment_repo = EnrollmentRepository(db)
    progress_repo = LearnerProgressRepository(db)
    attempt_repo = QuizAttemptRepository(db)

    enrollments = await enrollment_repo.list_by_learner(learner_id)
    courses_enrolled = len(enrollments)
    courses_completed = sum(1 for e in enrollments if e.status == "Completed")
    total_time = await progress_repo.get_total_time_by_learner(learner_id)
    avg_score = await progress_repo.get_average_score_by_learner(learner_id)

    # Engagement score: weighted combination of progress, time, and completion
    if courses_enrolled > 0:
        completion_ratio = courses_completed / courses_enrolled
        time_factor = min(total_time / (3600 * courses_enrolled), 1.0)  # Cap at 1 hour per course avg
        engagement_score = round((completion_ratio * 0.6 + time_factor * 0.2 + min(avg_score / 100, 1.0) * 0.2) * 100, 1)
    else:
        engagement_score = 0.0

    at_risk = engagement_score < 30.0

    return LearnerAnalytics(
        learner_id=learner_id,
        courses_enrolled=courses_enrolled,
        courses_completed=courses_completed,
        total_time_spent_hours=round(total_time / 3600, 1),
        average_score=round(avg_score, 1),
        engagement_score=engagement_score,
        at_risk=at_risk,
    )


async def get_course_analytics(db: AsyncSession, course_id: UUID) -> Optional[CourseAnalytics]:
    """Get analytics for a specific course."""
    course_repo = CourseRepository(db)
    enrollment_repo = EnrollmentRepository(db)
    progress_repo = LearnerProgressRepository(db)

    course = await course_repo.get_by_id(course_id)
    if not course:
        return None

    enrollment_count = await enrollment_repo.count_by_course(course_id)
    completion_count = await enrollment_repo.count_completed_by_course(course_id)
    completion_rate = (completion_count / enrollment_count * 100) if enrollment_count > 0 else 0.0
    avg_score = await enrollment_repo.get_average_score(course_id)

    # Average time to complete estimate
    from datetime import datetime, timedelta
    enrollments = await enrollment_repo.list_by_course(course_id)
    completed_times = []
    for e in enrollments:
        if e.status == "Completed" and e.completed_at and e.enrolled_at:
            delta = (e.completed_at - e.enrolled_at).days
            completed_times.append(delta)
    avg_days = sum(completed_times) / len(completed_times) if completed_times else 0.0

    return CourseAnalytics(
        course_id=course_id,
        title=course.title,
        enrollment_count=enrollment_count,
        completion_count=completion_count,
        completion_rate=round(completion_rate, 1),
        average_score=round(avg_score, 1),
        average_time_to_complete_days=round(avg_days, 1),
    )
