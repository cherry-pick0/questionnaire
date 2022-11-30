import json
from typing import List

import redis

from domain.entities.answer import Answer
from domain.entities.participant import Participant
from domain.entities.questionnaire import Question, Questionnaire


class AnswersRepository:
    @staticmethod
    def get_answers(participant_id, questionnaire_id) -> List[Answer]:
        answers_list = []
        r = redis.Redis(host='localhost', port=6379, db=0)
        participants = json.loads(r.get("participants").decode())
        participant = participants[str(participant_id)]
        answers = participant["answers"]

        questionnaires = json.loads(r.get("questionnaires").decode())
        questionnaire = questionnaires[str(questionnaire_id)]
        questions = questionnaire["questions"]

        participant_entity = Participant(identifier=participant["identifier"], participant_id=participant_id)
        for answer_data in answers:
            question_data = questions[answer_data["question_id"]]
            questionnaire_entity = Questionnaire(questionnaire_id)
            question_data["questionnaire"] = questionnaire_entity
            question_entity = Question(**question_data)

            answer_entity = Answer(participant_entity, question_entity, answer_data["value"], answer_data["id"])
            answers_list.append(answer_entity)

        return answers_list
