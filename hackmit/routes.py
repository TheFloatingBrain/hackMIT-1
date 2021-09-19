from flask import render_template, url_for, request, g, session
from werkzeug.utils import redirect
from hackmit import app, get_db, get_user_table, get_pay_table, get_countries
import hackmit.reports as reports
from datetime import date


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user_id = request.form[ "user_id" ]
        password = request.form[ "password" ]
        email = request.form[ "email" ]
        country = request.form[ "country" ]
        if not (password == request.form[ "confirm_password" ]):
            return "Passwords do not match, please try again"
        elif not (email == request.form[ "confirm_email" ]):
            return "Email's do not match, please try again"
        session[ request.form[ "user_id" ] ] = (
            user_id, 
            country, 
            password, 
            email
        )
        redirect(url_for("sign-up-info/" + user_id + "/" + country))
    countries = [country.name for country in list(get_countries())]
    return render_template("sign-up.html", countries = countries)

@app.route("/sign-up-info/<user_id>/<country>", methods=["GET", "POST"])
def sign_up_info(user_id, country):
    pass



@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        get_pay_table().new_entry( 
            get_db(), reports.Payment( 
            request.form[ "procedure_code" ], 
            request.form[ "insurance_plan" ], 
            request.form[ "plan_type" ], 
            date.fromisoformat(request.form[ "date" ]), 
            float( request.form[ "amount" ] ), 
            request.form[ "country" ], 
            request.form[ "state_province" ], 
            request.form[ "county" ], 
        ).to_tuple() )
        get_db().commit()
        return "Your report has been submitted :-)"
    return render_template("report.html")

@app.route("/view", methods=["GET", "POST"])
def view():
    return render_template("view.html")

@app.route("/home")
def home():
    return render_template('home.html')
