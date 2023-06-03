import sqlite3
import os.path

from Source import Settings


def connectDataBase(filePath):
    """Return connect object to database from filePath. If file does not exist, creates and setup new database."""
    conn = None

    if os.path.exists(filePath):
        try:
            conn = sqlite3.connect(filePath, 5)
        except sqlite3.OperationalError:
            print('Connection to database error: ', sqlite3.OperationalError)

    else:
        try:
            conn = sqlite3.connect(filePath)
        except sqlite3.OperationalError:
            print('Connection to database error: ', sqlite3.OperationalError)
        else:
            try:
                with open(Settings.dataBaseDirectoryPath.joinpath('CreateTable.sql')) as script:
                    conn.executescript(script.read())
                    conn.commit()
            except FileNotFoundError:
                print('Error: Script CreateTable.sql not found.')

    return conn


def loadData(connection: sqlite3.Connection, tableName: str):
    """Load and return rows from given table using connection. If table not exist return None."""
    try:
        cursor = connection.execute(f"SELECT * FROM {tableName};")
        return cursor

    except sqlite3.OperationalError:
        print(f'Error: Table {tableName} not exist.')
        return None
