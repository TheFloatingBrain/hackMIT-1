from flask import Flask
from flask import g
from hackmit import reports
import sqlite3


DefaultDatabaseFile = "database.db"

def CreateApp(db_file = DefaultDatabaseFile, 
        table_name = reports.PaymentTableName):
    app = Flask(__name__)
    with app.app_context() as context:
        reports.create_database(db_file, 
                reports.MakeDefaultTable(table_name))
    return app

app = CreateApp()

def get_db(db_file = DefaultDatabaseFile):
    if 'db' not in g:
        g.db = sqlite3.connect(db_file)
    return g.db

def get_table(table_name = reports.PaymentTableName):
    if 'table' not in g:
        g.table = reports.MakeDefaultTable(table_name)
    return g.table

@app.teardown_appcontext
def teardown(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

from hackmit import routes
