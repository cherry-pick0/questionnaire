import json

import redis

from domain.entities.questionnaire import Questionnaire, Question
from domain.services.create_questionnaire import CreateQuestionnaireQuestionnaireIRepository, \
    CreateQuestionnaireQuestionsIRepository


class QuestionnaireRepository(CreateQuestionnaireQuestionnaireIRepository):
    def add_questionnaire(self, questionnaire_entity: Questionnaire):
        r = redis.Redis(host='localhost', port=6379, db=0)

        questionnaires = r.get("questionnaires")

        if not questionnaires:
            r.set("questionnaires", "{}")
            questionnaires = r.get('questionnaires')

        questionnaires = json.loads(questionnaires.decode())

        questionnaire = {"questions": {}}
        questionnaires[questionnaire_entity.id] = questionnaire

        r.set("questionnaires", json.dumps(questionnaires))

        return questionnaire_entity


class QuestionsRepository(CreateQuestionnaireQuestionsIRepository):
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
