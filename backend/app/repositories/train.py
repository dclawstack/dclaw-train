from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, delete

from app.repositories.base_repo import BaseRepository
from app.models.train import (
    Course, Lesson, LessonResource, Quiz, Question, QuizAttempt,
    Enrollment, LearnerProgress, LiveSession, Certificate, Badge,
    SkillAssessment, ForumTopic, ForumReply, TutorConversation,
    LearningPath, ScormPackage, XApiStatement,
)


# ────────────────────────────── Course ──────────────────────────────

class CourseRepository(BaseRepository[Course]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Course)

    async def list_all(self, limit: int = 20, offset: int = 0) -> tuple[list[Course], int]:
        result = await self.db.execute(
            select(Course).order_by(Course.created_at.desc()).limit(limit).offset(offset)
        )
        items = list(result.scalars().all())
        count_result = await self.db.execute(select(func.count()).select_from(Course))
        total = count_result.scalar() or 0
        return items, total

    async def list_published(self, limit: int = 20, offset: int = 0) -> tuple[list[Course], int]:
        query = select(Course).where(Course.is_published == True).order_by(Course.created_at.desc())
        result = await self.db.execute(query.limit(limit).offset(offset))
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(Course).where(Course.is_published == True)
        )
        total = count_result.scalar() or 0
        return items, total

    async def search(self, q: str, limit: int = 20, offset: int = 0) -> tuple[list[Course], int]:
        query = select(Course).where(
            Course.title.ilike(f"%{q}%") | Course.description.ilike(f"%{q}%")
        ).order_by(Course.created_at.desc())
        result = await self.db.execute(query.limit(limit).offset(offset))
        items = list(result.scalars().all())
        return items, len(items)

    async def update(self, course_id: UUID, **kwargs) -> Optional[Course]:
        await self.db.execute(
            update(Course).where(Course.id == course_id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(course_id)


# ────────────────────────────── Lesson ──────────────────────────────

class LessonRepository(BaseRepository[Lesson]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Lesson)

    async def list_by_course(self, course_id: UUID) -> list[Lesson]:
        result = await self.db.execute(
            select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)
        )
        return list(result.scalars().all())

    async def update(self, lesson_id: UUID, **kwargs) -> Optional[Lesson]:
        await self.db.execute(
            update(Lesson).where(Lesson.id == lesson_id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(lesson_id)

    async def reorder(self, course_id: UUID, lesson_ids: list[UUID]) -> None:
        for idx, lid in enumerate(lesson_ids):
            await self.db.execute(
                update(Lesson).where(Lesson.id == lid, Lesson.course_id == course_id).values(order=idx)
            )
        await self.db.commit()

    async def count_by_course(self, course_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Lesson).where(Lesson.course_id == course_id)
        )
        return result.scalar() or 0


# ────────────────────────────── LessonResource ──────────────────────────────

class ResourceRepository(BaseRepository[LessonResource]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, LessonResource)

    async def list_by_lesson(self, lesson_id: UUID) -> list[LessonResource]:
        result = await self.db.execute(
            select(LessonResource).where(LessonResource.lesson_id == lesson_id)
        )
        return list(result.scalars().all())


# ────────────────────────────── Quiz ──────────────────────────────

class QuizRepository(BaseRepository[Quiz]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Quiz)

    async def list_by_lesson(self, lesson_id: UUID) -> list[Quiz]:
        result = await self.db.execute(
            select(Quiz).where(Quiz.lesson_id == lesson_id)
        )
        return list(result.scalars().all())

    async def update(self, quiz_id: UUID, **kwargs) -> Optional[Quiz]:
        await self.db.execute(
            update(Quiz).where(Quiz.id == quiz_id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(quiz_id)


# ────────────────────────────── Question ──────────────────────────────

class QuestionRepository(BaseRepository[Question]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Question)

    async def list_by_quiz(self, quiz_id: UUID) -> list[Question]:
        result = await self.db.execute(
            select(Question).where(Question.quiz_id == quiz_id).order_by(Question.order)
        )
        return list(result.scalars().all())

    async def count_by_quiz(self, quiz_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Question).where(Question.quiz_id == quiz_id)
        )
        return result.scalar() or 0

    async def bulk_create(self, questions: list[Question]) -> list[Question]:
        self.db.add_all(questions)
        await self.db.commit()
        for q in questions:
            await self.db.refresh(q)
        return questions


# ────────────────────────────── QuizAttempt ──────────────────────────────

class QuizAttemptRepository(BaseRepository[QuizAttempt]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, QuizAttempt)

    async def list_by_learner(self, learner_id: str, limit: int = 20, offset: int = 0) -> tuple[list[QuizAttempt], int]:
        query = select(QuizAttempt).where(QuizAttempt.learner_id == learner_id).order_by(
            QuizAttempt.completed_at.desc().nullslast()
        )
        result = await self.db.execute(query.limit(limit).offset(offset))
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(QuizAttempt).where(QuizAttempt.learner_id == learner_id)
        )
        total = count_result.scalar() or 0
        return items, total

    async def best_for_quiz(self, quiz_id: UUID, learner_id: str) -> Optional[QuizAttempt]:
        result = await self.db.execute(
            select(QuizAttempt).where(
                QuizAttempt.quiz_id == quiz_id,
                QuizAttempt.learner_id == learner_id
            ).order_by(QuizAttempt.score.desc()).limit(1)
        )
        return result.scalar_one_or_none()


# ────────────────────────────── Enrollment ──────────────────────────────

class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Enrollment)

    async def list_by_course(self, course_id: UUID) -> list[Enrollment]:
        result = await self.db.execute(
            select(Enrollment).where(Enrollment.course_id == course_id)
        )
        return list(result.scalars().all())

    async def list_by_learner(self, learner_id: str) -> list[Enrollment]:
        result = await self.db.execute(
            select(Enrollment).where(Enrollment.learner_id == learner_id)
        )
        return list(result.scalars().all())

    async def get_by_course_and_learner(self, course_id: UUID, learner_id: str) -> Optional[Enrollment]:
        result = await self.db.execute(
            select(Enrollment).where(
                Enrollment.course_id == course_id,
                Enrollment.learner_id == learner_id
            )
        )
        return result.scalar_one_or_none()

    async def update(self, enrollment_id: UUID, **kwargs) -> Optional[Enrollment]:
        await self.db.execute(
            update(Enrollment).where(Enrollment.id == enrollment_id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(enrollment_id)

    async def count_by_course(self, course_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Enrollment).where(Enrollment.course_id == course_id)
        )
        return result.scalar() or 0

    async def count_completed_by_course(self, course_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Enrollment).where(
                Enrollment.course_id == course_id,
                Enrollment.status == "Completed"
            )
        )
        return result.scalar() or 0

    async def count_all(self) -> int:
        result = await self.db.execute(select(func.count()).select_from(Enrollment))
        return result.scalar() or 0

    async def count_completed_all(self) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(Enrollment).where(Enrollment.status == "Completed")
        )
        return result.scalar() or 0

    async def get_average_score(self, course_id: Optional[UUID] = None) -> float:
        query = select(func.avg(LearnerProgress.score)).join(
            Enrollment, LearnerProgress.enrollment_id == Enrollment.id
        ).where(LearnerProgress.score != None)
        if course_id:
            query = query.where(Enrollment.course_id == course_id)
        result = await self.db.execute(query)
        avg = result.scalar()
        return float(avg) if avg else 0.0


