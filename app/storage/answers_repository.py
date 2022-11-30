import json
from typing import List

import redis

from domain.entities.answer import Answer
from domain.entities.participant import Participant
from domain.entities.questionnaire import Question, Questionnaire
from domain.services.create_answer import CreateAnswerAnswersIRepository


class AnswersRepository(CreateAnswerAnswersIRepository):
    @staticmethod
    def add_answer(answer: Answer):
        participant_id = answer.participant.id

        r = redis.Redis(host='localhost', port=6379, db=0)
        participants = json.loads(r.get("participants").decode())
        participant = participants[str(answer.participant.id)]
        answers = participant["answers"]

        filtered_answers = [a for a in answers if a.question.id == answer.question.id]
        if filtered_answers:
            answer_id = int(filtered_answers[0]["id"])
        else:
            answer_id = len(list(answers.keys())) + 1

        answers[answer_id] = {
            "id": answer_id,
            "value": answer.value,
            "question_id": answer.question.id
        }
        participant["answers"] = answers
        participants[str(participant_id)] = participant

        r.set("participants", json.dumps(participants))
        answer.id = answer_id

        return answer

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
        for key in answers.keys():
            answer_data = answers[key]
            question_data = questions[str(answer_data["question_id"])]
            questionnaire_entity = Questionnaire(questionnaire_id)
            question_data["questionnaire"] = questionnaire_entity
            question_data["question_id"] = question_data.pop("id")
            question_entity = Question(**question_data)

            answer_entity = Answer(participant_entity, question_entity, answer_data["value"], answer_data["id"])
            answers_list.append(answer_entity)

        return answers_list
