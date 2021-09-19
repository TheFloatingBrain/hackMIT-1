from flask import render_template, url_for, request, g
from hackmit import app, get_db, get_table
import hackmit.reports as reports
from datetime import date

@app.route("/report", methods=["GET", "POST"])
def report():
    if request.method == "POST":
        get_table().new_entry( 
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

@app.route("/home")
def home():
    return render_template('home.html')
