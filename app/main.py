import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv('../.env')

app = FastAPI()


@app.get("/")
async def root():
    pass


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
