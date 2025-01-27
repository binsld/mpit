from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def root():
    return render_template("root.html")

@app.get("/events")
def events():
    return render_template("events.html")

@app.get("/merch")
def tovarum():
    return render_template("tovarum.html")
