import abc
from domain.entities.answer import Answer
from domain.entities.participant import Participant
from domain.entities.questionnaire import Question


class CreateAnswerAnswersIRepository(abc.ABC):
    @abc.abstractmethod
    def add_answer(self, answer: Answer):
        pass


class CreateAnswerParticipantsIRepository(abc.ABC):
    @abc.abstractmethod
    def get_participant(self, participant_id) -> Participant:
        pass


class CreateAnswerQuestionsIRepository(abc.ABC):
    @abc.abstractmethod
    def get_question(self, questionnaire_id, question_id) -> Question:
        pass


class ServiceCreateAnswer:
    answers: CreateAnswerAnswersIRepository = None
    participants: CreateAnswerParticipantsIRepository = None
    questions: CreateAnswerQuestionsIRepository = None

    def execute(self, participant_id, questionnaire_id, question_id, value):
        participant = self.participants.get_participant(participant_id)
        question = self.questions.get_question(questionnaire_id, question_id)

        answer = Answer(question, value, participant)
        self.answers.add_answer(answer)
        return answer
