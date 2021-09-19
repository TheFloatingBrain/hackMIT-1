from hackmit.reports import User
from hackmit.reports import DatabaseTable

def retrieve_from_database(connection, user_id: str, password: str) -> User:
    fields = [ field[ 0 ] for field in User.__dataclass_fields__.items() ]
    row = tuple( connection.cursor().execute(
            "SELECT " + ", ".join(fields) + \
            " FROM Users WHERE user_id = " + \
            user_id + " AND password = " + password)[ 0 ] )
    return User(**row)

def create_new_user(connection, table: DatabaseTable, user: User, password: str, email: str):
    connection.cursor().execute(table.table_insert_string(), (*user.to_tuple(), password, email))
