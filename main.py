"""
Python program to access MySQL database.
"""

import argparse
import atexit
import sys

from tabulate import tabulate

from functional_modules import ConnectToMySQL


def str_to_bool(v: str) -> bool:
    true_opt = ("yes", "y", "true", "t", "1")
    false_opt = ("no", "n", "false", "f", "0")

    if v.lower() in true_opt:
        return True
    elif v.lower() in false_opt:
        return False
    else:
        raise argparse.ArgumentTypeError(
            f"Boolean value excepted, evaluated from following option set: True = {true_opt}, False = {false_opt}"
        )


parser = argparse.ArgumentParser(description="Python script to run SQL queries.")

parser.add_argument(
    "-d",
    "--dev",
    type=str_to_bool,
    default=False,
    help="Run in developer mode for detailed errors.",
)

args = parser.parse_args()


host = "localhost"
user = "bulk-admin"
passwd = "BulkTornado-admin123"
database = "CBSE_DATABASE"
default_query = (
    "SELECT school_id as 'School ID', school_name as 'School Name' FROM schools_data;"
)
developer_mode: bool = args.dev


def show_error(e: Exception):
    if developer_mode:
        print("[DEV MODE] Showing full exception trace:\n")
        print(repr(e))
    else:
        print(e)


try:
    db_object = ConnectToMySQL(host, user, passwd)
except Exception as error:
    print("Database connection failed. Refer to following error report for more:\n")

    show_error(error)

    print("\nTerminating script early.")
    sys.exit()


def display_menu():
    print(f"{'| CBSE Database |':=^80}\n")


@atexit.register
def display_exit():
    print(f"{'|      EXIT     |':=^80}")


@atexit.register
def close_database_connection():
    if "db_object" in globals() and db_object.check_connection():
        db_object.close_connection()


def get_sql_query() -> str:
    multi_line_sql_query = []
    line_count = 1

    print("Enter SQL query(end final line with ';' to complete the query):\n")
    while True:
        single_line_query = input(f"{line_count}. ").strip()

        # Skip adding to list if user presses ENTER key
        if single_line_query == "":
            print("Refrain from pressing ENTER key without writing a query.")
            continue

        multi_line_sql_query.append(single_line_query)
        line_count += 1

        if single_line_query.endswith(";"):
            break

    final_query = " ".join(multi_line_sql_query)

    if final_query == ";":
        print(f"\nNo query specified. Using the default query:\n{default_query}\n")
        return default_query

    print(f"\nFinal query: {final_query}\n")
    return final_query


def main() -> None:

    sql_query = get_sql_query()

    try:
        if developer_mode:
            print(f"[DEV MODE] Executing SQL Query:\n{sql_query}\n")
        db_object.execute_sql_query(sql_query)
    # '_mysql' refers to _mysql.connector
    # _mysql.errors.ProgrammingError
    except Exception as error:
        show_error(error)
        return


    data = db_object.fetch_data()

    if data[0] is None:
        print("Query executed successfully (no result set)")

        db_object.commit_to_database()

        return
    # DEBUG: DO NOT REMOVE
    # print(type(data))
    # print(data)
    # print(repr(data))

    # Fetch column names from cursor
    columns = [desc[0] for desc in data[0]]  #type: ignore

    # Pretty print results in a table format
    # OPTS : "simple", "grid"
    print(tabulate(data[1], headers=columns, tablefmt="simple"))

    print(f"\nRows retrieved: {data[-1]}")


if __name__ == "__main__":
    display_menu()

    main()
