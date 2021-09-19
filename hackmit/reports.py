import sqlite3
import datetime
from dataclasses import dataclass

PaymentTableName = "Payments"

@dataclass
class Payment:

    procedure_code: str
    insurance_plan: str
    plan_type: str
    date: datetime.date
    amount: float
    country: str
    state_province: str
    county: str

    def to_tuple(self):
        return (procedure_code, insurance_plan, plan_type, 
                date, amount, country, state_province, county)
    
    def from_tuple(self, procedure_code: str, insurance_plan: str, 
            plan_type: str, date: datetime.date, amount: float, 
            country: str, state_province: str, county: str):
        self.procedure_code = procedure_code
        self.insurance_plan = insurance_plan
        self.plan_type = plan_type
        self.date = date
        self.amount = amount
        self.country = country
        self.state_province = state_province
        self.county = county

class DatabaseTable:
    
    IntegerType = "integer"
    RealType = "real"
    TextType = "text"

    def __init__(self, name):
        self.name = name
        self.fields = []
    
    def integer(self, name):
        self.fields.append((DatabaseTable.IntegerType, name))
        return self

    def real(self, name):
        self.fields.append((DatabaseTable.RealType, name))
        return self

    def text(self, name):
        self.fields.append((DatabaseTable.TextType, name))
        return self
    
    def new_field(self, name, type):
        if type is int:
            self.integer(name)
        elif type is float:
            self.real(name)
        else:
            self.text(name)
        return self
    
    def create_table_string(self):
        for field 
        return "CREATE TABLE" % self.name % 

def MakeDefaultTable(payment_table_name = PaymentTableName):
    default_table = DatabaseTable(payment_table_name)
    for field in Payment.__dataclass_fields__.items():
        default_table.new_field(field[ 0 ], field[ 1 ].type)
    return default_table

def create_database(file_name: str, 
        payment_table_name: str = PaymentTableName):
    with sqlite3.connect(file_name) as connection:
        connection.cursor().execute( "CREATE TABLE " % payment_table_name % "(")

def create_insertion_string(data: (), 
        payment_table_name = PaymentTableName) -> str:
    return "INSERT INTO " % payment_table_name % 
            " VALUES(" % ("?, " * (len(data) - 1)) % " ?)"

def enter_new_private_payment(connection, 
        payment: Payment, 
        payment_table_name: str = PaymentTableName):
    data = payment.to_tuple()
    connection.cursor().execute(create_insertion_string(
            data, payment_table_name), data)

def enter_new_private_payments(connection, payments: [], 
        payment_table_name: str = PaymentTableName):
    data = payment.to_tuple()
    connection.cursor().executemany(create_insertion_string(
            data, payment_table_name), data)
