"""
Python program to access MySQL database.
"""

import atexit
import json
import sys
from pathlib import Path

import tkinter as tk

from PIL import Image, ImageTk
import tabulate

from modules import ConnectToMySQL


PATH_TO_ASSETS_DIR  = Path() / "assets"
PATH_TO_CONFIG      = Path() / 'config.json'


ASSETS: list[Path] = [
    PATH_TO_ASSETS_DIR / 'CBSE_logo.png',
    PATH_TO_ASSETS_DIR / 'KVS_logo.jpeg'
]
MISSING_ASSETS  = []


def check_for_missing_assets() -> bool:
    """
    :return: True if all assets exists, else False
    """

    for _asset in ASSETS:
        if not _asset.exists():
            MISSING_ASSETS.append(_asset.absolute().__str__())

    if MISSING_ASSETS:
        return True
    return False

if check_for_missing_assets():
    print(f"The following assets are missing, go fix them somehow:\n\n\t{'\n\t'.join(MISSING_ASSETS)}\n")
    print(
        f"Please go to my GitHub repo: ..., and from assets directory, download the missing images and\n"
        f"move them inside the following directory: {PATH_TO_ASSETS_DIR.absolute()}"
    )
    print("\nTill no fix, program will not continue to work. Terminating script early...")
    sys.exit()


if not PATH_TO_CONFIG.exists():
    print(f"Config file doesn't exists at the following file path: {PATH_TO_CONFIG.absolute()}")
    print("Run the set_configuration.py file as given in the instruction manual to set up the config file.")
    print("Till then, setup.py cannot complete execution. Terminating early...")
    sys.exit()


with open(PATH_TO_CONFIG, "r") as f:
    CONFIG = json.load(f)


if not CONFIG.get("setup_completed"):
    print("Set-up has not been completed before.")
    print("If that is not the case, please run set_configuration and follow the instructions carefully.")
    sys.exit()

cbse_logo_png       = Image.open(fp = ASSETS[0]).resize((100, 100))
kvs_logo_jpeg       = Image.open(fp = ASSETS[1]).resize((100, 100))

HOST = CONFIG.get("host")
USER = CONFIG.get("user")
PASSWD = CONFIG.get("passwd")
DATABASE = CONFIG.get("database")

CONN_OB = ConnectToMySQL(host=HOST, user=USER, passwd=PASSWD)
CONN_OB.connect_to_database(database_name=DATABASE)


@atexit.register
def close_connection():
    CONN_OB.close_connection()


def get_affiliated_school(affiliation_number: int):
    query_to_retrieve_affiliated_school = """
        SELECT 
            affiliation_no AS 'Affiliation Number',
            name_of_institution AS 'Name of Institution',
            (CONCAT(state, ', ', district)) AS 'State, District', 
            (CONCAT(postal_address, ', ', pin_code)) AS 'Postal Address', 
            website AS 'Website', 
            head_of_institution AS 'Head of Institution', 
            status_of_the_school AS 'Status of the School', 
            school_type AS 'School Type',
            (CONCAT('FROM: ', affiliation_period_start, ' TO: ', affiliation_period_end)) AS 'Affiliation Period',
            remarks AS 'Remarks'
        FROM AFFILIATED_SCHOOLS
        WHERE affiliation_no = %s;
    """
    CONN_OB.execute_sql_query(query_to_retrieve_affiliated_school % affiliation_number)

    fetched_school_records = CONN_OB.fetch_data()

    return fetched_school_records


def get_admit_card_info(exam_roll_number: int):
    query_to_retrieve_admit_card = """
        SELECT
            r.exam_roll_no AS 'Roll No.',
            CONCAT(
                s.affiliation_no, ' - ',
                s.name_of_institution, ', ',
                s.postal_address
            ) AS 'School',
            CONCAT(
                c.affiliation_no, ' - ',
                c.name_of_institution, ', ',
                c.postal_address
            ) AS 'Exam Centre',
            r.grade AS 'CLASS',
            r.candidate_name AS 'Candidate Name',
            r.mother_name AS 'Mother Name',
            r.guardian_name AS 'Guardian''s/Father''s Name',
            r.date_of_birth AS 'Date of Birth',
            r.category_of_pwd AS 'PWD Category',
            r.admit_card_id AS 'Admit Card ID'
        FROM REGISTERED_STUDENTS r
        JOIN AFFILIATED_SCHOOLS s
            ON r.school_affiliation_no = s.affiliation_no
        JOIN AFFILIATED_SCHOOLS c
            ON r.exam_centre_no = c.affiliation_no
        WHERE r.exam_roll_no = %s;
    """
    CONN_OB.execute_sql_query(query_to_retrieve_admit_card % exam_roll_number)

    fetched_student_records = CONN_OB.fetch_data()

    return fetched_student_records


