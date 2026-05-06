import uuid
import random
from datetime import datetime, timedelta

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TrainingCreate(BaseModel):
    name: str
    format: str


class Training(BaseModel):
    id: str
    name: str
    format: str
    enrollment_link: str
    completion_rate: int
    average_score: int
    certification_expiry: str
    created_at: str


class LearnerProgress(BaseModel):
    learner_name: str
    status: str
    score: int


@router.post("/trainings", response_model=Training)
async def create_training(payload: TrainingCreate):
    training_id = str(uuid.uuid4())
    enrollment_link = f"https://train.dclawstack.io/t/{training_id}"
    completion_rate = random.randint(40, 95)
    average_score = random.randint(70, 100)
    certification_expiry = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    created_at = datetime.now().isoformat()

    return Training(
        id=training_id,
        name=payload.name,
        format=payload.format,
        enrollment_link=enrollment_link,
        completion_rate=completion_rate,
        average_score=average_score,
        certification_expiry=certification_expiry,
        created_at=created_at,
    )


@router.get("/trainings/{id}/progress", response_model=list[LearnerProgress])
async def get_training_progress(id: str):
    return [
        LearnerProgress(learner_name="Alice", status="Completed", score=92),
        LearnerProgress(learner_name="Bob", status="In Progress", score=45),
        LearnerProgress(learner_name="Charlie", status="Completed", score=88),
    ]
