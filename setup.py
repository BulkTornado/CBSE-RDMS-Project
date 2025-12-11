import json
import pickle
import sys
from pathlib import Path

from functional_modules import ConnectToMySQL


PATH_TO_AFFILIATED_SCHOOLS_DATA = Path() / 'data' / 'affiliated_schools.dat'
PATH_TO_COURSES_DATA = Path() / 'data' / 'courses.dat'
PATH_TO_CONFIG = Path() / 'config.json'
PATH_TO_DB_QUERY = Path() / 'sql_scripts' / 'database_query.sql'


if not PATH_TO_AFFILIATED_SCHOOLS_DATA.exists():
    print(f"Affiliated schools data doesn't exists at: {PATH_TO_AFFILIATED_SCHOOLS_DATA.absolute()}")
    print("Either download the affiliated_schools.dat from the GitHub repo at: ...")
    print("or use the affiliated_schools.dat in the backup directory.")
    print("Till then, script cannot finish running.")
    sys.exit()

if not PATH_TO_COURSES_DATA.exists():
    print(f"Courses data file doesn't exists at: {PATH_TO_COURSES_DATA.absolute()}")
    print("Either download the courses.dat from the GitHub repo at: ...")
    print("or run sql_scripts/get_courses.py according to the instructions given in the manual to generate the file.")
    print("Till then, script cannot finish running.")
    sys.exit()

if not PATH_TO_CONFIG.exists():
    print(f"Config file doesn't exists at the following file path: {PATH_TO_CONFIG.absolute()}")
    print("Run the set_configuration.py file as given in the instruction manual to set up the config file.")
    print("Till then, setup.py cannot complete execution. Terminating early...")
    sys.exit()

if not PATH_TO_DB_QUERY.exists():
    print(f"Database query file doesn't exists at: {PATH_TO_DB_QUERY.absolute()}")
    print("Download the SQL file from the GitHub repo at: ...")
    print("Till then, script cannot finish running.")
    sys.exit()


with open(PATH_TO_CONFIG, 'r') as f:
    CONFIG = json.load(f)
DATABASES = CONFIG.get("databases")

with open(PATH_TO_DB_QUERY, 'r') as f:
    QUERY = f.read()

with open(PATH_TO_COURSES_DATA, "rb") as f:
    COURSES_DATA = pickle.load(f)

with ConnectToMySQL(
        host=CONFIG.get("host"), user=CONFIG.get("user"), passwd = CONFIG.get("passwd")
) as conn_ob:
    for database in DATABASES:
        QUERY.replace("CBSE_DATABASE", database)

