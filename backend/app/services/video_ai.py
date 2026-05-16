"""
AI Video Summarization — generates summaries, chapter markers, and searchable transcripts.
"""
import json
import uuid
from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import LessonRepository


# In production, use Whisper for transcription + LLM for summarization


async def summarize_video(
    db: AsyncSession,
    lesson_id: UUID,
    video_url: Optional[str] = None,
) -> dict:
    """Generate video summary, chapters, and transcript."""
    lesson_repo = LessonRepository(db)

    lesson = await lesson_repo.get_by_id(lesson_id)
    if not lesson:
        raise ValueError(f"Lesson {lesson_id} not found")

    # In production:
    # 1. Download/stream video from video_url or lesson.video_url
    # 2. Transcribe with Whisper
    # 3. Summarize with LLM
    # 4. Generate chapter markers

    # Simulated response
    transcript = (
        f"Welcome to {lesson.title}. "
        f"In this lesson, we cover the key concepts and practical applications. "
        f"First, we'll introduce the fundamental principles. "
        f"Then, we'll explore real-world examples and case studies. "
        f"Finally, we'll discuss best practices and common pitfalls to avoid. "
        f"{lesson.description or ''}"
    )

    summary = (
        f"This lesson on '{lesson.title}' covers the essential concepts including "
        f"fundamental principles, practical applications, and best practices. "
        f"Key takeaways: understand the core concepts, apply them in real scenarios, "
        f"and avoid common mistakes."
    )

    chapters = [
        {"title": "Introduction", "timestamp": "00:00", "description": "Overview and learning objectives"},
        {"title": "Core Concepts", "timestamp": "02:30", "description": "Fundamental principles explained"},
        {"title": "Practical Examples", "timestamp": "08:00", "description": "Real-world case studies"},
        {"title": "Best Practices", "timestamp": "15:00", "description": "Do's and don'ts"},
        {"title": "Summary", "timestamp": "20:00", "description": "Key takeaways and next steps"},
    ]

    # Update lesson with generated content
    await lesson_repo.update(
        lesson_id,
        video_transcript=transcript,
        video_summary=summary,
        video_chapters=json.dumps(chapters),
    )

    return {
        "lesson_id": str(lesson_id),
        "summary": summary,
        "chapters": chapters,
        "transcript": transcript,
    }
