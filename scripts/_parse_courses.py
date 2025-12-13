import json
import pickle
from pathlib import Path

from functional_modules import ConnectToMySQL

PATH_TO_COURSES_DATA = Path() / "data" / "courses.dat"

with open("./config.json", "r") as _:
    configs = json.load(_)

HOST, USER, PASSWD = configs.get("host"), configs.get("user"), configs.get("passwd")


def f1():
    with ConnectToMySQL(host=HOST, user=USER, passwd=PASSWD) as conn_ob:
        print("Connected:", conn_ob.check_connection())
        conn_ob.execute_sql_query("CREATE DATABASE temp1;")
        print(conn_ob.fetch_data())
        conn_ob.close_connection()


def main():
    if not PATH_TO_COURSES_DATA.exists():
        print(f"Required file at: {PATH_TO_COURSES_DATA.absolute()} does not exists.")
        print(
            "Please run the parse_courses.py file in sql_scripts directory to create and populate the file with data."
        )
        return

    with open(PATH_TO_COURSES_DATA, "rb") as f:
        DATA = pickle.load(f)

    CLASS_10 = list(filter(lambda x: x[-1] == 10, DATA))
    CLASS_12 = list(filter(lambda x: x[-1] == 12, DATA))
    print(CLASS_10)
    print(CLASS_12)


if __name__ == "__main__":
    main()
    # f1()