# ────────────────────────────── LearnerProgress ──────────────────────────────

class LearnerProgressRepository(BaseRepository[LearnerProgress]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, LearnerProgress)

    async def list_by_enrollment(self, enrollment_id: UUID) -> list[LearnerProgress]:
        result = await self.db.execute(
            select(LearnerProgress).where(LearnerProgress.enrollment_id == enrollment_id)
        )
        return list(result.scalars().all())

    async def get_by_enrollment_and_lesson(
        self, enrollment_id: UUID, lesson_id: UUID
    ) -> Optional[LearnerProgress]:
        result = await self.db.execute(
            select(LearnerProgress).where(
                LearnerProgress.enrollment_id == enrollment_id,
                LearnerProgress.lesson_id == lesson_id
            )
        )
        return result.scalar_one_or_none()

    async def update(self, progress_id: UUID, **kwargs) -> Optional[LearnerProgress]:
        await self.db.execute(
            update(LearnerProgress).where(LearnerProgress.id == progress_id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(progress_id)

    async def get_total_time_by_learner(self, learner_id: str) -> int:
        result = await self.db.execute(
            select(func.sum(LearnerProgress.time_spent_seconds)).join(
                Enrollment, LearnerProgress.enrollment_id == Enrollment.id
            ).where(Enrollment.learner_id == learner_id)
        )
        return result.scalar() or 0

    async def get_average_score_by_learner(self, learner_id: str) -> float:
        result = await self.db.execute(
            select(func.avg(LearnerProgress.score)).join(
                Enrollment, LearnerProgress.enrollment_id == Enrollment.id
            ).where(
                Enrollment.learner_id == learner_id,
                LearnerProgress.score != None
            )
        )
        avg = result.scalar()
        return float(avg) if avg else 0.0

    async def get_at_risk_learners(self, threshold: float = 0.3) -> list[str]:
        """Learners with progress < threshold across their enrollments."""
        result = await self.db.execute(
            select(Enrollment.learner_id).where(
                Enrollment.progress_percentage < threshold * 100,
                Enrollment.status != "Completed"
            ).distinct()
        )
        return [r for r in result.scalars().all()]

    async def get_completion_count_by_course(self, course_id: UUID) -> int:
        result = await self.db.execute(
            select(func.count()).select_from(LearnerProgress).join(
                Enrollment, LearnerProgress.enrollment_id == Enrollment.id
            ).where(
                Enrollment.course_id == course_id,
                LearnerProgress.status == "Completed"
            )
        )
        return result.scalar() or 0


# ────────────────────────────── LiveSession ──────────────────────────────

class LiveSessionRepository(BaseRepository[LiveSession]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, LiveSession)

    async def list_by_course(self, course_id: UUID) -> list[LiveSession]:
        result = await self.db.execute(
            select(LiveSession).where(LiveSession.course_id == course_id).order_by(LiveSession.scheduled_at)
        )
        return list(result.scalars().all())

    async def list_upcoming(self, limit: int = 10) -> list[LiveSession]:
        from datetime import datetime
        result = await self.db.execute(
            select(LiveSession).where(
                LiveSession.scheduled_at > datetime.utcnow(),
                LiveSession.status == "Scheduled"
            ).order_by(LiveSession.scheduled_at).limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, session_id: UUID, **kwargs) -> Optional[LiveSession]:
        await self.db.execute(
            update(LiveSession).where(LiveSession.id == session_id).values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(session_id)


# ────────────────────────────── Certificate ──────────────────────────────

class CertificateRepository(BaseRepository[Certificate]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Certificate)

    async def list_by_learner(self, learner_id: str) -> list[Certificate]:
        result = await self.db.execute(
            select(Certificate).where(Certificate.learner_id == learner_id).order_by(Certificate.issued_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_course_and_learner(self, course_id: UUID, learner_id: str) -> Optional[Certificate]:
        result = await self.db.execute(
            select(Certificate).where(
                Certificate.course_id == course_id,
                Certificate.learner_id == learner_id
            )
        )
        return result.scalar_one_or_none()


# ────────────────────────────── Badge ──────────────────────────────

class BadgeRepository(BaseRepository[Badge]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Badge)

    async def list_by_learner(self, learner_id: str) -> list[Badge]:
        result = await self.db.execute(
            select(Badge).where(Badge.learner_id == learner_id).order_by(Badge.earned_at.desc())
        )
        return list(result.scalars().all())


# ────────────────────────────── SkillAssessment ──────────────────────────────

class SkillAssessmentRepository(BaseRepository[SkillAssessment]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, SkillAssessment)

    async def list_by_learner(self, learner_id: str) -> list[SkillAssessment]:
        result = await self.db.execute(
            select(SkillAssessment).where(SkillAssessment.learner_id == learner_id).order_by(
                SkillAssessment.completed_at.desc()
            )
        )
        return list(result.scalars().all())

    async def get_by_learner_and_type(
        self, learner_id: str, assessment_type: str, course_id: Optional[UUID] = None
    ) -> list[SkillAssessment]:
        query = select(SkillAssessment).where(
            SkillAssessment.learner_id == learner_id,
            SkillAssessment.assessment_type == assessment_type
        )
        if course_id:
            query = query.where(SkillAssessment.course_id == course_id)
        result = await self.db.execute(query.order_by(SkillAssessment.completed_at.desc()))
        return list(result.scalars().all())


# ────────────────────────────── ForumTopic ──────────────────────────────

class ForumTopicRepository(BaseRepository[ForumTopic]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ForumTopic)

    async def list_by_course(self, course_id: UUID) -> list[ForumTopic]:
        result = await self.db.execute(
            select(ForumTopic).where(ForumTopic.course_id == course_id).order_by(
                ForumTopic.is_pinned.desc(), ForumTopic.created_at.desc()
            )
        )
        return list(result.scalars().all())


# ────────────────────────────── ForumReply ──────────────────────────────

class ForumReplyRepository(BaseRepository[ForumReply]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ForumReply)

    async def list_by_topic(self, topic_id: UUID) -> list[ForumReply]:
        result = await self.db.execute(
            select(ForumReply).where(ForumReply.topic_id == topic_id).order_by(ForumReply.created_at)
        )
        return list(result.scalars().all())


# ────────────────────────────── TutorConversation ──────────────────────────────

class TutorConversationRepository(BaseRepository[TutorConversation]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, TutorConversation)

    async def get_active_conversation(
        self, learner_id: str, lesson_id: Optional[UUID] = None, course_id: Optional[UUID] = None
    ) -> Optional[TutorConversation]:
        result = await self.db.execute(
            select(TutorConversation).where(
                TutorConversation.learner_id == learner_id,
                TutorConversation.lesson_id == lesson_id if lesson_id else True,
                TutorConversation.course_id == course_id if course_id else True,
            ).order_by(TutorConversation.updated_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()

    async def update_messages(self, conv_id: UUID, messages: str) -> None:
        from datetime import datetime
        await self.db.execute(
            update(TutorConversation).where(TutorConversation.id == conv_id).values(
                messages=messages,
                updated_at=datetime.utcnow()
            )
        )
        await self.db.commit()


# ────────────────────────────── LearningPath ──────────────────────────────

class LearningPathRepository(BaseRepository[LearningPath]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, LearningPath)

    async def get_latest_for_learner(self, learner_id: str) -> Optional[LearningPath]:
        result = await self.db.execute(
            select(LearningPath).where(LearningPath.learner_id == learner_id).order_by(
                LearningPath.generated_at.desc()
            ).limit(1)
        )
        return result.scalar_one_or_none()


# ────────────────────────────── SCORM ──────────────────────────────

class ScormPackageRepository(BaseRepository[ScormPackage]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ScormPackage)


class XApiStatementRepository(BaseRepository[XApiStatement]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, XApiStatement)

    async def list_by_learner(self, learner_id: str, limit: int = 50, offset: int = 0) -> tuple[list[XApiStatement], int]:
        query = select(XApiStatement).where(XApiStatement.learner_id == learner_id).order_by(
            XApiStatement.stored_at.desc()
        )
        result = await self.db.execute(query.limit(limit).offset(offset))
        items = list(result.scalars().all())
        count_result = await self.db.execute(
            select(func.count()).select_from(XApiStatement).where(XApiStatement.learner_id == learner_id)
        )
        total = count_result.scalar() or 0
        return items, total
