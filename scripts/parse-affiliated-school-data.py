import datetime
import pickle
import sys
from pathlib import Path

import tabulate

PATH_TO_AFFILIATED_SCHOOL = Path() / "data" / "affiliated_schools.dat"
PATH_TO_AFFILIATED_SCHOOL_BACKUP = Path() / "backup" / "affiliated_schools.dat"
PATH_TO_TABULAR_DATA = Path() / "data" / "affiliated_schools.txt"
PATH_TO_TABULAR_DATA_BACKUP = Path() / "backup" / "affiliated_schools.txt"
if not PATH_TO_TABULAR_DATA.exists():
    PATH_TO_TABULAR_DATA.touch()
if not PATH_TO_TABULAR_DATA_BACKUP.exists():
    PATH_TO_TABULAR_DATA_BACKUP.touch()

INDIAN_STATES = ['ANDAMAN AND NICOBAR ISLANDS', 'ANDHRA PRADESH', 'ARUNACHAL PRADESH', 'ASSAM', 'BIHAR', 'CHHATTISGARH',
                 'GOA', 'GUJARAT', 'HARYANA', 'HIMACHAL PRADESH', 'JHARKHAND', 'KARNATAKA', 'KERALA', 'MADHYA PRADESH',
                 'MAHARASHTRA', 'MANIPUR', 'MEGHALAYA', 'MIZORAM', 'NAGALAND', 'ODISHA', 'PUNJAB', 'RAJASTHAN',
                 'SIKKIM', 'TAMIL NADU', 'TELANGANA', 'TRIPURA', 'UTTAR PRADESH', 'UTTARAKHAND', 'WEST BENGAL']
COLUMNS = ["affiliation_no", "name_of_institution", "state", "district", "postal_address", "pin_code", "website",
           "year_of_foundation", "date_of_first_opening_of_school", "head_of_institution", "status_of_the_school",
           "school_type", "affiliation_period_start", "affiliation_period_end", "remarks"]
STATUS_OF_SCHOOL = ["Middle Class", "Secondary Level", "Senior Secondary Level"]
SCHOOL_TYPE = ["KV", "GOVT", "JNV", "STSS", "INDEPENDENT"]
# JNV: Jawahar Navodyalaya Vidyalaya; STSS: smth from Sambhota Tibetan School

if not PATH_TO_AFFILIATED_SCHOOL.exists():
    print("File doesn't exists. Creating file and stack SCHOOLS.")
    PATH_TO_AFFILIATED_SCHOOL.touch()
    SCHOOLS = []
else:
    try:
        with open(PATH_TO_AFFILIATED_SCHOOL, "rb") as f:
            SCHOOLS = pickle.load(f)
    except EOFError:
        print("Empty file, initiating an empty stack SCHOOLS")
        SCHOOLS = []
    except Exception:
        print("(1) Undocumented exception occurred. Terminating script.")
        sys.exit()


