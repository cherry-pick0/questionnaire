import abc
from typing import Optional

from domain.entities.questionnaire import Question


class CurrentFlowQuestionsIRepository(abc.ABC):
    @abc.abstractmethod
    def get_current_question(self, participant_id: int, questionnaire_id: int) -> Optional[Question]:
        pass


class ServiceCurrentFlow:
    questions: CurrentFlowQuestionsIRepository = None

    def execute(self, participant: int, questionnaire: int):
        current_question = self.questions.get_current_question(participant, questionnaire)
        status = "completed" if not current_question else "pending"

        return {
            "participant": participant,
            "questionnaire": questionnaire,
            "status": status,
            "current_question": current_question,
        }
