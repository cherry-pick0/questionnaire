from fastapi import APIRouter

from domain.services.create_questionnaire import ServiceCreateQuestionnaire
from storage.questionnaires_repository import QuestionnaireRepository, QuestionsRepository

router = APIRouter()


@router.get('/api/questionnaires', status_code=200)
async def get_questionnaires():
    # Create mock questionnaire
    service = ServiceCreateQuestionnaire()
    service.questionnaires = QuestionnaireRepository()
    service.questions = QuestionsRepository()
    questionnaire = service.execute()
    list_questionnaires = [{"id": questionnaire.id}]

    return list_questionnaires


@router.get('/api/questionnaire-flow', status_code=200)
async def get_questionnaire_flow():
    return []
