from domain.entities.participant import Participant
from domain.entities.questionnaire import Question


class Answer:
    id: int
    participant: Participant
    question: Question
    value: str

    def __init__(self, participant, question, value, answer_id=None):
        self.id = answer_id
        self.participant = participant
        self.question = question
        self.value = value
