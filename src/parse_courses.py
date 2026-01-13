import pickle
import sys
from pathlib import Path

import tabulate

PATH_TO_COURSES_DATA            = Path()    / "data"            / "courses.dat"
PATH_TO_COURSES_BACKUP_DATA     = Path()    / "backup"          / "courses.dat"
PATH_TO_TABULAR_DATA            = Path()    / "data"            / "tabular_data"    / "courses.txt"

# Hard-coded data in case file is missing. Will not be used much(probably)...
# Expected type 'list[tuple[int, str, int, int, int, int]]'
DEFAULT_COURSES: list[tuple[int, str, int, int, int, str, int]] = [
    # Class 10
        (2, 'Hindi Course-A', 80, 0, 20, 'MAIN', 10),
        (3, 'Urdu Course-A', 80, 0, 20, 'MAIN', 10),
        (4, 'Urdu Course-B', 80, 0, 20, 'MAIN', 10),
        (5, 'Bengali', 80, 0, 20, 'MAIN', 10),
        (41, 'Mathematics Standard', 80, 0, 20, 'MAIN', 10),
        (49, 'Painting', 30, 50, 20, 'ADDITIONAL', 10),
        (64, 'Home Science', 70, 0, 30, 'ADDITIONAL', 10),
        (85, 'Hindi Course-B', 80, 0, 20, 'MAIN', 10),
        (86, 'Science', 80, 0, 20, 'MAIN', 10),
        (87, 'Social Science', 80, 0, 20, 'MAIN', 10),
        (101, 'English Communicative', 80, 0, 20, 'MAIN', 10),
        (119, 'Sanskrit Communicative', 80, 0, 20, 'MAIN', 10),
        (122, 'Sanskrit', 80, 0, 20, 'MAIN', 10),
        (165, 'Computer Applications', 50, 0, 50, 'ADDITIONAL', 10),
        (184, 'English Lang & Literature', 80, 0, 20, 'MAIN', 10),
        (241, 'Mathematics-Basic', 80, 0, 20, 'MAIN', 10),
        (401, 'Retail', 50, 50, 0, 'ADDITIONAL', 10),
        (402, 'Information Technology', 50, 50, 0, 'ADDITIONAL', 10),
        (415, 'Multi Media', 50, 50, 0, 'ADDITIONAL', 10),
        (417, 'Artificial Intelligence', 50, 50, 0, 'ADDITIONAL', 10),
        (418, 'Physical Activity Trainer', 50, 50, 0, 'ADDITIONAL', 10),
        (419, 'Data Science', 50, 50, 0, 'ADDITIONAL', 10),
    # Class 12
        (1, 'English Elective', 80, 0, 20, 'MAIN', 12),
        (2, 'Hindi Elective', 80, 0, 20, 'MAIN', 12),
        (3, 'Urdu Elective', 80, 0, 20, 'MAIN', 12),
        (22, 'Sanskrit Elective', 80, 0, 20, 'MAIN', 12),
        (27, 'History', 80, 0, 20, 'MAIN', 12),
        (28, 'Political Science', 80, 0, 20, 'MAIN', 12),
        (29, 'Geography', 70, 30, 0, 'MAIN', 12),
        (30, 'Economics', 80, 20, 0, 'MAIN', 12),
        (41, 'Mathematics', 80, 0, 20, 'MAIN', 12),
        (42, 'Physics', 70, 30, 0, 'MAIN', 12),
        (43, 'Chemistry', 70, 30, 0, 'MAIN', 12),
        (44, 'Biology', 70, 30, 0, 'MAIN', 12),
        (48, 'Physical Education', 70, 30, 0, 'MAIN', 12),
        (65, 'Informatics Practices', 70, 30, 0, 'MAIN', 12),
        (83, 'Computer Science', 70, 30, 0, 'MAIN', 12),
        (105, 'Bengali', 80, 0, 20, 'MAIN', 12),
        (301, 'English Core', 80, 0, 20, 'MAIN', 12),
        (302, 'Hindi Core', 80, 0, 20, 'MAIN', 12),
        (303, 'Urdu Core', 80, 0, 20, 'MAIN', 12),
        (322, 'Sanskrit Core', 80, 0, 20, 'MAIN', 12),
        (801, 'Retail', 60, 40, 0, 'ADDITIONAL', 12),
        (802, 'Information Technology', 60, 40, 0, 'ADDITIONAL', 12),
        (813, 'Health Care', 60, 40, 0, 'ADDITIONAL', 12),
        (830, 'Design', 50, 50, 0, 'ADDITIONAL', 12),
        (841, 'Yoga', 50, 50, 0, 'ADDITIONAL', 12),
        (843, 'Artificial Intelligence', 50, 50, 0, 'ADDITIONAL', 12),
        (845, 'Physical Activity Trainer', 50, 50, 0, 'ADDITIONAL', 12)
]
COLUMNS = [
    "code",
    "name",
    "theory",
    "practical",
    "internal",
    "type",
    "grade",
]
TYPES = ["MAIN", "ADDITIONAL"]

