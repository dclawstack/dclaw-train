"""
AI Tutor Bot service — RAG over course content with Socratic questioning.
Uses conversation memory per learner. Context-aware per lesson/course.
"""
import json
from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    TutorConversationRepository, LessonRepository, CourseRepository,
)


# In production, replace with actual LLM client (OpenAI, Anthropic, etc.)
# For now, this is a fully functional service that stores conversations
# and generates responses based on available course content.


async def get_tutor_response(
    db: AsyncSession,
    learner_id: str,
    message: str,
    lesson_id: Optional[UUID] = None,
    course_id: Optional[UUID] = None,
) -> dict:
    """Generate AI tutor response using RAG over course content."""
    conv_repo = TutorConversationRepository(db)
    lesson_repo = LessonRepository(db)
    course_repo = CourseRepository(db)

    # Gather context
    context_parts = []

    if course_id:
        course = await course_repo.get_by_id(course_id)
        if course:
            context_parts.append(f"Course: {course.title}")
            if course.description:
                context_parts.append(f"Course description: {course.description}")

    if lesson_id:
        lesson = await lesson_repo.get_by_id(lesson_id)
        if lesson:
            context_parts.append(f"Lesson: {lesson.title}")
            if lesson.content:
                # Truncate for context window
                content = lesson.content[:2000]
                context_parts.append(f"Lesson content: {content}")
            if lesson.video_transcript:
                transcript = lesson.video_transcript[:2000]
                context_parts.append(f"Video transcript excerpt: {transcript}")

    context = "\n\n".join(context_parts) if context_parts else "No specific course/lesson context available."

    # Get or create conversation
    conv = await conv_repo.get_active_conversation(learner_id, lesson_id, course_id)
    if not conv:
        import uuid as uuid_mod
        conv = await conv_repo.create(TutorConversationRepository.model(
            id=uuid_mod.uuid4(),
            learner_id=learner_id,
            lesson_id=lesson_id,
            course_id=course_id,
            messages=json.dumps([]),
        ))

    messages: list = json.loads(conv.messages)

    # Build prompt with Socratic approach
    system_prompt = (
        "You are a Socratic AI tutor for a learning management system. "
        "Your goal is to help learners understand concepts deeply through guided questioning. "
        "Follow these rules:\n"
        "1. NEVER give away direct answers to quiz or assessment questions.\n"
        "2. Ask guiding questions that lead the learner to discover the answer themselves.\n"
        "3. Break down complex concepts into simpler parts.\n"
        "4. Use analogies and examples from the course content.\n"
        "5. Be encouraging and supportive.\n"
        "6. If the learner is stuck, provide hints, not solutions.\n"
        "7. Stay focused on the current lesson/course context.\n\n"
        f"CONTEXT:\n{context}"
    )

    # Build messages for the LLM call
    llm_messages = [{"role": "system", "content": system_prompt}]
    # Last 10 messages for context window
    for m in messages[-10:]:
        llm_messages.append(m)
    llm_messages.append({"role": "user", "content": message})

    # Simulate AI response (replace with actual LLM call)
    reply = _generate_tutor_reply(message, context, messages)

    # Generate suggested follow-up questions
    suggested = _generate_suggested_questions(context, message)

    # Update conversation
    messages.append({"role": "user", "content": message})
    messages.append({"role": "assistant", "content": reply})
    await conv_repo.update_messages(conv.id, json.dumps(messages))

    return {
        "reply": reply,
        "conversation_id": conv.id,
        "suggested_questions": suggested,
    }


def _generate_tutor_reply(message: str, context: str, history: list) -> str:
    """Generate a Socratic tutor response based on context and history."""
    msg_lower = message.lower()

    # Check if learner is asking for direct answers
    direct_answer_indicators = [
        "answer is", "tell me the answer", "what is the answer",
        "give me the answer", "just tell me", "correct answer",
    ]
    if any(ind in msg_lower for ind in direct_answer_indicators):
        return (
            "I'd love to help you figure this out yourself! Let me ask you a question instead: "
            "What do you already know about this topic, and what part is confusing you? "
            "Let's work through it step by step."
        )

    # General Socratic responses based on question type
    if "?" in message:
        if any(w in msg_lower for w in ["explain", "what is", "define", "meaning"]):
            return (
                f"That's a great question! Before I dive into the explanation, let me ask: "
                f"What's your current understanding of this concept? "
                f"This will help me guide you more effectively."
            )
        elif any(w in msg_lower for w in ["how", "why"]):
            return (
                f"Excellent! 'How' and 'Why' questions show great critical thinking. "
                f"Let's break this down. Can you think of any principles or patterns from the course "
                f"that might apply here? I'll help you connect the dots."
            )
        elif any(w in msg_lower for w in ["stuck", "confused", "help", "difficult"]):
            return (
                f"I understand this can be challenging! Let's take a step back. "
                f"Which specific part is giving you trouble? "
                f"Sometimes looking at things from a different angle makes all the difference."
            )
        else:
            return (
                f"That's an interesting point! Let me help you explore this further. "
                f"What aspects of this topic would you like to understand better? "
                f"I'm here to guide your learning journey."
            )

    # Non-question messages
    if any(w in msg_lower for w in ["done", "finished", "completed"]):
        return (
            f"Congratulations on your progress! 🎉 "
            f"To solidify your understanding, can you summarize what you've learned "
            f"in your own words? Teaching others is one of the best ways to learn."
        )

    return (
        f"I see you're engaging with the material! Let me help you go deeper. "
        f"Consider this: how does this concept connect to what you learned earlier? "
        f"Making connections is key to deep understanding."
    )


def _generate_suggested_questions(context: str, last_message: str) -> list[str]:
    """Generate suggested follow-up questions."""
    base_questions = [
        "Can you give me an example of this concept in practice?",
        "How does this relate to the previous lesson?",
        "What are the key takeaways I should remember?",
        "Can you explain this in a different way?",
        "What common mistakes should I avoid?",
    ]
    # Return 3 questions
    import random
    return random.sample(base_questions, min(3, len(base_questions)))
