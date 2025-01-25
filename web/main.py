from flask import Flask

app = Flask(__name__)
test_head = "<a href='/'>Главная</a> <a href='/profile'>Профиль</a> <a href='/moderator'>Страничка модератора</a> <a href='/administrator'>Страничка админа</a><br>"

@app.get("/")
def root():
    return (test_head+"<p>Здесь у нас находится мерч</p>")


@app.get("/logs")
def logs():
    return (test_head+"<p>Здесь у нас находятся логи</p>")

@app.get("/profile")
def profile():
    return (test_head+"<p>Здесь у нас находится профиль пользователя</p>")

@app.get("/moderator")
def moderator():
    return (test_head+"<p>Здесь у нас находится панель управления модератора</p>")


@app.get("/administrator")
def administrator():
    return (test_head+"<p>Здесь у нас находится панель управления администратора</p><br><a href='/logs'>Логи</a>")
