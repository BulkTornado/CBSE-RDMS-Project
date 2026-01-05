"""
Python program to access MySQL database.
"""

import atexit
import json
import sys, io
from pathlib import Path

import tkinter as tk

import cairosvg
from PIL import Image, ImageTk
import tabulate

from functional_modules import ConnectToMySQL


PATH_TO_ASSETS_DIR  = Path() / "assets"
PATH_TO_CONFIG      = Path() / 'config.json'


# Only 2 assets in SVG format
ASSETS: list[Path] = [
    PATH_TO_ASSETS_DIR / 'CBSE_logo.svg',
    PATH_TO_ASSETS_DIR / 'KVS_logo.svg'
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


cbse_logo_png_bytes = cairosvg.svg2png(url=ASSETS[0].__str__())
kvs_logo_png_bytes  = cairosvg.svg2png(url=ASSETS[1].__str__())

cbse_logo_png       = Image.open(io.BytesIO(cbse_logo_png_bytes)).resize((100, 100))
kvs_logo_png        = Image.open(io.BytesIO(kvs_logo_png_bytes)).resize((100, 100))


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
    query = """
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
    CONN_OB.execute_sql_query(query % affiliation_number)

    fetched_school_records = CONN_OB.fetch_data()

    return fetched_school_records


def get_admit_card_info(exam_roll_number: int):
    query = """
        SELECT
            r.exam_roll_no AS 'Roll No.',
            r.school_affiliation_no AS 'School',
            r.exam_centre_no AS 'Exam Centre No.',
            r.grade AS 'CLASS',
            r.candidate_name AS 'Candidate Name',
            r.mother_name AS 'Mother Name',
            r.guardian_name AS 'Guardian''s/Father''s Name',
            r.date_of_birth AS 'Date of Birth',
            s.name_of_institution AS 'School Name',
            c.name_of_institution AS 'Exam Centre Name',
            r.category_of_pwd AS 'PWD Category',
            r.admit_card_id AS 'Admit Card ID'
        FROM REGISTERED_STUDENTS r
        JOIN AFFILIATED_SCHOOLS s
            ON r.school_affiliation_no = s.affiliation_no
        JOIN AFFILIATED_SCHOOLS c
            ON r.exam_centre_no = c.affiliation_no
        WHERE r.exam_roll_no = %s;
    """
    CONN_OB.execute_sql_query(query % exam_roll_number)

    fetched_student_records = CONN_OB.fetch_data()

    return fetched_student_records


def get_student_record(exam_roll_number: int):
    query_student = """
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

    query_marks = """
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

    CONN_OB.execute_sql_query(query_student % exam_roll_number)
    fetched_student_record = CONN_OB.fetch_data()

    CONN_OB.execute_sql_query(query_marks % exam_roll_number)
    fetched_marks_record = CONN_OB.fetch_data()

    return fetched_student_record, fetched_marks_record


class MainWindow:
    def __init__(self, root: tk.Tk):
        self._root = root

        self._root.title("CBSE Database Manager")
        self._root.geometry("800x150")

        self._root.columnconfigure(1, weight=1)

        tk_cbse_logo = ImageTk.PhotoImage(cbse_logo_png)
        tk_kvs_logo = ImageTk.PhotoImage(kvs_logo_png)

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
    app = MainWindow(root)
    root.mainloop()

    """
    sql_query = get_sql_query()

    try:
        if developer_mode:
            print(f"[DEV MODE] Executing SQL Query:\n{sql_query}\n")
        db_object.execute_sql_query(sql_query)
    # '_mysql' refers to _mysql.connector
    # _mysql.errors.ProgrammingError
    except Exception as error:
        show_error(error)
        return


    data = db_object.fetch_data()

    if data[0] is None:
        print("Query executed successfully (no result set)")

        db_object.commit_to_database()

        return
    # DEBUG: DO NOT REMOVE
    # print(type(data))
    # print(data)
    # print(repr(data))

    # Fetch column names from cursor
    columns = [desc[0] for desc in data[0]]  #type: ignore

    # Pretty print results in a table format
    # OPTS : "simple", "grid"
    print(tabulate.tabulate(data[1], headers=columns, tablefmt="simple"))

    print(f"\nRows retrieved: {data[-1]}")
    """


if __name__ == "__main__":
    main()
