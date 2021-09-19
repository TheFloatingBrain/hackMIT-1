import sqlite3
import datetime
from dataclasses import dataclass
from os.path import exists

PaymentTableName = "Payments"
UserTableName = "Users"

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
        return (self.procedure_code, self.insurance_plan, self.plan_type, 
                self.date, self.amount, self.country, self.state_province, self.county)
    
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


@dataclass
class User:
    user_id: str
    insurance_plan: str
    plan_type: str
    country: str
    state_province: str
    county: str

    def create_payment(self, procedure_code: str, 
            date: datetime.date, 
            amount: float):
        return Payment(procedure_code, self.insurance_plan, 
                self.plan_type, date, amount, self.country, 
                self.state_province, self.county )
    
    def to_tuple(self):
        return (self.insurance_plan, self.plan_type, 
                self.country, self.state_province, 
                self.county)

    def from_tuple(self, insurance_plan: str, 
            plan_type: str, country: str, 
            state_province: str, county: str):
        self.insurance_plan = insurance_plan
        self.plan_type = plan_type
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
        return "CREATE TABLE " + self.name + " (" + ", ".join( 
                [ field[ 1 ] + " " + field[ 0 ] for field in self.fields ] ) + ")"

    def table_insert_string(self):
        return "INSERT INTO " + self.name + " VALUES(" + ", ".join( 
                [ "?" for field in self.fields ] ) + ")"

    def new_entry(self, connection, data):
        connection.cursor().execute(
                self.table_insert_string(), 
                data)

    def new_entries(self, connection, data: list):
        connection.cursor().executemany(
                self.create_insertion_string(), 
                data)

def MakeUserTable(table_name = UserTableName):
    user_table = DatabaseTable(table_name)
    for field in User.__dataclass_fields__.items():
        user_table.new_field(field[ 0 ], field[ 1 ].type)
    user_table.text("password").text("email")
    return user_table

def MakeDefaultTable(payment_table_name = PaymentTableName):
    default_table = DatabaseTable(payment_table_name)
    for field in Payment.__dataclass_fields__.items():
        default_table.new_field(field[ 0 ], field[ 1 ].type)
    return default_table

def create_database(file_name: str, 
        payment_table: DatabaseTable, 
        user_table: DatabaseTable):
    if not exists(file_name):
        with sqlite3.connect(file_name) as connection:
            cursor = connection.cursor()
            cursor.execute(payment_table.create_table_string())
            cursor.execute(user_table.create_table_string())
