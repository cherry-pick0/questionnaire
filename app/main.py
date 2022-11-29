import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from api import answers, questionnaires, participants

load_dotenv('../.env')

app = FastAPI()
app.include_router(answers.router)
app.include_router(questionnaires.router)
app.include_router(participants.router)


@app.get("/")
async def root():
    pass


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
