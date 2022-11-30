import json

import redis
from fastapi import APIRouter
from pydantic.main import BaseModel

from domain.services.create_answer import ServiceCreateAnswer
from storage.answers_repository import AnswersRepository
from storage.participants_repository import ParticipantsRepository
from storage.questions_repository import QuestionsRepository

router = APIRouter()


class CreateAnswerItem(BaseModel):
    participant_id: int
    questionnaire_id: int
    question_id: int
    value: str


@router.get('/api/answers', status_code=200)
async def get_answers(participant_id):
    r = redis.Redis(host='localhost', port=6379, db=0)
    participants = json.loads(r.get("participants").decode())
    participant = participants[str(participant_id)]
    answers = participant["answers"]

    return answers


@router.post('/api/answers', status_code=201)
async def create_answer(item: CreateAnswerItem):
    service = ServiceCreateAnswer()
    service.answers = AnswersRepository()
    service.questions = QuestionsRepository()
    service.participants = ParticipantsRepository()
    answer_entity = service.execute(item.participant_id, item.questionnaire_id, item.question_id, item.value)

    return {
        "id": answer_entity.id,
        "question_id": answer_entity.question.id,
        "value": answer_entity.value
    }
