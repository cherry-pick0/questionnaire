import json

import redis

from domain.entities.participant import Participant
from domain.services.create_participant import CreateParticipantParticipantsIRepository


class ParticipantsRepository (CreateParticipantParticipantsIRepository):
    def add_participant(self, participant_entity: Participant):
        r = redis.Redis(host='localhost', port=6379, db=0)

        participants = r.get("participants")

        if not participants:
            r.set("participants", "{}")
            participants = r.get('participants')

        participants = json.loads(participants.decode())

        participant_id = len(list(participants.keys())) + 1
        participant = {"id": participant_id, "identifier": participant_entity.identifier, "answers": {}}
        participants[participant_id] = participant

        r.set("participants", json.dumps(participants))
        participant_entity.id = participant_id

        return participant_entity