def get_student_record(exam_roll_number: int):
    query_to_retrieve_student_record = """
        SELECT
            r.candidate_name AS 'Candidate Name',
            r.exam_roll_no AS 'Roll No.',
            r.mother_name AS 'Mother Name',
            r.guardian_name AS 'Guardian''s/Father''s Name',
            r.date_of_birth AS 'Date of Birth',
            CONCAT(
                s.affiliation_no, ' - ',
                s.name_of_institution, ', ',
                s.postal_address
            ) AS 'School'
        FROM REGISTERED_STUDENTS r
        JOIN AFFILIATED_SCHOOLS s
            ON r.school_affiliation_no = s.affiliation_no
        WHERE r.exam_roll_no = %s;
    """

    query_to_retrieve_marksheet = """
        SELECT
            c.course_code AS 'Course Code',
            c.course_name AS 'Subject',
            e.marks_theory AS 'Theory',
            (e.marks_practical + e.marks_internal) AS 'IA/PR',
            (e.marks_theory + e.marks_practical + e.marks_internal) AS 'Total'
        FROM EXAM_RESULTS e
        JOIN COURSES c
            ON e.course_code = c.course_code
        JOIN REGISTERED_STUDENTS r
            ON e.exam_roll_no = r.exam_roll_no
        WHERE e.exam_roll_no = %s
        AND c.grade = r.grade
        ORDER BY c.course_code;
    """

    CONN_OB.execute_sql_query(query_to_retrieve_student_record % exam_roll_number)
    fetched_student_record = CONN_OB.fetch_data()

    CONN_OB.execute_sql_query(query_to_retrieve_marksheet % exam_roll_number)
    fetched_marks_record = CONN_OB.fetch_data()

    return fetched_student_record, fetched_marks_record


