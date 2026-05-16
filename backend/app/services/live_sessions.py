"""
Live Session & Webinar Management — scheduling, reminders, recording, transcription.
"""
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import LiveSessionRepository, CourseRepository
from app.models.train import LiveSession, SessionStatus


async def schedule_session(
    db: AsyncSession,
    course_id: Optional[UUID],
    title: str,
    description: Optional[str],
    session_url: Optional[str],
    scheduled_at: datetime,
    duration_minutes: int = 60,
    max_participants: Optional[int] = None,
) -> dict:
    """Schedule a new live session."""
    session_repo = LiveSessionRepository(db)

    # Generate a session URL if not provided
    if not session_url:
        session_url = f"https://meet.dclawstack.io/session/{uuid.uuid4().hex[:12]}"

    session = LiveSession(
        id=uuid.uuid4(),
        course_id=course_id,
        title=title,
        description=description,
        session_url=session_url,
        scheduled_at=scheduled_at,
        duration_minutes=duration_minutes,
        max_participants=max_participants,
    )
    session = await session_repo.create(session)

    # In production: send email reminders, create calendar invites

    return {
        "id": str(session.id),
        "course_id": str(session.course_id) if session.course_id else None,
        "title": session.title,
        "session_url": session.session_url,
        "scheduled_at": str(session.scheduled_at),
        "duration_minutes": session.duration_minutes,
    }


async def update_session_status(
    db: AsyncSession,
    session_id: UUID,
    status: str,
    recording_url: Optional[str] = None,
    transcript: Optional[str] = None,
) -> Optional[dict]:
    """Update session status and optionally attach recording/transcript."""
    session_repo = LiveSessionRepository(db)

    session = await session_repo.get_by_id(session_id)
    if not session:
        return None

    updates = {"status": status}
    if recording_url:
        updates["recording_url"] = recording_url
    if transcript:
        updates["transcript"] = transcript

    await session_repo.update(session_id, **updates)

    # If completed, store transcript and generate summary
    if status == "Completed" and not transcript:
        # In production: transcribe recording with Whisper
        pass

    return {
        "id": str(session.id),
        "title": session.title,
        "status": status,
        "recording_url": recording_url,
    }


async def list_sessions_by_course(db: AsyncSession, course_id: UUID) -> list[dict]:
    """List all sessions for a course."""
    session_repo = LiveSessionRepository(db)
    sessions = await session_repo.list_by_course(course_id)
    return [
        {
            "id": str(s.id),
            "course_id": str(s.course_id) if s.course_id else None,
            "title": s.title,
            "description": s.description,
            "session_url": s.session_url,
            "status": s.status.value if hasattr(s.status, 'value') else s.status,
            "scheduled_at": str(s.scheduled_at),
            "duration_minutes": s.duration_minutes,
            "recording_url": s.recording_url,
            "transcript": s.transcript[:200] if s.transcript else None,
            "max_participants": s.max_participants,
        }
        for s in sessions
    ]


async def list_upcoming_sessions(db: AsyncSession, limit: int = 10) -> list[dict]:
    """List upcoming scheduled sessions."""
    session_repo = LiveSessionRepository(db)
    sessions = await session_repo.list_upcoming(limit)
    return [
        {
            "id": str(s.id),
            "title": s.title,
            "course_id": str(s.course_id) if s.course_id else None,
            "scheduled_at": str(s.scheduled_at),
            "duration_minutes": s.duration_minutes,
            "session_url": s.session_url,
        }
        for s in sessions
    ]