if not PATH_TO_COURSES_DATA.exists():
    print("File is missing. Creating right now.")
    with open(PATH_TO_COURSES_DATA, "wb") as f:
        pickle.dump(DEFAULT_COURSES, f)
    print("File created, default data dumped.")
else:
    try:
        with open(PATH_TO_COURSES_DATA, "rb") as f:
            # type expected: list[tuple[int, str, int, int, int, int]]
            COURSES = pickle.load(f)
    except EOFError:
        print("Empty file, initiating an empty stack COURSES.")
        COURSES = []
    except Exception as exc:
        print(f"Undocumented exception occurred: {exc}")
        print("Terminating early.")
        sys.exit()


def validate_course_code() -> int:
    while True:
        try:
            course_code: int = int(input("\nCourse code: "))

            if course_code <= 0:
                print("Enter an integer greater than 0.")
                continue

            break

        except ValueError as exc:
            print(exc)
        except Exception as exc:
            print(f"(1) Undocumented exception occurred: {exc}")
            print("Terminating early.")
            sys.exit()

    return course_code


def sanitize_course_name() -> str:
    # Sanitize input: MathEmatics   standard -> Mathematics Standard
    return " ".join(
        input("Course name: ").strip().title().split()
    )


def validate_marks() -> list[int]:
    while True:
        try:
            _str_input:   list[str] = input("<Theory marks> <Practical marks> <Internal marks>: ").strip().split()
            _mapped_to_int:     map = map(int, _str_input)
            marks:        list[int] = list(_mapped_to_int)

            if not len(marks) == 3:
                print(f"Exactly 3 values required, got {len(marks)} instead.")
                print(f"Values provided: {marks}")
                continue

            if not sum(marks) == 100:
                print(f"Sum of marks is not equal to 100: got {sum(marks)} instead.")
                continue

            break

        except ValueError as exc:
            print(exc)
        except Exception as exc:
            print(f"(2) Undocumented exception occurred: {exc}")
            print("Terminating early.")
            sys.exit()

    return marks


def validate_grade() -> int:
    while True:
        try:
            grade: int = int(input("Grade (10 or 12): "))

            if grade not in (10, 12):
                print("Validate grades are: 10, 12")
                continue

            break

        except ValueError as exc:
            print(exc)
        except Exception as exc:
            print(f"(3) Undocumented exception occurred: {exc}")
            print("Terminating early.")
            sys.exit()

    return grade


def choose_type() -> str:
    for index, value in enumerate(TYPES):
        print(f"{index}. {value}")
    while True:
        try:
            choice = int(input("Choice (0 or 1): "))
            subject_type = TYPES[choice]
            break
        except ValueError as exc:
            print(exc)
        except IndexError as exc:
            print(exc)
        except Exception as exc:
            print(f"(4) Undocumented exception occurred: {exc}")
            print("Terminating early.")
            sys.exit()

    return subject_type


