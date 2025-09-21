import datetime
import mysql.connector
__mydb=None

def get_sql_connection():
    global __mydb
    __mydb = mysql.connector.connect(
        user="root",
        host='127.0.0.1',
        password="ManuManya@1857;",
        database="gs"
    )
    return __mydb
