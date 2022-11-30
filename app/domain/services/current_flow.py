import abc
from typing import List

from domain.entities.questionnaire import Question


class CurrentFlowQuestionsIRepository(abc.ABC):
    @abc.abstractmethod
    def get_current_question(self, participant: int, questionnaire: int) -> List[Question]:
        pass

    @abc.abstractmethod
    def questions_completed(self, participant: int, questionnaire: int) -> bool:
        pass


class ServiceCurrentFlow:
    questions: CurrentFlowQuestionsIRepository = None

    def execute(self, participant: int, questionnaire: int):
        current_question = self.questions.get_current_question(participant, questionnaire)
        status = "completed" if self.questions.questions_completed(participant, questionnaire) else "pending"

        return {
            "participant": participant,
            "questionnaire": questionnaire,
            "status": status,
            "current_question": current_question,
        }
