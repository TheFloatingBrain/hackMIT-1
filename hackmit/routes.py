from flask import render_template, url_for, request
from hackmit import app

@app.route("/")

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        return( request.form["amount"] )
    return render_template("report.html")

@app.route("/home")
def home():
    return render_template('home.html')