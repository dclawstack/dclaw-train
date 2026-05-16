"""
AI Learning Path recommendation engine.
Recommends courses based on role, skills gaps, and career goals.
"""
import json
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    LearningPathRepository, CourseRepository, EnrollmentRepository,
    SkillAssessmentRepository,
)
from app.models.train import LearningPath


async def generate_learning_path(
    db: AsyncSession,
    learner_id: str,
    role: Optional[str] = None,
    career_goals: Optional[list[str]] = None,
) -> dict:
    """Generate personalized learning path recommendations."""
    course_repo = CourseRepository(db)
    enrollment_repo = EnrollmentRepository(db)
    assessment_repo = SkillAssessmentRepository(db)
    path_repo = LearningPathRepository(db)

    # Get learner's current enrollments
    enrollments = await enrollment_repo.list_by_learner(learner_id)
    enrolled_course_ids = {str(e.course_id) for e in enrollments}
    completed_course_ids = {str(e.course_id) for e in enrollments if e.status == "Completed"}

    # Get skills gaps from assessments
    skill_gaps = {}
    pre_assessments = await assessment_repo.get_by_learner_and_type(learner_id, "pre")
    if pre_assessments:
        latest_pre = pre_assessments[0]
        skills_data = json.loads(latest_pre.skills_data)
        for skill, score in skills_data.items():
            if score < 70:
                skill_gaps[skill] = 70 - score

    # Get available courses
    courses, _ = await course_repo.list_published(limit=50)

    # Recommend courses (in production, use LLM for intelligent matching)
    recommended = []
    for course in courses:
        course_id_str = str(course.id)
        if course_id_str in completed_course_ids:
            continue
        if course_id_str in enrolled_course_ids:
            continue

        # Simple content-based recommendation
        reasons = []
        if course.category:
            if role and role.lower() in (course.category or "").lower():
                reasons.append(f"Relevant for your {role} role")
            if career_goals:
                for goal in career_goals:
                    if goal.lower() in (course.category or "").lower() or goal.lower() in (course.title or "").lower():
                        reasons.append(f"Aligns with your career goal: {goal}")

        if course.title and any(
            gap.lower() in course.title.lower() for gap in skill_gaps
        ):
            reasons.append("Addresses a skill gap identified in your assessment")

        if not reasons:
            reasons.append("Popular course in your field")

        course_id_str = str(course.id)
        if course_id_str not in enrolled_course_ids:
            recommended.append({
                "course_id": str(course.id),
                "title": course.title,
                "reason": "; ".join(reasons),
                "priority": 1 if "skill gap" in reasons[0].lower() else 2,
            })

    # Sort by priority
    recommended.sort(key=lambda x: x["priority"])

    # Store the learning path
    path = LearningPath(
        id=uuid.uuid4(),
        learner_id=learner_id,
        recommended_course_ids=json.dumps([r["course_id"] for r in recommended[:10]]),
        skills_gap=json.dumps(skill_gaps) if skill_gaps else None,
        reasoning=json.dumps(recommended[:10]),
    )
    path = await path_repo.create(path)

    return {
        "id": path.id,
        "learner_id": learner_id,
        "recommended_courses": recommended[:10],
        "skills_gap": skill_gaps if skill_gaps else None,
        "reasoning": f"Based on your {role or 'learning'} profile and {len(skill_gaps)} identified skill gaps",
        "generated_at": path.generated_at,
    }
