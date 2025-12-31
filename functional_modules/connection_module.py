import sys

import mysql.connector as _mysql

class ConnectToMySQL:
    def __init__(self, host: str, user: str, passwd: str) -> None:
        self._host = host
        self._user = user
        self._passwd = passwd

        self._result_set = []
        self._exception_history = []


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

        self._cursor = self._db_connection.cursor()
        print("Connection successful.")


    def __enter__(self):
        return self

    def __str__(self) -> str:
        return f"ConnectToMySQL(host='{self._host}', user='{self._user}', passwd='{self._passwd}')"

    def __repr__(self) -> str:
        return f"ConnectToMySQL('To be implemented')"

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close_connection()

    def commit_to_database(self, silent=False):
        self._db_connection.commit()
        if not silent:
            print("(COMMIT successful)")

    def check_connection(self) -> bool:
        return self._db_connection.is_connected()

    def close_connection(self) -> None:
        if not self.check_connection():
            print("Connection has already been closed.")
            return
        self._db_connection.close()
        print("\nConnection closed successfully.\n")
        return

    def execute_sql_query(self, sql_query: str) -> None:
        try:
            self._cursor.execute(sql_query)
            print("Query executed successfully")
            _result_set = self._cursor.description
            _fetched_data = self._cursor.fetchall()
            _row_count = self._cursor.rowcount
            if _result_set is not None:
                self._result_set.append((_result_set, _fetched_data, _row_count))
                print("(Query result stored)\n")
            else:
                print("(No result set)\n")

        except Exception as error:
            self.show_exception_traceback(error)

    def insert_data(self, sql_query: str, data):
        try:
            self._cursor.executemany(sql_query, data)
        except Exception as error:
            self.show_exception_traceback(error)


    def fetch_data(self):
        return self._result_set[-1]

    @staticmethod
    def parameterized_data(data: list | tuple) -> str:
        return ','.join(map(str, data))

    def use_db(self, db_name: str = "") -> None:
        self.execute_sql_query(f"USE {db_name};")

    def show_stored_data(self):
        for item in self._result_set:
            print(item)

    def show_exception_traceback(self, exc_tb: Exception) -> None:
        #print(f"Exception traceback:\n{exc_tb}\n")
        self._exception_history.append(exc_tb)
        print(f"Full exception traceback:\n{repr(exc_tb)}\n")
        return


if __name__ == "__main__":
    print("You are not supposed to run this program by itself.")
    sys.exit()
