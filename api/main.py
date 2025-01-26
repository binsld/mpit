from fastapi import FastAPI
import db
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/whoami/{identificator}")
async def whoami(identificator):
    return db.session.query(db.User).filter(db.User.telegram_id==identificator).first()

@app.post("/new-event")
async def new_event(username: str, password: str):
    return print(username, password)