import sys

import mysql.connector as _mysql
import tabulate

class ConnectToMySQL:
    def __init__(self, host: str, user: str, passwd: str) -> None:
        self._host = host
        self._user = user
        self._passwd = passwd
        try:
            self._db_connection = _mysql.connect(
                host=self._host, user=self._user, passwd=self._passwd
            )

        except _mysql.errors.ProgrammingError as exc_tb:
            print("\nCould not connect to MySQL server.\n")
            self.show_exception_traceback(exc_tb)
            sys.exit("Terminating script early.\n")
        except Exception as exc_tb:
            print("\n(1) Undocumented error occurred. Refer to exception traceback.\n")
            self.show_exception_traceback(exc_tb)
            sys.exit("Terminating script early.\n")

        self._cursor_object = self._db_connection.cursor()
        print("Connection successful.")

        self._fetched_data = []

    def __enter__(self):
        return self

    def __str__(self) -> str:
        return f"ConnectToMySQL(host='{self._host}', user='{self._user}', passwd='{self._passwd}')"

    def __repr__(self) -> str:
        return f"ConnectToMySQL('To be implemented')"

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close_connection()

    def commit_to_database(self):
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

    def execute_sql_query(self, sql_query: str) -> None:
        try:
            self._cursor_object.execute(sql_query)
            if self.check_result_set() is None:
                print("Query executed successfully (No result set).")
                return

        except Exception as error:
            self.show_exception_traceback(error)

    def fetch_data(self):
        return self._cursor_object.fetchall()

    @staticmethod
    def parameterized_data(data: list | tuple) -> str:
        return ',\n'.join(map(str, data))

    def use_db(self, db_name: str = "") -> None:
        self.execute_sql_query(f"USE {db_name};")

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
