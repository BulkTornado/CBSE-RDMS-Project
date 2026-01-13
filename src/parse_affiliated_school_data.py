import pickle
import sys
from datetime import date
from pathlib import Path

import tabulate

PATH_TO_AFFILIATED_SCHOOL_DATA          = Path() / "data"       / "affiliated_schools.dat"
PATH_TO_AFFILIATED_SCHOOL_BACKUP_DATA   = Path() / "backup"     / "affiliated_schools.dat"
PATH_TO_TABULAR_DATA                    = Path() / "data"       / "tabular_data"            / "affiliated_schools.txt"


COLUMNS = [
    "affiliation_no",
    "name_of_institution",
    "state",
    "district",
    "postal_address",
    "pin_code",
    "website",
    "year_of_foundation",
    "date_of_first_opening_of_school",
    "head_of_institution",
    "status_of_the_school",
    "school_type",
    "affiliation_period_start",
    "affiliation_period_end",
    "remarks"
]
INDIAN_STATES = [
    'ANDAMAN AND NICOBAR ISLANDS',
    'ANDHRA PRADESH',
    'ARUNACHAL PRADESH',
    'ASSAM',
    'BIHAR',
    'CHHATTISGARH',
    'DELHI',
    'GOA',
    'GUJARAT',
    'HARYANA',
    'HIMACHAL PRADESH',
    'JHARKHAND',
    'KARNATAKA',
    'KERALA',
    'MADHYA PRADESH',
    'MAHARASHTRA',
    'MANIPUR',
    'MEGHALAYA',
    'MIZORAM',
    'NAGALAND',
    'ODISHA',
    'PUNJAB',
    'RAJASTHAN',
    'SIKKIM',
    'TAMIL NADU',
    'TELANGANA',
    'TRIPURA',
    'UTTAR PRADESH',
    'UTTARAKHAND',
    'WEST BENGAL'
]
STATUS_OF_SCHOOL = ["Middle Class", "Secondary Level", "Senior Secondary Level"]
SCHOOL_TYPE = ["KV", "GOVT", "JNV", "STSS", "INDEPENDENT"]
# JNV: Jawahar Navodaya Vidyalaya; STSS: smth from Sambhota Tibetan School

if not PATH_TO_AFFILIATED_SCHOOL_DATA.exists():
    print("File doesn't exists. Creating file and stack SCHOOLS.")
    PATH_TO_AFFILIATED_SCHOOL_DATA.touch()
    print(f"File created at: {PATH_TO_AFFILIATED_SCHOOL_DATA.absolute()}")
    SCHOOLS: list[tuple[int, str, str, str, str, int, str, int, date, str, str, str, date, date, str]] = []
else:
    try:
        with open(PATH_TO_AFFILIATED_SCHOOL_DATA, "rb") as f:
            # type expected: list[tuple[int, str, str, str, str, int, str, int, date, str, str, str, date, date, str]]
            SCHOOLS = pickle.load(f)
    except EOFError:
        print("Empty file, initiating an empty stack SCHOOLS")
        SCHOOLS = []
    except Exception as exc_value:
        print(f"(1) Undocumented exception occurred.\n\t{exc_value}\n")
        print("Terminating script.")
        sys.exit()


def validate_and_return_int_value(line: str) -> int:
    while True:
        try:
            _int_value = int(input(line))
            break
        except ValueError:
            print("Enter a valid base 10 integer.")
        except Exception as exc_value:
            print(f"(2) Undocumented exception occurred.\n\t{exc_value}\n")
            print("Terminating early for safety.")
            sys.exit()
    return _int_value


def validate_and_return_str_value(line: str) -> str:
    while True:
        try:
            # maHARASHTRA, NEW   DELHI -> MAHARASHTRA, NEW DELHI
            _str_value = " ".join(
                input(line).strip().upper().split()
            )
            break
        except Exception as exc_value:
            print(f"(2) Undocumented exception occurred.\n\t{exc_value}\n")
            print("Terminating early for safety.")
            sys.exit()
    return _str_value


def validate_and_return_value_from_list(iterable: list[str], line: str) -> str:
    for index, item in enumerate(iterable, start=1):
        print(f"{index:>02}. {item}")
    while True:
        try:
            _str_value: str = iterable[int(input(line)) - 1]
            break
        except ValueError:
            print("Enter a base 10 integer.")
        except IndexError:
            print("Out of range value.")
        except Exception as exc_value:
            print(f"(3) Undocumented exception occurred.\n\t{exc_value}\n")
            print("Terminating early for safety.")
            sys.exit()
    return _str_value


def validate_and_return_date_object(line: str) -> date:
    while True:
        try:
            # input type expected: DD MM YYYY
            _str_input:         list[str]   = input(line).strip().split()
            mapped_to_int:      map         = map(int, _str_input)
            converted_to_list:  list[int]   = list(mapped_to_int)
            # list type expected: [DD, MM, YYYY]
            # will reverse this when unpacking inside the date() function


            if not len(converted_to_list) == 3:
                print("Exactly 3 values needed in the following format: DD MM YYYY")
                print(f"Number of values provided: {len(converted_to_list)}")
                print(f"Values provided: {converted_to_list}")
                continue
            # Can I remove this?
            """if not (1 <= converted_to_list[-1] <= 9999):
                print(f"year must be in 1...9999, not {converted_to_list[-1]}")
                continue
            if not (1 <= converted_to_list[1] <= 12):
                print(f"month must be in 1...12, not {converted_to_list[1]}")"""
            _date = date(*converted_to_list[::-1])
            break
        except ValueError as exc_value:
            # Will handle the following:
            # 1. non-int values are provided
            # 2. year range
            # 3. month range
            # 4. date range for the particular month and year
            print(exc_value)
        # What exceptions can occur here?
        except Exception as exc_value:
            print(f"(4) Undocumented exception occurred.\n\t{exc_value}\n")
            print("Terminating early for safety.")
            sys.exit()
    return _date


