import datetime
import json
import pickle
import sys
import string
import random
from pathlib import Path
from time import perf_counter

from functional_modules import ConnectToMySQL

from faker import Faker


start_time = perf_counter()


PATH_TO_AFFILIATED_SCHOOLS_DATA     = Path() / 'data'           / 'affiliated_schools.dat'
PATH_TO_COURSES_DATA                = Path() / 'data'           / 'courses.dat'
PATH_TO_CONFIG                      = Path() / 'config.json'
PATH_TO_DB_QUERY                    = Path() / 'sql_scripts'    / 'database_query.sql'


fake = Faker("en_IN")
STUDENT_COUNT: int = 500_000
GRADE_10_STUDENT_COUNT: int = int(STUDENT_COUNT * 0.4)
GRADE_12_STUDENT_COUNT: int = STUDENT_COUNT - GRADE_10_STUDENT_COUNT


def random_dates_for_year(year: int, count: int):
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    days = (end - start).days + 1

    return [
        start + datetime.timedelta(days=random.randrange(days))
        for _ in range(count)
    ]


def generate_unique_numbers(digits: int, count: int):
    start = 0
    end = 10**digits - 1
    return random.sample(range(start, end + 1), count)


def generate_unique_admit_card_ids(count: int):
    letters = string.ascii_uppercase
    prefixes = [a + b for a in letters for b in letters]

    result = set()

    while len(result) < count:
        prefix = random.choice(prefixes)
        number = random.randint(100_000, 999_999)
        result.add(f"{prefix}{number:06d}")

    return list(result)


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


SECONDARY_SCHOOLS_AFFILIATION_NUMBERS = [
    row[0] for row in
    filter(
        lambda x: x[-5].strip() == "Secondary Level",
        AFFILIATED_SCHOOLS
    )
]
SENIOR_SECONDARY_SCHOOLS_AFFILIATION_NUMBERS = [
    row[0] for row in
    filter(
        lambda x: x[-5].strip() == "Senior Secondary Level",
        AFFILIATED_SCHOOLS
    )
]


GRADE_10_SCHOOL_AFFILIATION_NOS = random.choices(
    population=SECONDARY_SCHOOLS_AFFILIATION_NUMBERS,
    k=GRADE_10_STUDENT_COUNT
)
GRADE_12_SCHOOL_AFFILIATION_NOS = random.choices(
    population=SENIOR_SECONDARY_SCHOOLS_AFFILIATION_NUMBERS,
    k=GRADE_12_STUDENT_COUNT
)
GRADE_10_DATE_OF_BIRTHS = random_dates_for_year(CURRENT_YEAR - 16, GRADE_10_STUDENT_COUNT)
GRADE_12_DATE_OF_BIRTHS = random_dates_for_year(CURRENT_YEAR - 18, GRADE_12_STUDENT_COUNT)
GRADE_10_DATE_OF_BIRTHS.sort()
GRADE_12_DATE_OF_BIRTHS.sort()


EXAM_ROLL_NUMBERS = list(range(1_000_000, 1_000_000 + STUDENT_COUNT))
AFFILIATION_NUMBERS = GRADE_10_SCHOOL_AFFILIATION_NOS + GRADE_12_SCHOOL_AFFILIATION_NOS
EXAM_CENTRE_NOS = random.choices(
    population=AFFILIATION_NUMBERS,
    k=STUDENT_COUNT
)
CANDIDATE_NAMES = [fake.name() for _ in range(STUDENT_COUNT)]
DATE_OF_BIRTHS = GRADE_10_DATE_OF_BIRTHS + GRADE_12_DATE_OF_BIRTHS
GENDERS = random.choices(
    population=['M', 'F', 'O'],
    weights=[0.52, 0.47, 0.01],
    k=STUDENT_COUNT
)
GRADES = random.choices(
    population=[10, 12],
    weights=[0.45, 0.55],
    k=STUDENT_COUNT
)
AADHAR_NOS = generate_unique_numbers(12, STUDENT_COUNT)
APAAR_ID = generate_unique_numbers(12, STUDENT_COUNT)
CATEGORY_OF_PWD = random.choices(
    population=['Y', 'N'],
    weights=[0.01, 0.99],
    k=STUDENT_COUNT
)
ADMIT_CARD_IDS = generate_unique_admit_card_ids(STUDENT_COUNT)


REGISTERED_STUDENTS = list(
    zip(
        EXAM_ROLL_NUMBERS,
        AFFILIATION_NUMBERS,
        EXAM_CENTRE_NOS,
        CANDIDATE_NAMES,
        DATE_OF_BIRTHS,
        GENDERS,
        GRADES,
        AADHAR_NOS,
        APAAR_ID,
        CATEGORY_OF_PWD,
        ADMIT_CARD_IDS
    )
)


with ConnectToMySQL(
        host=HOST, user=USER, passwd =PASSWD
) as conn_ob:
    for line in QUERY.split(";"):
        stmt = line.strip()
        if stmt:
            ...#conn_ob.execute_sql_query(stmt)
    print("Database has been created.")
    #conn_ob.execute_sql_query(f"INSERT INTO COURSES VALUES {conn_ob.parameterized_data(MAIN_COURSES + ADDITIONAL_COURSES)};")
    conn_ob.commit_to_database()
    print("Courses has been added.")
    #conn_ob.execute_sql_query(f"INSERT INTO AFFILIATED_SCHOOLS VALUES {conn_ob.parameterized_data(AFFILIATED_SCHOOLS)};")
    conn_ob.commit_to_database()
    print("Affiliated schools has been added.")

    #for student_record in REGISTERED_STUDENTS: ...


#CONFIG["setup_completed"] = True
#with open(PATH_TO_CONFIG, "w") as f:
    #json.dump(CONFIG, f, indent=4)


print("Set up has been completed. Now you can run main.py to start the program.")

end_time = perf_counter()
print(f"Total time taken: {end_time - start_time:.3f}s")
