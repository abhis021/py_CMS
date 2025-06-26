import sqlite3
from config import DATABASE_FILE

class Database:
    def __init__(self, db_path=DATABASE_FILE):
        self.db_path = db_path
    
    def initialize_schema(self, sql_file='schema.sql'):
        conn = self.connect()
        try:
            with open(sql_file, 'r') as f:
                conn.executescript(f.read())
        except Exception as e:
            print(f"[SCHEMA ERROR] {e}")
        finally:
            conn.close()


    def connect(self):
        """Creates a new connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=None):
        """Executes INSERT, UPDATE, DELETE queries."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or [])
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query, params=None):
        """Fetches all results from a SELECT query."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or [])
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def fetch_one(self, query, params=None):
        """Fetches a single result from a SELECT query."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or [])
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[DB ERROR] {e}")
            return None
        finally:
            cursor.close()
            conn.close()
