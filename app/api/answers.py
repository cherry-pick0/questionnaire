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
async def get_answers(participant_id, questionnaire_id):
    answers_repo = AnswersRepository()
    answers = answers_repo.get_answers(participant_id, questionnaire_id)
    answers_list = []

    for answer in answers:
        answer_data = {
            "participant": int(answer.participant.id),
            "value": answer.value,
            "question_id": answer.question.id,
            "question_text": answer.question.text,
            "question_type": answer.question.question_type,
            "question_order": answer.question.order,
        }
        answers_list.append(answer_data)

    return answers_list


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
