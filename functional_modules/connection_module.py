import mysql.connector as _mysql
import sys
from typing import Any


class ConnectToMySQL:
    def __init__(
        self, host: str, user: str, passwd: str, database: str, dev_mode: bool
    ) -> None:
        self._host = host
        self._user = user
        self._passwd = passwd
        self._database = database

        self._dev_mode = dev_mode

        self._default_query = "SELECT school_id as 'School ID', school_name as 'School Name' FROM schools_data;"

    def connect_to_database(self) -> None:
        try:
            self._db_connection = _mysql.connect(
                host=self._host,
                user=self._user,
                passwd=self._passwd,
                database=self._database,
            )

        except Exception as error:
            print(
                "Database connection failed. Refer to following error report for more:\n"
            )

            self.show_exception_traceback(error)

            print("\nTerminating script early.")
            sys.exit()

    def create_cursor_object(self) -> None:
        self._cursor_object = self._db_connection.cursor()

    def execute_sql_query(self, sql_query: str) -> None:
        try:
            if self._dev_mode:
                print(f"[DEV MODE] Executing SQL Query: \n{sql_query}\n")
            self._cursor_object.execute(sql_query)
        except Exception as error:
            self.show_exception_traceback(error)
            self.close_connection()

    def fetch_data(self) -> Any:
        return self._cursor_object.fetchall()

    def close_connection(self) -> None:
        self._db_connection.close()

    def check_connection(self) -> bool:
        return self._db_connection.is_connected()

    def check_result_set(self):
        return self._cursor_object.description

    def get_column_name(self):
        return self._cursor_object.description

    def rows_retrieved(self) -> int:
        return self._cursor_object.rowcount

    def show_exception_traceback(self, e: Exception) -> None:
        if self._dev_mode:
            print("[DEV MODE] Showing full exception traceback:\n")
            print(repr(e))
        else:
            print(e)

        return

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return ""

    def __exit__(self) -> None:
        return


if __name__ == "__main__":
    print("You are not supposed to run this program by itself.")
    sys.exit()
