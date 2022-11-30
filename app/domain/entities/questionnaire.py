from typing import Union


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
    conditional_value: Union[int, str]

    def __init__(self, question_id, questionnaire, order, text, question_type, conditional_question_id,
                 conditional_operation, conditional_value):
        self.id = question_id
        self.questionnaire = questionnaire
        self.order = order
        self.text = text
        self.question_type = question_type
        self.conditional_question_id = conditional_question_id
        self.conditional_operation = conditional_operation
        self.conditional_value = conditional_value
