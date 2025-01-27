from fastapi import FastAPI, Request
from urllib.parse import unquote
from config import TOKEN
from hashlib import sha256, md5
from json import loads
from datetime import datetime
from random import randrange
import hmac
import db
app = FastAPI()

def dcode_and_verify(data):
    try:
        vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in data.split('&')]}
        identificator = loads(vals["user"])['id']
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')
        secret = hmac.new("WebAppData".encode(),TOKEN.encode(),sha256)
        newhash = hmac.new(secret.digest(),data_check_string.encode(),sha256).hexdigest()
        return vals['hash'] == newhash, identificator
    except:
        return False, 0

def validate(token):
    auth_data: db.Authtoken | None = db.session.query(db.Authtoken).filter(db.Authtoken.token == token).first()
    if auth_data is None:
        return 0,0
    return auth_data.user_id, auth_data.access

@app.post("/auth")
async def auth(request: Request):
    a = await request.body()
    answer, identificator = dcode_and_verify(a.decode())
    if answer:
        user: db.User | None = db.session.query(db.User).filter(db.User.telegram_id == identificator).first()
        if user is None:
            return "Not registered"
        newtoken = (md5(f"{randrange(10000000000)}.{randrange(10000000000)}".encode()).hexdigest()
                    +'0'*(10-len(hex(identificator)))+hex(identificator)[2:])
        db.session.add(db.Authtoken(user_id=identificator, created=datetime.now(), token=newtoken, access=user.type))
        db.session.commit()
        return f"{newtoken} {user.type}"
    return "Data corrupred"

@app.get("/registered-to-event")
async def registered_to_event(event_id):
    registrations = db.session.query(db.Registered).where(db.Registered.event_id == event_id).all()