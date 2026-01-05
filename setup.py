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


def random_dates_for_year(year: int, count: int) -> list[datetime.date]:
    start = datetime.date(year, 1, 1)
    end = datetime.date(year, 12, 31)
    days = (end - start).days + 1

    result: list[datetime.date] = [
        start + datetime.timedelta(days=random.randrange(days))
        for _ in range(count)
    ]
    result.sort()

    return result


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


def filter_course_by_grade(course: list, grade: int) -> list:
    return list(
        filter(
            lambda x: x[-1] == grade,
            course
        )
    )


def pick_courses(grade: int):
    main = random.sample(courses[grade]["main"], 5)
    additional = random.sample(courses[grade]["additional"], 2)

    return main, additional


def generate_marks(course):
    course_number, course_name, th_max, pr_max, ia_max, grade = course

    th = random.randint(0, th_max)
    pr = random.randint(0, pr_max)
    ia = random.randint(0, ia_max)

    return th, pr, ia


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


courses = {
    10: {
        "main": filter_course_by_grade(MAIN_COURSES, 10),
        "additional": filter_course_by_grade(ADDITIONAL_COURSES, 10)
    },
    12: {
        "main": filter_course_by_grade(MAIN_COURSES, 12),
        "additional": filter_course_by_grade(ADDITIONAL_COURSES, 12)
    }
}


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


# Generating required number of affiliation numbers for students
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


EXAM_ROLL_NUMBERS = random.sample(range(1_000_000, 9_999_999), STUDENT_COUNT)
EXAM_ROLL_NUMBERS.sort()
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
GRADES = [10] * GRADE_10_STUDENT_COUNT + [12] * GRADE_12_STUDENT_COUNT
MOTHER_NAMES = [fake.name_female() for _ in range(STUDENT_COUNT)]
GUARDIAN_NAMES = [fake.name_male() for _ in range(STUDENT_COUNT)]
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
        MOTHER_NAMES,
        GUARDIAN_NAMES,
        AADHAR_NOS,
        APAAR_ID,
        CATEGORY_OF_PWD,
        ADMIT_CARD_IDS
    )
)


STUDENTS = list(
    # [(roll number, grade), ...]
    map(
        lambda x: (x[0], x[6]),
        REGISTERED_STUDENTS
    )
)


EXAM_RESULTS = []

for roll_no, grade in STUDENTS:
    main_courses, add_courses = pick_courses(grade)

    for course in main_courses:
        th, pr, ia = generate_marks(course)
        EXAM_RESULTS.append(
            (roll_no, course[0], th, pr, ia)
        )

    for course in add_courses:
        th, pr, ia = generate_marks(course)
        EXAM_RESULTS.append(
            (roll_no, course[0], th, pr, ia)
        )


STUDENT_BATCH = 5000
RESULT_BATCH = 2000


with ConnectToMySQL(
        host=HOST, user=USER, passwd =PASSWD
) as conn_ob:
    for line in QUERY.split(";"):
        stmt = line.strip()
        if stmt:
            conn_ob.execute_sql_query(stmt)
    print("\nDatabase has been created.")

    conn_ob.insert_data("INSERT INTO COURSES VALUES (%s, %s, %s, %s, %s, %s);", (MAIN_COURSES + ADDITIONAL_COURSES))
    conn_ob.commit_to_database()
    print("\nCourses has been added.")

    conn_ob.insert_data("INSERT INTO AFFILIATED_SCHOOLS VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", AFFILIATED_SCHOOLS)
    conn_ob.commit_to_database()
    print("\nAffiliated schools has been added.")

    for i in range(0, STUDENT_COUNT, STUDENT_BATCH):
        chunk = REGISTERED_STUDENTS[i:i+STUDENT_BATCH]
        conn_ob.insert_data("INSERT INTO REGISTERED_STUDENTS VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", chunk)
        conn_ob.commit_to_database(silent=True)
    print("\nRegistered students added.")

    for i in range(0, len(EXAM_RESULTS), RESULT_BATCH):
        chunk = EXAM_RESULTS[i:i+RESULT_BATCH]
        conn_ob.insert_data("INSERT INTO EXAM_RESULTS VALUES (%s,%s,%s,%s,%s)", chunk)
        conn_ob.commit_to_database(silent=True)
    print("\nExam results added.")


CONFIG["setup_completed"] = True
with open(PATH_TO_CONFIG, "w") as f:
    json.dump(CONFIG, f, indent=4)


print("Set up has been completed. Now you can run main.py to start the program.")

end_time = perf_counter()
print(f"Total time taken: {end_time - start_time:.3f}s")