def input_school_record(modifying_stack: bool = False):
    while True:
        try:
            affiliation_number = int(input("\nAffiliation Number: "))
            if not modifying_stack:
                record_exists = any(record[0] == affiliation_number for record in SCHOOLS)
                if record_exists:
                    print(f"Record with Affiliation Number: {affiliation_number} already exists.")
                    continue
            name_of_institution = " ".join(
                input("Name of Institution: ").strip().upper().split()
            )
            for index, value in enumerate(INDIAN_STATES, start=1):
                print(f"{index}. {value}")
            state = INDIAN_STATES[int(input("State code: ")) - 1]
            district = input("District: ").strip().upper()
            postal_address = " ".join(
                input("Postal Address: ").strip().upper().split()
            )
            pin_code = int(input("PIN Code: "))
            website = input("Website (if any): ").strip() or ""
            year_of_foundation = int(input("Year of Foundation: "))
            print("Date of First Opening of School (DD MM YEAR): ", end="")
            date_of_first_opening_of_school = datetime.date(
                *list(
                    map(
                        int,
                        input().strip().split()[::-1]
                    )
                )
            )
            head_of_institution = " ".join(
                input("Head of Institution: ").strip().upper().split()
            )
            for index, value in enumerate(STATUS_OF_SCHOOL, start=1):
                print(f"{index}. {value}")
            status_of_the_school = STATUS_OF_SCHOOL[int(input("Status of The School: ")) - 1]
            for index, value in enumerate(SCHOOL_TYPE, start=1):
                print(f"{index}. {value}")
            school_type = SCHOOL_TYPE[int(input("School Type: ")) - 1]
            print("Affiliation Period Start (DD MM YEAR): ", end="")
            affiliation_period_start = datetime.date(
                *list(
                    map(
                        int,
                        input().strip().split()[::-1]
                    )
                )
            )
            print("Affiliation Period End (DD MM YEAR): ", end="")
            affiliation_period_end = datetime.date(
                *list(
                    map(
                        int,
                        input().strip().split()[::-1]
                    )
                )
            )
            remarks = input("Remarks, if any: ") or ""

            return (affiliation_number, name_of_institution,
                    state, district, postal_address, pin_code,
                    website,
                    year_of_foundation, date_of_first_opening_of_school,
                    head_of_institution,
                    status_of_the_school, school_type,
                    affiliation_period_start, affiliation_period_end,
                    remarks)
        except ValueError as exc_value:
            print(f"Exception occurred: {exc_value}")
        except IndexError:
            print("Refer to the index goddammit.")
        except Exception as exc_value:
            print(f"Undocumented exception occurred: {exc_value}")


def append_school_record():
    while True:
        school_record = input_school_record()
        SCHOOLS.append(school_record)
        if input("\nType 'stop' to finish: ").strip().lower() == "stop":
            break
    SCHOOLS.sort(key=lambda x: x[0])
    with open(PATH_TO_AFFILIATED_SCHOOL, "wb") as f:
        pickle.dump(SCHOOLS, f)
    with open(PATH_TO_AFFILIATED_SCHOOL_BACKUP, "wb") as f:
        pickle.dump(SCHOOLS, f)

def modify_school_record():
    if not SCHOOLS:
        print("No records in stack SCHOOLS.")
        return

    try:
        affiliation_no = int(input("Affiliation Number: "))
    except ValueError:
        print("Enter a number goddammit!")
        return
    except Exception as exc_value:
        print(f"Undocumented exception occurred: {exc_value}")
        return

    for index, record in enumerate(SCHOOLS):
        if record[0] == affiliation_no:
            new_record = input_school_record(True)
            SCHOOLS[index] = new_record
            break
    else:
        print("Record not found.")
        return

    SCHOOLS.sort(key=lambda x: x[0])
    with open(PATH_TO_AFFILIATED_SCHOOL, "wb") as f:
        pickle.dump(SCHOOLS, f)
    with open(PATH_TO_AFFILIATED_SCHOOL_BACKUP, "wb") as f:
        pickle.dump(SCHOOLS, f)
    print("Records updated.")
    return

def main():
    mode = input("a=append, m=modify, ls=list: ").strip().lower()

    match mode:
        case "a":
            append_school_record()
        case "m":
            modify_school_record()
        case "ls":
            # print(tabulate.tabulate(SCHOOLS, headers=COLUMNS, tablefmt="pipe"))
            print(f"Row count: {len(SCHOOLS)}")
            with open(PATH_TO_TABULAR_DATA, "w") as f:
                f.write(tabulate.tabulate(SCHOOLS, headers=COLUMNS, tablefmt="pipe"))
            print(f"Data exported to {PATH_TO_TABULAR_DATA.absolute()}")
            with open(PATH_TO_TABULAR_DATA_BACKUP, "w") as f:
                f.write(tabulate.tabulate(SCHOOLS, headers=COLUMNS, tablefmt="pipe"))
            print(f"Backup created at: {PATH_TO_TABULAR_DATA_BACKUP.absolute()}")
        case _:
            print("Invalid mode. Script terminating.")
    return


if __name__ == '__main__':
    main()
