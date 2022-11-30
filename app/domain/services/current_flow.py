import abc
from typing import Optional

from domain.entities.questionnaire import Question


class CurrentFlowQuestionsIRepository(abc.ABC):
    @abc.abstractmethod
    def get_current_question(self, participant_id: int, questionnaire_id: int) -> Optional[Question]:
        pass


class ServiceCurrentFlow:
    questions: CurrentFlowQuestionsIRepository = None

    def execute(self, questionnaire: int, participant: int):
        current_question_data = None
        current_question = self.questions.get_current_question(participant, questionnaire)
        status = "completed" if not current_question else "pending"

        if current_question:
            current_question_data = {
                "id": current_question.id,
                "order": current_question.order,
                "text": current_question.text,
                "question_type": current_question.question_type,
                "conditional_question_id": current_question.conditional_question_id,
                "conditional_operation": current_question.conditional_operation,
                "conditional_operator": current_question.conditional_operator,
                "conditional_value": current_question.conditional_value,
            }

        return {
            "participant": int(participant),
            "questionnaire": int(questionnaire),
            "status": status,
            "current_question": current_question_data
        }