def get_input() -> tuple[int, str, int, int, int, str, int]:

    while True:
        grade           : int   = validate_grade()
        course_code     : int   = validate_course_code()

        record_exists   : bool  = any(
            record[0] == course_code
            for record in filter(
                lambda x: x[-1] == grade,
                COURSES
            )
        )

        if record_exists:
            print(f"Course record with course code: {course_code} already exists.")
            continue

        break

    course_name         : str       = sanitize_course_name()
    marks               : list[int] = validate_marks()
    subject_type        : str       = choose_type()

    return course_code, course_name, marks[0], marks[1], marks[-1], subject_type, grade


def append_course_record():
    while True:
        course_record = get_input()
        COURSES.append(course_record)
        if input("\nType 'stop' to finish: ").strip().lower() == "stop":
            break

    COURSES.sort(key=lambda x: (x[-1], x[0]))
    with (
        open(PATH_TO_COURSES_DATA, "wb") as f1,
        open(PATH_TO_COURSES_BACKUP_DATA, "wb") as f2
    ):
        pickle.dump(COURSES, f1)
        pickle.dump(COURSES, f2)
    print("Records updated on disk.")
    return


# NOT IMPLEMENTED, DO NOT USE
def modify_course_record():
    raise NotImplementedError
    if not COURSES:
        print("No record. Cannot perform operation.")
        return

    course_code: int = validate_course_code()

    for index, record in enumerate(COURSES):
        if record[0] == course_code:
            print("Record found. Enter new details for this record.\n")
            new_record = get_input() #TODO: Serious issue, remember bro
            COURSES[index] = new_record
            break
    else:
        print("No record found.")
        return

    COURSES.sort(key=lambda x: (x[-1], x[0]))
    with (
        open(PATH_TO_COURSES_DATA, "wb") as f1,
        open(PATH_TO_COURSES_BACKUP_DATA, "wb") as f2
    ):
        pickle.dump(COURSES, f1)
        pickle.dump(COURSES, f2)
    print("Records updated on disk.")
    return


def remove_course_record():
    if not COURSES:
        print("No records in stack COURSES. Cannot perform operation.")
        return
    affiliation_no: int = validate_course_code()

    for index, course in enumerate(COURSES):
        if course[0] == affiliation_no:
            break
    else:
        print("Course not found.")
        return

    print(f"Course found.\n\t{course}\n")
    if input("Confirm removing the course (y/n): ").strip().lower() == "y":
        del COURSES[index]
        print("Record deleted.")
        with (
                open(PATH_TO_COURSES_DATA, "wb") as f1,
                open(PATH_TO_COURSES_BACKUP_DATA, "wb") as f2
        ):
            pickle.dump(COURSES, f1)
            pickle.dump(COURSES, f2)
        print("Data has been updated on disk.")
        return

    print("Cancelled removing operation...")
    return


def tabular_record() -> None:
    if not COURSES:
        print("No record. Cannot make tabular data.")
        return

    print(f"Row count: {len(COURSES)}")
    with open(PATH_TO_TABULAR_DATA, "w") as f:
        f.write(tabulate.tabulate(COURSES, headers=COLUMNS, tablefmt="pipe"))
    print(f"Data exported to: {PATH_TO_TABULAR_DATA.absolute()}")
    return


def list_raw_data() -> None:
    if not COURSES:
        print("No record.")
        return

    print(f"[\n\t{',\n\t'.join(map(str, COURSES))}\n]")
    print(f"Record count: {len(COURSES)}")
    return


def main():

    mode = input("a=append, ls=list, dd='dump default data': ").strip().lower()

    match mode:
        case "a":
            append_course_record()
        case "ls":
            tabular_record()

        case "dd":
            with open(PATH_TO_COURSES_DATA, "wb") as f:
                pickle.dump(DEFAULT_COURSES, f)
                print("Default data dumped")

        ### DEBUG MODE: NOT FOR END-USER
        case "rls": # raw-listing
            list_raw_data()
        ###

        case _:
            print("No valid mode provided. Terminating.")
    return


if __name__ == "__main__":
    main()
