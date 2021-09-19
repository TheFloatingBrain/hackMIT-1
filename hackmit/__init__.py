from flask import Flask
from flask import g
from hackmit import reports
import sqlite3
import pycountry

DefaultDatabaseFile = "database.db"

def CreateApp(db_file = DefaultDatabaseFile, 
        payment_table_name = reports.PaymentTableName, 
        user_table_name = reports.UserTableName):
    app = Flask(__name__)
    with app.app_context() as context:
        reports.create_database(db_file, 
                reports.MakeDefaultTable(payment_table_name),
                reports.MakeUserTable(user_table_name))
    return app

app = CreateApp()

def get_countries():
    if 'pycountry' not in g:
        g.countries = pycountry.countries
    return g.countries

def get_db(db_file = DefaultDatabaseFile):
    if 'db' not in g:
        g.db = sqlite3.connect(db_file)
    return g.db

def get_pay_table(table_name = reports.PaymentTableName):
    if 'pay_table' not in g:
        g.pay_table = reports.MakeDefaultTable(table_name)
    return g.pay_table

def get_user_table(table_name = reports.UserTableName):
    if 'user_table' not in g:
        g.user_table = reports.MakeUserTable(table_name)
    return g.user_table

@app.teardown_appcontext
def teardown(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

from hackmit import routes
