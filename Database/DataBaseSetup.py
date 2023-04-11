import sqlite3 as sq
import os

DB_SCHEMA = 'Database/schema.sql'


def dataBaseExist():
    """Return true if database file exist."""
    return os.path.exists('Database/database.db')


def createDataBase():
    conn = sq.connect('Database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
    
        CREATE TABLE Assets (
            Asset_ID integer,
            Asset_type string,
            name string)
            
    ''')

    cursor.execute('''
        insert into Assets (Asset_ID, Asset_type, name) values (1, "Zloto", "Britania")
    ''')
    conn.commit()
    return conn


def setupShema(connection):
    with open(DB_SCHEMA, 'r') as rf:
        # Read the schema from the file
        schema = rf.read()
    connection.executescript(schema)


def connectDatabase():
    return sq.connect('Database/database.db')
