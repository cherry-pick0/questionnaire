import abc
import uuid

from domain.entities.participant import Participant


class CreateParticipantParticipantsIRepository(abc.ABC):
    @abc.abstractmethod
    def add_participant(self, participant: Participant):
        pass


class ServiceCreateParticipant:
    participants: CreateParticipantParticipantsIRepository = None

    def execute(self):
        identifier = str(uuid.uuid4())
        participant = Participant(identifier)
        participant = self.participants.add_participant(participant)
        return participant
