from fastapi import APIRouter

from domain.services.create_participant import ServiceCreateParticipant
from storage.participants_repository import ParticipantsRepository

router = APIRouter()


@router.post('/api/participants', status_code=201)
async def create_participant():
    service = ServiceCreateParticipant()
    service.participants = ParticipantsRepository()
    participant = service.execute()
    return participant
