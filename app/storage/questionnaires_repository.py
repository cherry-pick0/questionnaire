import json

import redis

from domain.entities.questionnaire import Questionnaire
from domain.services.create_questionnaire import CreateQuestionnaireQuestionnaireIRepository


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

