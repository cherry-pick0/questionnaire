import requests


class TestQuestions:
    def test_questions_flow(self):
        base_url = "http://0.0.0.0:8000/"

        # Get questions
        path = "api/questions"
        response = requests.get(url=f"{base_url}{path}")
        assert response.status_code == 200

        expected_data = [
            {
                "id": 1,
                "order": 1,
                "text": "When were you born?",
                "type": "date",
                "conditional_question_id": None,
                "conditional_operation": None,
                "conditional_value": None,
            },
            {
                "id": 2,
                "order": 2,
                "text": "How much do you weigh?",
                "type": "integer",
                "conditional_question_id": 1,
                "conditional_operation": "date_number_of_years",
                "conditional_operator": ">",
                "conditional_value": 35,
            },
            {
                "id": 3,
                "order": 3,
                "text": "How often do you dye your hair?",
                "type": "integer",
                "conditional_question_id": 1,
                "conditional_operation": "date_number_of_years",
                "conditional_operator": "<=",
                "conditional_value": 35,
            }
        ]
