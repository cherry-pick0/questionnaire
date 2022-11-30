class Participant:
    id: int
    identifier: str

    def __init__(self, identifier, participant_id=None):
        self.id = participant_id
        self.identifier = identifier
