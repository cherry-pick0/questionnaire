import json

import redis
from domain.services.create_participant import CreateParticipantParticipantsIRepository


class ParticipantsRepository (CreateParticipantParticipantsIRepository):
    def add_participant(self, identifier: str):
        r = redis.Redis(host='localhost', port=6379, db=0)

        participants = r.get("participants").decode()
        r.set("participants", "{}")
        if not participants:
            r.set("participants", "{}")
            participants = r.get('participants').decode()

        participants = json.loads(participants)

        participant_id = len(list(participants.keys())) + 1
        participant = {"id": participant_id}
        participants[identifier] = participant

        r.set("participants", json.dumps(participants))
        return participant
