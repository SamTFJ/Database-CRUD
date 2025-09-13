# dbconnection.py
import os
import psycopg2
from psycopg2 import sql, OperationalError, DatabaseError
from dotenv import load_dotenv
from typing import Any, List, Optional

# ensures it loads from the .env in the current folder (override for development)
load_dotenv(dotenv_path=".env", override=True)

class DBconnect:
    def __init__(self):
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cur: Optional[psycopg2.extensions.cursor] = None
        self._connect()

    def _connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("db_name"),
                user=os.getenv("db_user"),
                password=os.getenv("db_password"),
                host=os.getenv("db_host"),
                port=os.getenv("db_port")
            )
            self.cur = self.conn.cursor()
        except (OperationalError, Exception) as err:
            # prints useful info and keeps attributes as None for future calls to check
            print("Error while connecting to PostgreSQL:", err)
            self.conn = None
            self.cur = None

    def end_connection(self):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print("Error closing connection:", e)
        finally:
            self.cur = None
            self.conn = None

    def _ensure_connection(self):
        if self.conn is None or self.cur is None:
            self._connect()
        if self.conn is None or self.cur is None:
            raise ConnectionError("No database connection available.")

    def execute_command(self, sqlcommand: Any, params: Optional[tuple] = None,
                          fetch: bool = False, fetch_one: bool = False) -> Optional[List[tuple]]:
        """
        Executes an SQL command.
        - sqlcommand: SQL string or psycopg2.sql.SQL
        - params: tuple with parameters (or None)
        - fetch: if True, returns cur.fetchall()
        - fetch_one: if True, returns cur.fetchone()
        Returns None on error.
        """
        try:
            self._ensure_connection()
            self.cur.execute(sqlcommand, params)
            # Commit only if necessary (INSERT/UPDATE/DELETE) - safe to always do
            try:
                self.conn.commit()
            except Exception:
                # some read-only connections don't require it, ignore
                pass

            if fetch_one:
                return [self.cur.fetchone()]
            if fetch:
                return self.cur.fetchall()
            return None
        except (DatabaseError, Exception) as e:
            # rolls back if possible and shows the error
            if self.conn:
                try:
                    self.conn.rollback()
                except Exception:
                    pass
            print("Database error:", e)
            raise  # re-raises for the caller to handle (or remove raise if you prefer to return None)