import pickle
from pathlib import Path

import tabulate

# Hard-coded data in case file is missing. Will not be used much(probably)...
#Expected type 'list[tuple[int, str, int, int, int, int]]'
_DATA: list[tuple[int, str, int, int, int, tuple[int, int], int] | tuple[int, str, int, int, int, tuple[()], int]] = [
    # Grade 10
    (2, "Hindi Course-A", 80, 0, 20, (2, 85), 10),
    (3, "Urdu Course-A", 80, 0, 20, (3, 4), 10),
    (4, "Urdu Course-B", 80, 0, 20, (3, 4), 10),
    (5, "Bengali", 80, 0, 20, (), 10),
    (41, "Mathematics Standard", 80, 0, 20, (41, 241), 10),
    (49, "Painting", 30, 50, 20, (), 10),
    (85, "Hindi Course-B", 80, 0, 20, (2, 85), 10),
    (86, "Science", 80, 0, 20, (), 10),
    (87, "Social Science", 80, 0, 20, (), 10),
    (101, "English Communicative", 80, 0, 20, (101, 184), 10),
    (119, "Sanskrit Communicative", 80, 0, 20, (119, 122), 10),
    (122, "Sanskrit", 80, 0, 20, (119, 122), 10),
    (184, "English Lang & Lit.", 80, 0, 20, (101, 184), 10),
    (241, "Mathematics-Basic", 80, 0, 20, (41, 241), 10),
    (402, "Information Technology", 50, 50, 0, (), 10),
    (417, "Artificial Intelligence", 50, 50, 0, (), 10),
    (418, "Physical Activity Trainer", 50, 50, 0, (), 10),
    # Grade 12
    (1, "English Elective", 80, 0, 20, (1, 301), 12),
    (2, "Hindi Elective", 80, 0, 20, (2, 302), 12),
    (3, "Urdu Elective", 80, 0, 20, (3, 303), 12),
    (22, "Sanskrit Elective", 80, 0, 20, (22, 322), 12),
    (27, "History", 80, 0, 20, (), 12),
    (28, "Political Science", 80, 0, 20, (), 12),
    (29, "Geography", 70, 30, 0, (), 12),
    (30, "Economics", 80, 20, 0, (), 12),
    (41, "Mathematics", 80, 0, 20, (), 12),
    (42, "Physics", 70, 30, 0, (), 12),
    (43, "Chemistry", 70, 30, 0, (), 12),
    (44, "Biology", 70, 30, 0, (), 12),
    (48, "Physical Education", 70, 30, 0, (), 12),
    (65, "Informatics Practices", 70, 30, 0, (65, 83), 12),
    (83, "Computer Science", 70, 30, 0, (65, 83), 12),
    (105, "Bengali", 80, 0, 20, (), 12),
    (301, "English Core", 80, 0, 20, (1, 301), 12),
    (302, "Hindi Core", 80, 0, 20, (2, 302), 12),
    (303, "Urdu Core", 80, 0, 20, (3, 303), 12),
    (322, "Sanskrit Core", 80, 0, 20, (22, 322), 12),
    (802, "Information Technology", 60, 40, 0, (), 12),
    (843, "Artificial Intelligence", 50, 50, 0, (), 12),
    (845, "Physical Activity Trainer", 50, 50, 0, (), 12),
]
COLUMNS = [
    "code",
    "name",
    "theory",
    "practical",
    "IA",
    "constrained-to-which-subject-code",
    "grade",
]
PATH_TO_COURSES_DATA = Path() / "data" / "courses.dat"
print(PATH_TO_COURSES_DATA.absolute(), PATH_TO_COURSES_DATA.exists())

