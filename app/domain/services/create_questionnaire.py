import abc
import json
from domain.entities.questionnaire import Questionnaire, Question


class CreateQuestionnaireQuestionnaireIRepository(abc.ABC):
    @abc.abstractmethod
    def add_questionnaire(self, questionnaire: Questionnaire):
        pass


class CreateQuestionnaireQuestionsIRepository(abc.ABC):
    @abc.abstractmethod
    def add_question(self, question: Question):
        pass


class ServiceCreateQuestionnaire:
    questionnaires: CreateQuestionnaireQuestionnaireIRepository = None
    questions: CreateQuestionnaireQuestionsIRepository = None

    def execute(self):
        file = open("domain/services/mock_questionnaire.json")
        data = json.load(file)

        questionnaire_data = data['questionnaires'][0]
        questionnaire_id = questionnaire_data["id"]
        questionnaire_entity = Questionnaire(questionnaire_id)

        self.questionnaires.add_questionnaire(questionnaire_entity)

        for question_data in questionnaire_data["questions"]:
            question_data["questionnaire"] = questionnaire_entity
            question_data["question_id"] = question_data.pop("id")
            question_entity = Question(**question_data)
            self.questions.add_question(question_entity)

        return questionnaire_entity
