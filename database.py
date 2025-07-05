import sqlite3
import os
import sys
import shutil

def resource_path(relative_path):
    """ Get path to resource, works for dev and for PyInstaller bundles """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_writable_db_path():
    """ Returns a user-writable path for the database file """
    appdata = os.getenv('APPDATA') or os.path.expanduser("~")
    target_dir = os.path.join(appdata, "ClinicCMS")
    os.makedirs(target_dir, exist_ok=True)

    bundled_db = resource_path("clinic.db")
    target_db = os.path.join(target_dir, "clinic.db")

    if not os.path.exists(target_db):
        shutil.copy(bundled_db, target_db)

    return target_db

class Database:
    def __init__(self, db_path=None):
        self.db_path = db_path or get_writable_db_path()

    def initialize_schema(self, sql_file='schema.sql'):
        conn = self.connect()
        try:
            with open(resource_path(sql_file), 'r') as f:
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