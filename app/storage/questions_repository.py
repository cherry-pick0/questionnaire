import json
from typing import List

import redis

from domain.entities.questionnaire import Question
from domain.services.create_questionnaire import CreateQuestionnaireQuestionsIRepository
from domain.services.current_flow import CurrentFlowQuestionsIRepository


class QuestionsRepository(CreateQuestionnaireQuestionsIRepository, CurrentFlowQuestionsIRepository):
    def add_question(self, question_entity: Question):
        r = redis.Redis(host='localhost', port=6379, db=0)

        questionnaires = json.loads(r.get("questionnaires").decode())
        questionnaire = questionnaires[str(question_entity.questionnaire.id)]
        questions = questionnaire["questions"]

        questions[question_entity.id] = {
            "id": question_entity.id,
            "questionnaire_id": question_entity.questionnaire.id,
            "order": question_entity.order,
            "text": question_entity.text,
            "type": question_entity.question_type,
            "conditional_question_id": question_entity.conditional_question_id,
            "conditional_operation": question_entity.conditional_operation,
            "conditional_value": question_entity.conditional_value
        }

        questionnaire["questions"] = questions

        r.set("questionnaires", json.dumps(questionnaires))

        return question_entity

    def get_current_question(self, participant: int, questionnaire: int) -> List[Question]:
        pass

    def questions_completed(self, participant: int, questionnaire: int) -> bool:
        pass
