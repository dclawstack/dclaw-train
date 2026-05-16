"""
SCORM/xAPI Compliance — import/export SCORM packages, track xAPI statements.
"""
import uuid
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.train import (
    ScormPackageRepository, XApiStatementRepository, CourseRepository,
    LessonRepository,
)
from app.models.train import ScormPackage, XApiStatement


async def import_scorm_package(
    db: AsyncSession,
    title: str,
    version: str = "1.2",
    manifest_xml: Optional[str] = None,
    course_id: Optional[UUID] = None,
) -> dict:
    """Import a SCORM package."""
    scorm_repo = ScormPackageRepository(db)

    # In production: parse manifest XML, extract structure,
    # create corresponding lessons and quizzes

    scorm = ScormPackage(
        id=uuid.uuid4(),
        title=title,
        version=version,
        manifest_xml=manifest_xml,
        course_id=course_id,
        file_path=f"/scorm/{uuid.uuid4().hex}.zip",
    )
    scorm = await scorm_repo.create(scorm)

    return {
        "id": str(scorm.id),
        "title": scorm.title,
        "version": scorm.version,
        "course_id": str(scorm.course_id) if scorm.course_id else None,
        "imported_at": str(scorm.imported_at),
    }


async def export_scorm_package(
    db: AsyncSession,
    course_id: UUID,
) -> dict:
    """Export a course as a SCORM package."""
    course_repo = CourseRepository(db)
    lesson_repo = LessonRepository(db)

    course = await course_repo.get_by_id(course_id)
    if not course:
        raise ValueError(f"Course {course_id} not found")

    lessons = await lesson_repo.list_by_course(course_id)

    # In production: generate SCORM manifest XML and zip contents
    manifest = _generate_scorm_manifest(course.title, lessons)

    scorm_repo = ScormPackageRepository(db)
    scorm = ScormPackage(
        id=uuid.uuid4(),
        title=f"{course.title} - SCORM Export",
        version="1.2",
        manifest_xml=manifest,
        course_id=course_id,
        file_path=f"/scorm/exports/{course_id}.zip",
    )
    scorm = await scorm_repo.create(scorm)

    return {
        "id": str(scorm.id),
        "title": scorm.title,
        "version": scorm.version,
        "course_id": str(course_id),
        "exported_at": str(scorm.imported_at),
    }


async def store_xapi_statement(
    db: AsyncSession,
    learner_id: str,
    verb: str,
    object_id: str,
    result: Optional[dict] = None,
    context: Optional[dict] = None,
) -> dict:
    """Store an xAPI learning statement."""
    import json
    xapi_repo = XApiStatementRepository(db)

    statement = XApiStatement(
        id=uuid.uuid4(),
        learner_id=learner_id,
        verb=verb,
        object_id=object_id,
        result=json.dumps(result) if result else None,
        context=json.dumps(context) if context else None,
    )
    statement = await xapi_repo.create(statement)

    return {
        "id": str(statement.id),
        "learner_id": statement.learner_id,
        "verb": statement.verb,
        "object_id": statement.object_id,
        "stored_at": str(statement.stored_at),
    }


async def get_xapi_statements(
    db: AsyncSession,
    learner_id: str,
    limit: int = 50,
    offset: int = 0,
) -> dict:
    """Retrieve xAPI statements for a learner."""
    import json
    xapi_repo = XApiStatementRepository(db)

    statements, total = await xapi_repo.list_by_learner(learner_id, limit, offset)

    items = []
    for s in statements:
        items.append({
            "id": str(s.id),
            "learner_id": s.learner_id,
            "verb": s.verb,
            "object_id": s.object_id,
            "result": json.loads(s.result) if s.result else None,
            "context": json.loads(s.context) if s.context else None,
            "stored_at": str(s.stored_at),
        })

    return {
        "items": items,
        "total": total,
        "page": offset // limit + 1 if limit else 1,
        "page_size": limit,
        "pages": (total + limit - 1) // limit if limit else 1,
    }


def _generate_scorm_manifest(course_title: str, lessons: list) -> str:
    """Generate a basic SCORM 1.2 manifest XML."""
    items_xml = ""
    for i, lesson in enumerate(lessons):
        items_xml += f"""
    <item identifier="item_{i}" identifierref="resource_{i}">
      <title>{lesson.title}</title>
    </item>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="MANIFEST-{uuid.uuid4().hex[:8]}"
          version="1.0"
          xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2">
  <organizations default="org_1">
    <organization identifier="org_1">
      <title>{course_title}</title>{items_xml}
    </organization>
  </organizations>
  <resources>
    <resource identifier="resource_0" type="webcontent" href="index.html"/>
  </resources>
</manifest>"""
