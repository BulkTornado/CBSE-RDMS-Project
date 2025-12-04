import sys

import mysql.connector as _mysql


class ConnectToMySQL:
    def __init__(self, host: str, user: str, passwd: str) -> None:
        self._host = host
        self._user = user
        self._passwd = passwd
        try:
            self._db_connection = _mysql.connect(
                host=self._host, user=self._user, passwd=self._passwd
            )
            """if not self.check_connection():
                print("Connection failed.")
                sys.exit()"""
            print("Connection successful.")

        except _mysql.errors.ProgrammingError as exc_tb:
            print("\nCould not connect to MySQL server.\n")
            self.show_exception_traceback(exc_tb)
            sys.exit("Terminating script early.\n")
        except Exception as exc_tb:
            print("\nAn undocumented error occurred. Refer to exception traceback.\n")
            self.show_exception_traceback(exc_tb)
            sys.exit("Terminating script early.\n")

        self._cursor_object = self._db_connection.cursor()
        print(
            "Connection has been successfully made and a cursor object has been instantiated."
        )

        # self._default_query = "SELECT school_id as 'School ID', school_name as 'School Name' FROM schools_data;"

    def __enter__(self):
        return self

    def __str__(self) -> str:
        return f"{__name__}"

    def __repr__(self) -> str:
        return ""

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close_connection()

    def use_db(self, db_name: str = "") -> None:
        self.execute_sql_query(f"USE {db_name};")

    def execute_sql_query(self, sql_query: str) -> None:
        try:
            self._cursor_object.execute(sql_query)
            if self.check_result_set() is None:
                print("Query executed successfully (No result set).")
                self._commit()
                return
        except Exception as error:
            self.show_exception_traceback(error)

    def fetch_data(self):
        return self._cursor_object.fetchall()

    def _commit(self):
        self._db_connection.commit()

    def check_connection(self) -> bool:
        return self._db_connection.is_connected()

    def close_connection(self) -> None:
        if not self.check_connection():
            print("Connection has already been closed.")
            return
        self._db_connection.close()
        print("Connection closed successfully.")
        return

    def check_result_set(self):
        return self._cursor_object.description

    def get_column_name(self):
        return self._cursor_object.description

    def rows_retrieved(self) -> int:
        return self._cursor_object.rowcount

    def show_exception_traceback(self, exc_tb: Exception) -> None:
        print(f"Exception traceback:\n{exc_tb}\n")
        print(f"Full exception traceback:\n{repr(exc_tb)}\n")
        return


if __name__ == "__main__":
    print("You are not supposed to run this program by itself.")
    sys.exit()
