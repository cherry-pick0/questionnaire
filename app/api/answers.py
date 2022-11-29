from fastapi import APIRouter

router = APIRouter()


@router.get('/api/answers', status_code=200)
async def get_answers():
    return []


@router.post('/api/answers', status_code=201)
async def create_answer():
    return {}
