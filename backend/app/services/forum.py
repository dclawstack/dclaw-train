"""
Discussion Forum service — course-specific forums with AI moderation.
"""
import uuid
from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    ForumTopicRepository, ForumReplyRepository, CourseRepository,
)
from app.models.train import ForumTopic, ForumReply


async def create_topic(
    db: AsyncSession,
    course_id: UUID,
    learner_id: str,
    title: str,
    content: str,
) -> dict:
    """Create a new forum topic."""
    topic_repo = ForumTopicRepository(db)
    course_repo = CourseRepository(db)

    course = await course_repo.get_by_id(course_id)
    if not course:
        raise ValueError(f"Course {course_id} not found")

    # AI moderation check (in production: flag inappropriate content)
    is_safe = _moderate_content(title + " " + content)

    topic = ForumTopic(
        id=uuid.uuid4(),
        course_id=course_id,
        learner_id=learner_id,
        title=title,
        content=content,
        is_ai_moderated=not is_safe,
    )
    topic = await topic_repo.create(topic)

    # Auto AI response for common questions
    if "?" in content:
        ai_reply = _generate_ai_reply(content, course.title if course else "")
        reply_repo = ForumReplyRepository(db)
        ai_response = ForumReply(
            id=uuid.uuid4(),
            topic_id=topic.id,
            learner_id="ai-assistant",
            content=ai_reply,
            is_ai_response=True,
        )
        await reply_repo.create(ai_response)

    return {
        "id": str(topic.id),
        "title": topic.title,
        "learner_id": topic.learner_id,
        "ai_moderated": topic.is_ai_moderated,
    }


async def reply_to_topic(
    db: AsyncSession,
    topic_id: UUID,
    learner_id: str,
    content: str,
) -> dict:
    """Reply to a forum topic."""
    reply_repo = ForumReplyRepository(db)
    topic_repo = ForumTopicRepository(db)

    topic = await topic_repo.get_by_id(topic_id)
    if not topic:
        raise ValueError(f"Topic {topic_id} not found")

    is_safe = _moderate_content(content)

    reply = ForumReply(
        id=uuid.uuid4(),
        topic_id=topic_id,
        learner_id=learner_id,
        content=content,
    )
    reply = await reply_repo.create(reply)

    return {
        "id": str(reply.id),
        "topic_id": str(topic_id),
        "learner_id": learner_id,
        "created_at": str(reply.created_at),
    }


async def get_topic_with_replies(db: AsyncSession, topic_id: UUID) -> Optional[dict]:
    """Get a topic with all its replies."""
    topic_repo = ForumTopicRepository(db)
    reply_repo = ForumReplyRepository(db)

    topic = await topic_repo.get_by_id(topic_id)
    if not topic:
        return None

    replies = await reply_repo.list_by_topic(topic_id)

    return {
        "id": str(topic.id),
        "course_id": str(topic.course_id),
        "learner_id": topic.learner_id,
        "title": topic.title,
        "content": topic.content,
        "is_pinned": topic.is_pinned,
        "created_at": str(topic.created_at),
        "replies": [
            {
                "id": str(r.id),
                "learner_id": r.learner_id,
                "content": r.content,
                "is_ai_response": r.is_ai_response,
                "created_at": str(r.created_at),
            }
            for r in replies
        ],
    }


async def list_topics_by_course(db: AsyncSession, course_id: UUID) -> list[dict]:
    """List all topics for a course."""
    topic_repo = ForumTopicRepository(db)
    reply_repo = ForumReplyRepository(db)

    topics = await topic_repo.list_by_course(course_id)

    result = []
    for t in topics:
        replies = await reply_repo.list_by_topic(t.id)
        result.append({
            "id": str(t.id),
            "learner_id": t.learner_id,
            "title": t.title,
            "content": t.content[:200],
            "is_pinned": t.is_pinned,
            "reply_count": len(replies),
            "created_at": str(t.created_at),
        })
    return result


def _moderate_content(text: str) -> bool:
    """Simple content moderation. In production, use LLM-based moderation."""
    prohibited_words = []  # Add prohibited words here
    text_lower = text.lower()
    return not any(word in text_lower for word in prohibited_words)


def _generate_ai_reply(question: str, course_title: str) -> str:
    """Generate AI reply for forum questions."""
    question_lower = question.lower()
    if "how" in question_lower:
        return f"Great question! Here's how you can approach this: First, review the relevant lesson material in '{course_title}'. Then, try breaking the problem down into smaller steps. If you're still stuck, I'd recommend reaching out to your instructor or checking the course resources."
    elif "what" in question_lower:
        return f"Based on the '{course_title}' materials, the key concept you're asking about is covered in the lessons. I'd suggest reviewing the lesson content and checking the provided examples. Feel free to ask more specific questions!"
    else:
        return f"Thanks for your question! The '{course_title}' course materials should help address this. If you need more specific guidance, please provide additional context about what you're trying to understand."
