import sqlite3
import os.path


def connectDataBase(filePath):
    """Return connect object to database from filePath. If file does not exist, creates and setup new database."""
    if os.path.exists(filePath):
        return sqlite3.connect(filePath, 5)

    else:
        conn = sqlite3.connect(filePath)
        try:
            with open('../Database/CreateTable.sql') as script:
                conn.executescript(script.read())
                conn.commit()
        except FileNotFoundError:
            print('Error: Script CreateTable.sql not found.')
            return None

        return conn


def loadData(connection, tableName):
    """Load and return rows from given table using connection. If table not exist return None."""
    try:
        cursor = connection.execute(f"SELECT * FROM {tableName};")
        return cursor

    except sqlite3.OperationalError:
        print(f'Error: Table {tableName} not exist.')
        return None


connn = connectDataBase('../Database/test.db')
loadData(connn, 'GOLDSE')
