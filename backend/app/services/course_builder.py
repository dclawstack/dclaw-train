"""
Course Builder service — handles content hierarchy, file storage, and video processing.
"""
import json
import uuid
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    CourseRepository, LessonRepository, ResourceRepository,
)
from app.models.train import Course, Lesson, LessonResource, TrainingFormat


async def create_course_with_lessons(
    db: AsyncSession,
    title: str,
    description: Optional[str],
    format: str,
    lessons_data: list[dict],
    category: Optional[str] = None,
    tags: Optional[str] = None,
) -> dict:
    """Create a course with its lesson hierarchy in one transaction."""
    course_repo = CourseRepository(db)
    lesson_repo = LessonRepository(db)

    course = Course(
        id=uuid.uuid4(),
        title=title,
        description=description,
        format=format,
        category=category,
        tags=tags,
        is_published=False,
    )
    course = await course_repo.create(course)

    created_lessons = []
    for i, lesson_data in enumerate(lessons_data):
        lesson = Lesson(
            id=uuid.uuid4(),
            course_id=course.id,
            title=lesson_data.get("title", f"Lesson {i+1}"),
            description=lesson_data.get("description"),
            content=lesson_data.get("content"),
            video_url=lesson_data.get("video_url"),
            duration_minutes=lesson_data.get("duration_minutes"),
            order=i,
            is_published=False,
        )
        lesson = await lesson_repo.create(lesson)
        created_lessons.append(lesson)

    return {
        "course_id": str(course.id),
        "title": course.title,
        "lesson_count": len(created_lessons),
    }


async def add_lesson_to_course(
    db: AsyncSession,
    course_id: UUID,
    title: str,
    description: Optional[str] = None,
    content: Optional[str] = None,
    video_url: Optional[str] = None,
    duration_minutes: Optional[int] = None,
) -> dict:
    """Add a lesson to an existing course."""
    lesson_repo = LessonRepository(db)
    course_repo = CourseRepository(db)

    course = await course_repo.get_by_id(course_id)
    if not course:
        raise ValueError(f"Course {course_id} not found")

    existing = await lesson_repo.list_by_course(course_id)
    next_order = len(existing)

    lesson = Lesson(
        id=uuid.uuid4(),
        course_id=course_id,
        title=title,
        description=description,
        content=content,
        video_url=video_url,
        duration_minutes=duration_minutes,
        order=next_order,
        is_published=False,
    )
    lesson = await lesson_repo.create(lesson)

    return {
        "lesson_id": str(lesson.id),
        "title": lesson.title,
        "order": lesson.order,
    }


async def add_resource_to_lesson(
    db: AsyncSession,
    lesson_id: UUID,
    title: str,
    resource_type: str,
    url: str,
) -> dict:
    """Add a resource attachment to a lesson."""
    resource_repo = ResourceRepository(db)
    lesson_repo = LessonRepository(db)

    lesson = await lesson_repo.get_by_id(lesson_id)
    if not lesson:
        raise ValueError(f"Lesson {lesson_id} not found")

    resource = LessonResource(
        id=uuid.uuid4(),
        lesson_id=lesson_id,
        title=title,
        resource_type=resource_type,
        url=url,
    )
    resource = await resource_repo.create(resource)

    return {
        "resource_id": str(resource.id),
        "title": resource.title,
        "type": resource.resource_type,
    }


async def get_course_structure(db: AsyncSession, course_id: UUID) -> Optional[dict]:
    """Get the full course structure with lessons, resources, and quizzes."""
    course_repo = CourseRepository(db)
    lesson_repo = LessonRepository(db)
    resource_repo = ResourceRepository(db)
    from app.repositories.train import QuizRepository
    quiz_repo = QuizRepository(db)

    course = await course_repo.get_by_id(course_id)
    if not course:
        return None

    lessons = await lesson_repo.list_by_course(course_id)
    lessons_data = []
    for lesson in lessons:
        resources = await resource_repo.list_by_lesson(lesson.id)
        quizzes = await quiz_repo.list_by_lesson(lesson.id)

        lessons_data.append({
            "id": str(lesson.id),
            "title": lesson.title,
            "description": lesson.description,
            "content": lesson.content[:500] if lesson.content else None,
            "video_url": lesson.video_url,
            "duration_minutes": lesson.duration_minutes,
            "order": lesson.order,
            "is_published": lesson.is_published,
            "resources": [
                {"id": str(r.id), "title": r.title, "type": r.resource_type, "url": r.url}
                for r in resources
            ],
            "quizzes": [
                {"id": str(q.id), "title": q.title, "is_published": q.is_published}
                for q in quizzes
            ],
        })

    return {
        "id": str(course.id),
        "title": course.title,
        "description": course.description,
        "format": course.format.value if hasattr(course.format, 'value') else course.format,
        "category": course.category,
        "tags": course.tags,
        "is_published": course.is_published,
        "created_at": str(course.created_at),
        "lessons": lessons_data,
    }
