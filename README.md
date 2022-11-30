## Instructions

Note: Instructions for Linux/Ubuntu
    
### 1) Setup
 
Install:
     
   * pipenv

### 2) Start a project
        

        # Create and enter virtual environment
        cd app
        pipenv shell
        
        # Install dependencies
        pipenv install
   
        # Run the app
        uvicorn main:app --reload
        
        # Go to http://127.0.0.1:8000/docs

### 3) Tests
   

        cd app
        pytest api/questionnaire_flow_test.py

### 4) Samples

#### Create participant

      curl -X 'POST' \
     'http://127.0.0.1:8000/api/participants' \
     -H 'accept: application/json' \
     -d ''

#### Get questionnaires

      curl -X 'GET' \
        'http://127.0.0.1:8000/api/questionnaires' \
        -H 'accept: application/json'

#### Getting the question (api/questionnaire-flow)

      curl -X 'GET' \
        'http://127.0.0.1:8000/api/questionnaire-flow?questionnaire=1&participant=82' \
        -H 'accept: application/json'

#### Answering the question (api/answers")

      curl -X 'POST' \
        'http://127.0.0.1:8000/api/answers' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "participant_id": 0,
        "questionnaire_id": 0,
        "question_id": 0,
        "value": "string"
      }'

#### Listing answers (api/answers")
      
      curl -X 'GET' \
        'http://127.0.0.1:8000/api/answers?participant_id=82&questionnaire_id=1' \
        -H 'accept: application/json'