class MainWindow:
    def __init__(self, root: tk.Tk):
        self._root = root

        self._root.title("CBSE Database Manager")
        self._root.geometry("800x150")

        self._root.columnconfigure(1, weight=1)

        tk_cbse_logo = ImageTk.PhotoImage(cbse_logo_png)
        tk_kvs_logo = ImageTk.PhotoImage(kvs_logo_jpeg)

        self._photo_1 = tk.Label(
            self._root,
            image=tk_cbse_logo
        )
        self._photo_1.grid(row=0, column=0, padx=10, pady=20)

        self.center_text = tk.Label(
            self._root,
            text="Central Board of Secondary Education",
            font=("Jetbrains Mono", 16),
            padx=20, pady=10,
            anchor="center",
            justify="center",
            wraplength=250
        )
        self.center_text.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

        self._photo_2 = tk.Label(
            self._root,
            image=tk_kvs_logo
        )
        self._photo_2.grid(row=0, column=2, padx=10, pady=20)

        self._button_frame = tk.Frame(self._root)

        self._button_frame.grid(row=0, column=3, padx=10)

        self.btn_affl_schl = tk.Button(
            self._button_frame,
            text="Affiliated Schools",
            font=("Jetbrains Mono", 10),
            padx=5, pady=5,
            anchor="center",
            justify="center"
        )
        self.btn_affl_schl.bind("<Button>", lambda e: AffiliatedSchools(self._root))

        self.btn_admit_card = tk.Button(
            self._button_frame,
            text="Admit Card",
            font=("Jetbrains Mono", 10),
            padx=5, pady=5,
            anchor="center",
            justify="center"
        )
        self.btn_admit_card.bind("<Button>", lambda e: AdmitCard(self._root))

        self.btn_exam_result = tk.Button(
            self._button_frame,
            text="Exam Result",
            font=("Jetbrains Mono", 10),
            padx=5, pady=5,
            anchor="center",
            justify="center"
        )
        self.btn_exam_result.bind("<Button>", lambda e: ExamResult(self._root))

        self.btn_affl_schl.pack(fill="x", pady=5)
        self.btn_admit_card.pack(fill="x", pady=5)
        self.btn_exam_result.pack(fill="x", pady=5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


class AffiliatedSchools(tk.Toplevel):
    def __init__(self, master_window=None):
        super().__init__(master_window)
        self.title("Affiliated Schools")
        self.geometry("500x450")

        self.heading = tk.Label(self, text="Affiliated Schools")
        self.heading.config(font=('Jetbrains Mono', 30))
        self.heading.grid(column=0, row=0, columnspan=2)

        self.entry = tk.Entry(self)
        self.entry.config(font=('Consolas', 30))
        self.entry.grid(column=0, row=1, columnspan=2)

        self.output = tk.Label(self, font=('Jetbrains Mono', 10))
        self.output.grid(column=0, row=5)

        self.button = tk.Button(self, text="SUBMIT", command = self.func_1)
        self.button.grid(column=2, row=1)


    def func_1(self):
        input_value = self.entry.get()

        if not input_value.isdigit():
            self.output.config(text="Please enter a integer value.")
            return

        affiliation_number = int(input_value)

        data = get_affiliated_school(affiliation_number)

        if data[-1] == 0:
            self.output.config(text="No record found for the given affiliation number.")
            return

        columns = [desc[0] for desc in data[0]]

        transposed = list(zip(columns, *data[1]))

        display_string = tabulate.tabulate(transposed, tablefmt="grid")

        self.output.config(text=display_string)

        return


class AdmitCard(tk.Toplevel):
    def __init__(self, master_window=None):
        super().__init__(master_window)
        self.title("Admit Card")
        self.geometry("400x700")

        self.heading = tk.Label(self, text="Admit Card")
        self.heading.config(font=("Jetbrains Mono", 30))
        self.heading.grid(column=0, row=0, columnspan=2)

        self.entry = tk.Entry(self)
        self.entry.config(font=("Consolas", 30))
        self.entry.grid(column=0, row=1, columnspan=2)

        self.output = tk.Label(self, font=("Jetbrains Mono", 10))
        self.output.grid(column=0, row=5)

        self.button = tk.Button(self, text="SUBMIT", command=self.func1)
        self.button.grid(column=2, row=1)

    def func1(self):
        input_value = self.entry.get()

        if not input_value.isdigit():
            self.output.config(text="Please enter a integer value")
            return

        exam_roll_no = int(input_value)

        data = get_admit_card_info(exam_roll_no)

        if data[-1] == 0:
            self.output.config(text="No record found.")
            return

        columns = [desc[0] for desc in data[0]]

        transposed = list(zip(columns, *data[1]))

        display_string = tabulate.tabulate(transposed, tablefmt="grid")

        self.output.config(text=display_string)

        return


class ExamResult(tk.Toplevel):
    def __init__(self, master_window=None):
        super().__init__(master_window)
        self.title("Report Maker")
        self.geometry("700x300")

        self.heading = tk.Label(self, text="Exam Result")
        self.heading.config(font=("Jetbrains Mono", 30))
        self.heading.grid(column=0, row=0, columnspan=2)

        self.entry = tk.Entry(self)
        self.entry.config(font=("Consolas", 30))
        self.entry.grid(column=0, row=1, columnspan=2)


        self.output_frame = tk.Frame(self)
        self.output_frame.grid(column=0, row=5, padx=10)

        self.output_heading = tk.Label(
            self.output_frame,
            font=("Jetbrains Mono", 10),
            padx=5, pady=5,
            anchor="center",
            justify="center"
        )

        self.output_student = tk.Label(
            self.output_frame,
            font=("Jetbrains Mono", 10),
            padx=5, pady=5,
            anchor="center",
            justify="center"
        )

        self.output_marks = tk.Label(
            self.output_frame,
            font=("Jetbrains Mono", 10),
            padx=5, pady=5,
            anchor="center",
            justify="center"
        )

        self.output_heading.pack(fill="x", pady=5)
        self.output_student.pack(fill="x", pady=5)
        self.output_marks.pack(fill="x", pady=5)


        self.button = tk.Button(self, text="SUBMIT", command=self.func1)
        self.button.grid(column=2, row=1)


    def func1(self):
        input_value = self.entry.get()

        if not input_value.isdigit():
            self.output_heading.config(text="Please enter a integer value.")
            return

        exam_roll_no = int(input_value)

        student_record, marks_record = get_student_record(exam_roll_no)

        if student_record[-1] == 0:
            self.output_heading.config(text="No record found.")
            return

        student_record_columns = [desc[0] for desc in student_record[0]]
        marks_record_columns = [desc[0] for desc in marks_record[0]]

        student_record_transposed = list(zip(student_record_columns, *student_record[1]))

        display_string_1 = tabulate.tabulate(student_record_transposed, tablefmt="grid")
        display_string_2 = tabulate.tabulate(marks_record[1], headers=marks_record_columns, tablefmt="grid")

        self.output_student.config(text=display_string_1)
        self.output_marks.config(text=display_string_2)

        return


def main() -> None:
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
