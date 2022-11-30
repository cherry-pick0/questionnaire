from datetime import datetime
from typing import Union

from dateutil import relativedelta

from domain.entities.answer import Answer


class Questionnaire:
    id: int

    def __init__(self, questionnaire_id):
        self.id = questionnaire_id


class Question:
    id: int
    questionnaire: Questionnaire
    order: int
    text: str
    question_type: str
    conditional_question_id: int
    conditional_operation: str
    conditional_operator: str
    conditional_value: Union[int, str]

    OPERATIONS = ["date_number_of_years"]
    OPERATORS = ["==", ">", "<", "<="]

    def __init__(self, question_id, questionnaire, order, text, question_type, conditional_question_id,
                 conditional_operation, conditional_operator, conditional_value):
        self.id = question_id
        self.questionnaire = questionnaire
        self.order = order
        self.text = text
        self.question_type = question_type
        self.conditional_question_id = conditional_question_id
        self.conditional_operation = conditional_operation
        self.conditional_operator = conditional_operator
        self.conditional_value = conditional_value

    def show_based_on_condition(self, conditional_answer: Answer):
        if self.conditional_operation == "date_number_of_years":
            date = datetime.strptime(conditional_answer.value, "%Y-%m-%d")
            diff = relativedelta.relativedelta(datetime.now(), date)
            num_years = diff.years

            if self.conditional_operator == ">":
                return num_years > self.conditional_value

            if self.conditional_operator == "<=":
                return num_years <= self.conditional_value

        return True
