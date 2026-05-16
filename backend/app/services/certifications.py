"""
Certification & Badges service — PDF certificate generation and badge management.
"""
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    CertificateRepository, BadgeRepository, EnrollmentRepository,
    CourseRepository,
)
from app.models.train import Certificate, Badge, BadgeType


async def issue_certificate(
    db: AsyncSession,
    course_id: UUID,
    learner_id: str,
    learner_name: str,
) -> dict:
    """Issue a completion certificate for a learner."""
    cert_repo = CertificateRepository(db)
    enrollment_repo = EnrollmentRepository(db)
    course_repo = CourseRepository(db)

    # Verify enrollment is completed
    enrollment = await enrollment_repo.get_by_course_and_learner(course_id, learner_id)
    if not enrollment or enrollment.status != "Completed":
        raise ValueError("Learner has not completed this course")

    # Check for existing certificate
    existing = await cert_repo.get_by_course_and_learner(course_id, learner_id)
    if existing:
        return {
            "id": str(existing.id),
            "course_id": str(existing.course_id),
            "learner_id": existing.learner_id,
            "certificate_url": existing.certificate_url,
            "issued_at": str(existing.issued_at),
            "expires_at": str(existing.expires_at) if existing.expires_at else None,
        }

    course = await course_repo.get_by_id(course_id)

    # In production: generate actual PDF certificate
    certificate_url = f"https://train.dclawstack.io/certificates/{learner_id}/{course_id}"

    cert = Certificate(
        id=uuid.uuid4(),
        course_id=course_id,
        learner_id=learner_id,
        certificate_url=certificate_url,
        expires_at=datetime.utcnow() + timedelta(days=365 * 3),  # 3 year validity
        cert_metadata=json.dumps({
            "learner_name": learner_name,
            "course_title": course.title if course else "Unknown",
            "completion_date": str(enrollment.completed_at),
        }),
    )
    cert = await cert_repo.create(cert)

    # Auto-award completion badge
    await _award_badge(
        db, learner_id, BadgeType.COMPLETION, course_id,
        f"Completed: {course.title if course else 'Course'}",
        "Awarded for completing this course",
    )

    return {
        "id": str(cert.id),
        "course_id": str(cert.course_id),
        "learner_id": cert.learner_id,
        "certificate_url": cert.certificate_url,
        "issued_at": str(cert.issued_at),
        "expires_at": str(cert.expires_at) if cert.expires_at else None,
    }


async def award_badge(
    db: AsyncSession,
    learner_id: str,
    badge_type: str,
    course_id: Optional[UUID] = None,
    title: str = "",
    description: Optional[str] = None,
    icon_url: Optional[str] = None,
) -> dict:
    """Award a badge to a learner."""
    badge = await _award_badge(db, learner_id, badge_type, course_id, title, description, icon_url)
    return {
        "id": str(badge.id),
        "learner_id": badge.learner_id,
        "badge_type": badge.badge_type.value if hasattr(badge.badge_type, 'value') else badge.badge_type,
        "title": badge.title,
        "description": badge.description,
        "earned_at": str(badge.earned_at),
    }


async def _award_badge(
    db: AsyncSession,
    learner_id: str,
    badge_type: str,
    course_id: Optional[UUID] = None,
    title: str = "",
    description: Optional[str] = None,
    icon_url: Optional[str] = None,
) -> Badge:
    badge_repo = BadgeRepository(db)

    badge = Badge(
        id=uuid.uuid4(),
        learner_id=learner_id,
        badge_type=badge_type,
        course_id=course_id,
        title=title or f"{badge_type.replace('_', ' ').title()} Badge",
        description=description,
        icon_url=icon_url,
    )
    return await badge_repo.create(badge)


async def get_learner_certificates(db: AsyncSession, learner_id: str) -> list[dict]:
    """Get all certificates for a learner."""
    cert_repo = CertificateRepository(db)
    certs = await cert_repo.list_by_learner(learner_id)
    return [
        {
            "id": str(c.id),
            "course_id": str(c.course_id),
            "learner_id": c.learner_id,
            "certificate_url": c.certificate_url,
            "issued_at": str(c.issued_at),
            "expires_at": str(c.expires_at) if c.expires_at else None,
        }
        for c in certs
    ]


async def get_learner_badges(db: AsyncSession, learner_id: str) -> list[dict]:
    """Get all badges for a learner."""
    badge_repo = BadgeRepository(db)
    badges = await badge_repo.list_by_learner(learner_id)
    return [
        {
            "id": str(b.id),
            "learner_id": b.learner_id,
            "badge_type": b.badge_type.value if hasattr(b.badge_type, 'value') else b.badge_type,
            "course_id": str(b.course_id) if b.course_id else None,
            "title": b.title,
            "description": b.description,
            "icon_url": b.icon_url,
            "earned_at": str(b.earned_at),
        }
        for b in badges
    ]
