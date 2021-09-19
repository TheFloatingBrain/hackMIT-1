from flask import render_template, url_for
from hackmit import app

@app.route("/")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/home")
def home():
    return render_template('home.html')