def get_input() -> tuple[int, str, int, int, int, int]:
    while True:
        try:
            _course_code = int(input("\nCourse code: ").strip())
            if _course_code <= 0:
                print("Enter a value greater than 0 for course code.")
                continue
            _course_name = " ".join(
                # In case someone accidentally puts: MathEmatics   standard -> Mathematics Standard
                input("Course name: ").strip().title().split()
            )
            _marks = list(
                map(
                    int,
                    input("<Theory marks> <Practical marks> <Internal marks>: ")
                    .strip()
                    .split(),
                )
            )
            if not len(_marks) == 3:
                print(
                    f"Exactly 3 values not provide, got {len(_marks)} values instead: {_marks}"
                )
                continue
            if not sum(_marks) == 100:
                print(f"Sum of marks is not exactly 100: got {sum(_marks)} instead.")
                continue
            _grade = int(input("GRADE(10 | 12): ").strip())
            # DEBUG
            # print(f"{(_course_code, _course_name, *_marks, _grade)}")
            return _course_code, _course_name, *_marks, _grade
        except ValueError as exc_value:
            print(f"Please enter a valid integer value: got {exc_value} instead.")
        except Exception as exc_value:
            print(f"Traceback to exception: {exc_value}")


def list_all_data() -> None:
    try:
        with open(PATH_TO_COURSES_DATA, "rb") as f:
            data = pickle.load(f)
    except EOFError:
        print(
            "Looks like file has just been created and there is no data present in it. Use append mode to first data, then you can use list mode to see all the data."
        )
        return
    except Exception as error:
        print(f"Some new type of undocumented error occurred: {error}")
        return

    print(tabulate.tabulate(data, headers=COLUMNS, tablefmt="simple"))
    return


def list_raw_data() -> None:
    try:
        with open(PATH_TO_COURSES_DATA, "rb") as f:
            data = list(pickle.load(f))
    except EOFError:
        print(
            "Looks like file has just been created and there is no data present in it. Use append mode to first data, then you can use list mode to see all the data."
        )
        return
    except Exception as error:
        print(f"Some new type of undocumented error occurred: {error}")
        return
    print(f"[\n\t{'\n\t'.join(map(str, data))}\n]")
    return


def append_data() -> None:
    try:
        with open(PATH_TO_COURSES_DATA, "rb") as f:
            data: list = pickle.load(f)
    except EOFError:
        data = []
    except Exception as error:
        print(f"Some new type of undocumented error occurred: {error}")
        print("Terminating program.")
        return
    while True:
        _ = get_input()
        data.append(_)
        if input("\nEnter 'stop' to stop adding more data: ").strip().lower() == "stop":
            break
    data.sort(key=lambda x: (x[-1], x[0]))
    with open(PATH_TO_COURSES_DATA, "wb") as f:
        pickle.dump(data, f)
    return


### SHOULD NOT TO BE USED, has not been completed
def modify_data() -> None:
    try:
        with open(PATH_TO_COURSES_DATA, "rb") as f:
            data = list(pickle.load(f))
    except EOFError:
        print("Empty data file. Dumping default data.")
        with open(PATH_TO_COURSES_DATA, "wb") as f:
            pickle.dump(_DATA, f)
        print("Default data dumped.")
        data = _DATA
    except Exception as error:
        print(f"Some new type of undocumented error occurred: {error}")
        print("Terminating program.")
        return
    print("Listing all data for reference:")
    list_all_data()
    subject_code = int(input("Enter subject code: "))
    for subject in data:
        if subject[0] == subject_code:
            print("Subject data found.")
            print(tabulate.tabulate(subject, headers=COLUMNS, tablefmt = "simple"))
    else:
        print("No subject data found.")
    raise NotImplementedError
### SHOULD NOT TO BE USED AT ALL

def main():
    if not PATH_TO_COURSES_DATA.exists():
        print(
            "File not found. Creating file first and dumping default data. After that, you can re-run the program to append data or all list data."
        )
        with open(PATH_TO_COURSES_DATA, "wb") as f:
            pickle.dump(_DATA, f)
        print("File created, default data dumped. Run program again to append data, else leave it.")
        return

    mode = input("Enter 'a' to append data or 'ls' to list all data: ").strip().lower()

    match mode:
        case "ls":
            list_all_data()
            return
        case "a":
            append_data()
            return

        ### DEBUG MODE NOT FOR END-USER
        case "rls": # raw-listing
            list_raw_data()
            return
        case "ra": # raw-append
            with open(PATH_TO_COURSES_DATA, "wb") as f:
                pickle.dump(_DATA, f)
            return
        ###

        case _:
            print("No valid mode provided. Terminating.")
    return


if __name__ == "__main__":
    main()
