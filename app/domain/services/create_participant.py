import abc
import uuid


class CreateParticipantParticipantsIRepository(abc.ABC):
    @abc.abstractmethod
    def add_participant(self, identifier: str):
        pass


class ServiceCreateParticipant:
    participants: CreateParticipantParticipantsIRepository = None

    def execute(self):
        identifier = str(uuid.uuid4())
        participant = self.participants.add_participant(identifier)
        return participant
