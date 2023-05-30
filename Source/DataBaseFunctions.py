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
