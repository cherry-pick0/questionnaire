from fastapi import APIRouter

router = APIRouter()


@router.post('/api/participants', status_code=201)
async def create_participant():
    return {}
