import datetime
import json
import pickle
import sys
from pathlib import Path

from functional_modules import ConnectToMySQL


PATH_TO_AFFILIATED_SCHOOLS_DATA     = Path() / 'data'           / 'affiliated_schools.dat'
PATH_TO_COURSES_DATA                = Path() / 'data'           / 'courses.dat'
PATH_TO_CONFIG                      = Path() / 'config.json'
PATH_TO_DB_QUERY                    = Path() / 'sql_scripts'    / 'database_query.sql'


if not PATH_TO_AFFILIATED_SCHOOLS_DATA.exists():
    print(f"Affiliated schools data doesn't exists at: {PATH_TO_AFFILIATED_SCHOOLS_DATA.absolute()}")
    print("Either download the affiliated_schools.dat from the GitHub repo at: ...")
    print("or use the affiliated_schools.dat in the backup directory.")
    print("Till then, setup.py cannot complete execution. Terminating early...")
    sys.exit()


if not PATH_TO_COURSES_DATA.exists():
    print(f"Courses data file doesn't exists at: {PATH_TO_COURSES_DATA.absolute()}")
    print("Either download the courses.dat from the GitHub repo at: ...")
    print("or run scripts/parse_courses.py according to the instructions given in the manual to generate the file.")
    print("Till then, setup.py cannot complete execution. Terminating early...")
    sys.exit()


if not PATH_TO_CONFIG.exists():
    print(f"Config file doesn't exists at the following file path: {PATH_TO_CONFIG.absolute()}")
    print("Run the set_configuration.py file as given in the instruction manual to set up the config file.")
    print("Till then, setup.py cannot complete execution. Terminating early...")
    sys.exit()


if not PATH_TO_DB_QUERY.exists():
    print(f"Database query file doesn't exists at: {PATH_TO_DB_QUERY.absolute()}")
    print("Download the SQL file from the GitHub repo at: ...")
    print("Till then, setup.py cannot complete execution. Terminating early...")
    sys.exit()


with (
    open(PATH_TO_AFFILIATED_SCHOOLS_DATA, "rb") as f1,
    open(PATH_TO_COURSES_DATA, "rb") as f2,
    open(PATH_TO_CONFIG, 'r') as f3,
    open(PATH_TO_DB_QUERY, 'r') as f4
):
    AFFILIATED_SCHOOLS      = pickle.load(f1)
    COURSES_DATA            = pickle.load(f2)
    CONFIG                  = json.load(f3)
    QUERY                   = f4.read()


if CONFIG.get("setup_completed"):
    print("Set-up has already been completed before.")
    print("If that is not the case, please run set_configuration and follow the instructions carefully.")
    sys.exit()


HOST    = CONFIG.get("host")
USER    = CONFIG.get("user")
PASSWD  = CONFIG.get("passwd")

CURRENT_YEAR: int   = datetime.date.today().year
QUERY               = QUERY.replace("XXXX", str(CURRENT_YEAR))

MAIN_COURSES            = list(
    map(
        lambda x: (*x[:-2], x[-1]),
        filter(
            lambda x: x[-2]=='MAIN',
            COURSES_DATA
        )
    )
)
ADDITIONAL_COURSES      = list(
    map(
        lambda x: (*x[:-2], x[-1]),
        filter(
            lambda x: x[-2]=='ADDITIONAL',
            COURSES_DATA
        )
    )
)


with ConnectToMySQL(
        host=HOST, user=USER, passwd =PASSWD
) as conn_ob:
    conn_ob.execute_sql_query(QUERY)
    conn_ob.execute_sql_query(f"INSERT INTO COURSES VALUES {conn_ob.parameterized_data(COURSES_DATA)};")
    conn_ob.execute_sql_query(f"INSERT INTO AFFILIATED_SCHOOLS VALUES {conn_ob.parameterized_data(AFFILIATED_SCHOOLS)};")

    ...#(conn_ob.parameterized_data(MAIN_COURSES))


#CONFIG["setup_completed"] = True
#with open(PATH_TO_CONFIG, "w") as f:
    #json.dump(CONFIG, f, indent=4)


print("Set up has been completed. Now you can run main.py to start the program.")

