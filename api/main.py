from fastapi import FastAPI
from db import session, User
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/whoami/{identificator}")
async def whoami(identificator):
    return

