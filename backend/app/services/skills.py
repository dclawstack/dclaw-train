"""
Skills Assessment & Gap Analysis service.
"""
import json
import uuid
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    SkillAssessmentRepository, CourseRepository,
)
from app.models.train import SkillAssessment


async def submit_assessment(
    db: AsyncSession,
    learner_id: str,
    assessment_type: str,  # pre, post
    skills_data: dict,
    course_id: Optional[UUID] = None,
) -> dict:
    """Submit a skills assessment."""
    assessment_repo = SkillAssessmentRepository(db)

    overall_score = sum(skills_data.values()) / len(skills_data) if skills_data else 0.0

    assessment = SkillAssessment(
        id=uuid.uuid4(),
        learner_id=learner_id,
        assessment_type=assessment_type,
        course_id=course_id,
        skills_data=json.dumps(skills_data),
        overall_score=round(overall_score, 1),
    )
    assessment = await assessment_repo.create(assessment)

    return {
        "id": str(assessment.id),
        "learner_id": assessment.learner_id,
        "assessment_type": assessment.assessment_type,
        "skills_data": skills_data,
        "overall_score": assessment.overall_score,
        "completed_at": str(assessment.completed_at),
    }


async def get_skills_gap_analysis(
    db: AsyncSession,
    learner_id: str,
    course_id: Optional[UUID] = None,
) -> dict:
    """Analyze skills gap between pre and post assessments."""
    assessment_repo = SkillAssessmentRepository(db)

    pre_assessments = await assessment_repo.get_by_learner_and_type(
        learner_id, "pre", course_id
    )
    post_assessments = await assessment_repo.get_by_learner_and_type(
        learner_id, "post", course_id
    )

    pre_data = None
    post_data = None
    improvements = None
    gaps = None

    if pre_assessments:
        latest_pre = pre_assessments[0]
        pre_data = json.loads(latest_pre.skills_data)

    if post_assessments:
        latest_post = post_assessments[0]
        post_data = json.loads(latest_post.skills_data)

    if pre_data and post_data:
        improvements = {}
        gaps = {}
        all_skills = set(list(pre_data.keys()) + list(post_data.keys()))
        for skill in all_skills:
            pre_score = pre_data.get(skill, 0)
            post_score = post_data.get(skill, 0)
            improvements[skill] = round(post_score - pre_score, 1)
            gaps[skill] = round(max(0, 80 - post_score), 1)  # Target: 80%

    return {
        "learner_id": learner_id,
        "pre_assessment": pre_data,
        "post_assessment": post_data,
        "improvements": improvements,
        "gaps": gaps,
    }
