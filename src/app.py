from fastapi import FastAPI
from dotenv import load_dotenv

import uvicorn

load_dotenv()
app = FastAPI()


@app.get('/')
def root():
    return {'message': 'CI'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
