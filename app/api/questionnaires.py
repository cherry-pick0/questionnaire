from fastapi import APIRouter

router = APIRouter()


@router.get('/api/questionnaires', status_code=200)
async def get_questionnaires():
    return []


@router.get('/api/questionnaire-flow', status_code=200)
async def get_questionnaire_flow():
    return []
