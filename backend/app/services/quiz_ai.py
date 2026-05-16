"""
AI Quiz Generator — auto-generates quizzes from course content using LLM.
Supports multiple choice, true/false, short answer questions with distractors.
"""
import json
import uuid
import random
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    LessonRepository, QuizRepository, QuestionRepository,
)
from app.models.train import Quiz, Question, QuestionType, DifficultyLevel


# In production, replace with actual LLM call
# For now, generates structured questions from lesson content


async def generate_quiz_from_lesson(
    db: AsyncSession,
    lesson_id: uuid.UUID,
    num_questions: int = 5,
    difficulty: str = "medium",
    question_types: Optional[list[str]] = None,
) -> dict:
    """Generate quiz questions from lesson content using AI."""
    lesson_repo = LessonRepository(db)
    lesson = await lesson_repo.get_by_id(lesson_id)
    if not lesson:
        raise ValueError(f"Lesson {lesson_id} not found")

    # Extract content for question generation
    content = lesson.content or ""
    transcript = lesson.video_transcript or ""
    source_text = f"{lesson.title}\n\n{content}\n\n{transcript}"

    if len(source_text.strip()) < 50:
        raise ValueError("Lesson content too short to generate quiz questions")

    # Create quiz
    quiz_repo = QuizRepository(db)
    question_repo = QuestionRepository(db)

    quiz = Quiz(
        id=uuid.uuid4(),
        lesson_id=lesson_id,
        title=f"Quiz: {lesson.title}",
        description=f"Auto-generated quiz for {lesson.title}",
        passing_score=70.0,
        is_published=False,
    )
    quiz = await quiz_repo.create(quiz)

    # Generate questions
    if question_types is None:
        question_types = ["multiple_choice", "true_false"]

    questions = []
    for i in range(min(num_questions, 10)):
        q_type = random.choice(question_types) if question_types else "multiple_choice"
        question_data = _generate_question(
            source_text, q_type, difficulty, i
        )
        q = Question(
            id=uuid.uuid4(),
            quiz_id=quiz.id,
            question_type=question_data["type"],
            difficulty=difficulty,
            text=question_data["text"],
            options=json.dumps(question_data.get("options")),
            correct_answer=question_data["correct_answer"],
            explanation=question_data.get("explanation"),
            points=1.0,
            order=i,
        )
        questions.append(q)

    questions = await question_repo.bulk_create(questions)

    # Build response
    from app.schemas.train import QuestionResponse
    question_responses = []
    for q in questions:
        question_responses.append(QuestionResponse(
            id=q.id,
            quiz_id=q.quiz_id,
            question_type=q.question_type.value if hasattr(q.question_type, 'value') else q.question_type,
            difficulty=q.difficulty.value if hasattr(q.difficulty, 'value') else q.difficulty,
            text=q.text,
            options=q.options,
            correct_answer=q.correct_answer,
            explanation=q.explanation,
            points=q.points,
            order=q.order,
            created_at=q.created_at,
        ))

    return {
        "quiz_id": quiz.id,
        "questions": question_responses,
    }


def _generate_question(
    source_text: str, q_type: str, difficulty: str, index: int
) -> dict:
    """Generate a single question from source text. Replace with LLM call in production."""
    # Extract key sentences for question generation
    sentences = [s.strip() for s in source_text.replace("\n", ". ").split(".") if len(s.strip()) > 20]
    if not sentences:
        sentences = [source_text]

    topic = sentences[index % len(sentences)]

    if q_type == "true_false":
        is_true = random.choice([True, False])
        return {
            "type": "true_false",
            "text": f'Based on the lesson content: "{topic[:100]}..." — is the following statement true or false?',
            "options": None,
            "correct_answer": "true" if is_true else "false",
            "explanation": "Review the lesson content for the correct answer.",
        }

    elif q_type == "multiple_choice":
        # Generate plausible distractors
        words = topic.split()
        correct = topic[:80] if len(topic) > 80 else topic
        distractors = [
            f"Option A: Different interpretation of the concept",
            f"Option B: Common misconception about this topic",
            f"Option C: Related but incorrect concept",
            f"Option D: {correct} (Correct)",
        ]
        random.shuffle(distractors)
        return {
            "type": "multiple_choice",
            "text": f'Based on the lesson, which of the following is correct regarding: "{topic[:100]}"?',
            "options": distractors,
            "correct_answer": distractors[-1].split(":")[0].strip() if "Correct" in distractors[-1] else distractors[0].split(":")[0].strip(),
            "explanation": f"The correct answer is based on the lesson content about this topic.",
        }

    elif q_type == "short_answer":
        return {
            "type": "short_answer",
            "text": f'In your own words, explain the concept: "{topic[:100]}"',
            "options": None,
            "correct_answer": topic[:100],
            "explanation": f"A good answer should cover the key points from the lesson.",
        }

    # Default multiple choice
    return {
        "type": "multiple_choice",
        "text": f'What is the key concept discussed in: "{topic[:100]}"?',
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option D",
        "explanation": "Refer to the lesson content.",
    }
