from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def root():
    return render_template("events.html")

@app.get("/events")
def events():
    return render_template("events.html")

@app.get("/check")
def check():
    return render_template("check.html")

@app.get("/tovarum")
def tovarum():
    return render_template("tovarum.html")
