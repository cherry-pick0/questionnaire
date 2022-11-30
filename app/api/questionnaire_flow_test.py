import json

import requests


class TestQuestionnaireFlow:
    def test_questionnaire_flow(self):
        base_url = "http://0.0.0.0:8000/"

        # Create a participant
        path = "api/participants"
        participant_data = {}
        response = requests.post(url=f"{base_url}{path}", data=json.dumps(participant_data))
        assert response.status_code == 201
        participant_id = json.loads(response.text)["id"]

        # Get questionnaire
        path = "api/questionnaires"
        response = requests.get(url=f"{base_url}{path}")
        assert response.status_code == 200
        assert len(response.json()) == 1
        questionnaire_id = response.json()[0]["id"]

        # Get questionnaire with the first question
        path = "api/questionnaire-flow"
        response = requests.get(url=f"{base_url}{path}", params={"questionnaire": questionnaire_id,
                                                                 "participant": participant_id})
        assert response.status_code == 200

        expected_data = {
            "participant": int(participant_id),
            "questionnaire": int(questionnaire_id),
            "status": "pending",
            "current_question":
                {
                    "id": 1,
                    "order": 1,
                    "text": "When were you born?",
                    "question_type": "date",
                    "conditional_question_id": None,
                    "conditional_operation": None,
                    "conditional_operator": None,
                    "conditional_value": None,
                }
        }

        assert expected_data == response.json()

        # Answer question one
        path = "api/answers"
        question_data = {
            "question_id": 1,
            "value": "01-01-1900",
            "participant_id": participant_id,
            "questionnaire_id": questionnaire_id,
        }

        response = requests.post(url=f"{base_url}{path}", data=json.dumps(question_data))
        assert response.status_code == 201
        answer_id = response.json()["id"]

        expected_data = {
            "id": answer_id,
            "question_id": 1,
            "value": "01-01-1900"
        }
        assert expected_data == response.json()

        # Get questionnaire with the second question
        path = "api/questionnaire-flow"
        response = requests.get(url=f"{base_url}{path}", params={"questionnaire": questionnaire_id,
                                                                 "participant": participant_id})
        assert response.status_code == 200

        expected_data = {
            "participant": participant_id,
            "questionnaire": questionnaire_id,
            "status": "pending",
            "current_question":
                {
                    "id": 2,
                    "order": 2,
                    "text": "How much do you weigh?",
                    "question_type": "integer",
                    "conditional_question_id": 1,
                    "conditional_operation": "date_number_of_years",
                    "conditional_operator": ">",
                    "conditional_value": 35,
                }
        }

        assert expected_data == response.json()

        # Answer question two
        path = "api/answers"
        question_data = {
            "question_id": 2,
            "value": 70
        }
        response = requests.post(url=f"{base_url}{path}", data=json.dumps(question_data))
        assert response.status_code == 201
        answer_id = json.loads(response.text)[0]["id"]
        expected_data = {
            "id": answer_id,
            "question_id": 2,
            "value": 70
        }
        assert expected_data == response.json()

        # Get questionnaire
        path = "api/questionnaire-flow"
        response = requests.get(url=f"{base_url}{path}", params={"questionnaire": questionnaire_id,
                                                                 "participant": participant_id})
        assert response.status_code == 200

        expected_data = {
            "participant": participant_id,
            "questionnaire": questionnaire_id,
            "status": "completed",
            "current_question": None
        }

        assert expected_data == response.json()

        # Get all answers
        path = "api/answers"
        response = requests.get(url=f"{base_url}{path}", params={"participant": participant_id})
        assert response.status_code == 200

        expected_data = [
            {
                "participant": participant_id,
                "value": "01-01-1900",
                "question_id": 1,
                "question_text": "When were you born?",
                "question_type": "date",
                "question_order": 1,
            },
            {
                "participant": participant_id,
                "value": 70,
                "question_id": 2,
                "question_text": "How much do you weigh?",
                "question_type": "integer",
                "question_order": 2,
            }
        ]

        assert expected_data == response.json()
