import json
from typing import List, Optional

import redis

from domain.entities.questionnaire import Question, Questionnaire
from domain.services.create_answer import CreateAnswerQuestionsIRepository
from domain.services.create_questionnaire import CreateQuestionnaireQuestionsIRepository
from domain.services.current_flow import CurrentFlowQuestionsIRepository
from storage.answers_repository import AnswersRepository


class QuestionsRepository(CreateQuestionnaireQuestionsIRepository,
                          CurrentFlowQuestionsIRepository,
                          CreateAnswerQuestionsIRepository):
    def add_question(self, question_entity: Question):
        r = redis.Redis(host='localhost', port=6379, db=0)

        questionnaires = json.loads(r.get("questionnaires").decode())
        questionnaire = questionnaires[str(question_entity.questionnaire.id)]
        questions = questionnaire["questions"]

        questions[question_entity.id] = {
            "id": question_entity.id,
            "order": question_entity.order,
            "text": question_entity.text,
            "question_type": question_entity.question_type,
            "conditional_question_id": question_entity.conditional_question_id,
            "conditional_operation": question_entity.conditional_operation,
            "conditional_operator": question_entity.conditional_operator,
            "conditional_value": question_entity.conditional_value
        }

        questionnaire["questions"] = questions

        r.set("questionnaires", json.dumps(questionnaires))

        return question_entity

    @staticmethod
    def get_question(questionnaire_id, question_id) -> Question:
        r = redis.Redis(host='localhost', port=6379, db=0)
        questionnaires = json.loads(r.get("questionnaires").decode())
        questionnaire = questionnaires[str(questionnaire_id)]
        questions = questionnaire["questions"]
        question_data = questions[str(question_id)]
        questionnaire_entity = Questionnaire(questionnaire_id)
        question_data["questionnaire"] = questionnaire_entity
        question_data["question_id"] = question_data.pop("id")
        return Question(**question_data)

    @staticmethod
    def get_questions(questionnaire_id) -> List[Question]:
        questions_list = []
        r = redis.Redis(host='localhost', port=6379, db=0)
        questionnaires = json.loads(r.get("questionnaires").decode())
        questionnaire = questionnaires[str(questionnaire_id)]
        questions = questionnaire["questions"]

        questionnaire_entity = Questionnaire(questionnaire_id)
        for key in questions.keys():
            question_data = questions[key]
            question_data["questionnaire"] = questionnaire_entity
            question_data["question_id"] = question_data.pop("id")
            question_entity = Question(**question_data)
            questions_list.append(question_entity)

        questions_list.sort(key=lambda question: question.order)
        return questions_list

    def get_current_question(self, participant_id: int, questionnaire_id: int) -> Optional[Question]:
        questions = self.get_questions(questionnaire_id)
        answers_repo = AnswersRepository()
        answers = answers_repo.get_answers(participant_id, questionnaire_id)

        for question in questions:
            filtered_answers = [a for a in answers if a.question.id == question.id]
            if not filtered_answers:

                # Question not answered yet
                if not question.conditional_question_id:
                    return question

                conditional_answers = [a for a in answers if a.question.id == question.conditional_question_id]
                if not conditional_answers:
                    return

                conditional_answer = conditional_answers[0]
                show = question.show_based_on_condition(conditional_answer)

                if show:
                    return question