def return_school_record():
    while True:
        affiliation_number: int             = validate_and_return_int_value("\nAffiliation Number: ")
        record_exists: bool                 = any(record[0] == affiliation_number for record in SCHOOLS)

        if record_exists:
            print(f"Record with the affiliation number: {affiliation_number} already exists.")
            continue

        break

    name_of_institution: str                = validate_and_return_str_value("Name of Institution: ")
    state: str                              = validate_and_return_value_from_list(INDIAN_STATES, "State code: ")
    district: str                           = input("District: ").strip().upper()
    postal_address: str                     = validate_and_return_str_value("Postal Address: ")
    pin_code: int                           = validate_and_return_int_value("PIN Code: ")
    website: str                            = input("Website (if any): ").strip() or ""
    year_of_foundation: int                 = validate_and_return_int_value("Year of Foundation: ")
    date_of_first_opening_of_school: date   = validate_and_return_date_object("Date of First Opening of School (DD MM YYYY): ")
    head_of_institution: str                = validate_and_return_str_value("Head of Institution: ")
    status_of_the_school: str               = validate_and_return_value_from_list(STATUS_OF_SCHOOL, "Status of the School: ")
    school_type: str                        = validate_and_return_value_from_list(SCHOOL_TYPE, "School Type: ")
    affiliation_period_start: date          = validate_and_return_date_object("Affiliation Period Start (DD MM YYYY): ")
    affiliation_period_end: date            = validate_and_return_date_object("Affiliation Period End (DD MM YYYY): ")
    remarks: str                            = input("Remarks, if any: ")

    return (
        affiliation_number,
        name_of_institution,
        state,
        district,
        postal_address,
        pin_code,
        website,
        year_of_foundation,
        date_of_first_opening_of_school,
        head_of_institution,
        status_of_the_school,
        school_type,
        affiliation_period_start,
        affiliation_period_end,
        remarks
    )


def append_school_record():
    while True:
        school_record = return_school_record()
        SCHOOLS.append(school_record)
        if input("\nType 'stop' to finish: ").strip().lower() == "stop":
            break
    SCHOOLS.sort(key=lambda x: x[0])
    with (
        open(PATH_TO_AFFILIATED_SCHOOL_DATA, "wb") as f1,
        open(PATH_TO_AFFILIATED_SCHOOL_BACKUP_DATA, "wb") as f2
    ):
        pickle.dump(SCHOOLS, f1)
        pickle.dump(SCHOOLS, f2)
    print("Records updated on disk.")
    return


def modify_school_record():
    if not SCHOOLS:
        print("No records in stack SCHOOLS. Cannot perform operation.")
        return

    affiliation_no: int = validate_and_return_int_value("\nAffiliation Number: ")

    for index, record in enumerate(SCHOOLS):
        if record[0] == affiliation_no:
            print("Record found. Enter new details for this record.\n")
            new_record = return_school_record() #TODO: Serious issue, remember bro
            SCHOOLS[index] = new_record
            break
    else:
        print("Record not found.")
        return

    SCHOOLS.sort(key=lambda x: x[0])
    with (
        open(PATH_TO_AFFILIATED_SCHOOL_DATA, "wb") as f1,
        open(PATH_TO_AFFILIATED_SCHOOL_BACKUP_DATA, "wb") as f2
    ):
        pickle.dump(SCHOOLS, f1)
        pickle.dump(SCHOOLS, f2)
    print("Records updated on disk.")
    return


def remove_school_record():
    if not SCHOOLS:
        print("No records in stack SCHOOLS. Cannot perform operation.")
        return
    affiliation_no: int = validate_and_return_int_value("\nAffiliation Number: ")

    for index, record in enumerate(SCHOOLS):
        if record[0] == affiliation_no:
            break
    else:
        print("Record not found.")
        return

    print(f"Record found.\n\t{record}\n")
    if input("Confirm removing the record (y/n): ").strip().lower() == "y":
        del SCHOOLS[index]
        print("Record deleted.")
        with (
                open(PATH_TO_AFFILIATED_SCHOOL_DATA, "wb") as f1,
                open(PATH_TO_AFFILIATED_SCHOOL_BACKUP_DATA, "wb") as f2
        ):
            pickle.dump(SCHOOLS, f1)
            pickle.dump(SCHOOLS, f2)
        print("Data has been updated on disk.")
        return

    print("Cancelled removing operation...")
    return


def tabular_record():
    if not SCHOOLS:
        print("No record. Cannot make a tabular data.")
        return
    print(f"Row count: {len(SCHOOLS)}")
    with open(PATH_TO_TABULAR_DATA, "w") as f:
        f.write(tabulate.tabulate(SCHOOLS, headers=COLUMNS, tablefmt="pipe"))
    print(f"Data exported to {PATH_TO_TABULAR_DATA.absolute()}")
    return


def main():
    mode = input("a=append, m=modify, rm=remove, ls=list: ").strip().lower()

    match mode:
        case "a":
            append_school_record()
        case "m":
            modify_school_record()
        case "rm":
            remove_school_record()
        case "ls":
            tabular_record()
        case _:
            print("Invalid mode. Script terminating.")
    return


if __name__ == '__main__':
    main()
