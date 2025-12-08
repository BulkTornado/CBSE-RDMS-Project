CREATE TABLE STUDENT_DATA(

exam_roll_no INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

school_affiliation_no INT UNSIGNED UNIQUE NOT NULL,
exam_centre_no INT UNSIGNED UNIQUE NOT NULL,

first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) DEFAULT NULL,
date_of_birth DATE NOT NULL,
gender CHAR(1) NOT NULL,
class TINYINT UNSIGNED NOT NULL,

aadhar_no BIGINT UNSIGNED UNIQUE NOT NULL,
apaar_id BIGINT UNSIGNED UNIQUE NOT NULL,

category_of_pwd CHAR(1) NOT NULL,
-- admit card starts with 2 english letters and rest filled with integers from 0 to 9
admit_card_id CHAR(8) UNIQUE NOT NULL,

main_subject1 SMALLINT UNSIGNED UNIQUE NOT NULL,
main_subject2 SMALLINT UNSIGNED UNIQUE NOT NULL,
main_subject3 SMALLINT UNSIGNED UNIQUE NOT NULL,
main_subject4 SMALLINT UNSIGNED UNIQUE NOT NULL,
main_subject5 SMALLINT UNSIGNED UNIQUE NOT NULL,
additional_subject1 SMALLINT UNSIGNED UNIQUE DEFAULT NULL,
additional_subject2 SMALLINT UNSIGNED UNIQUE DEFAULT NULL,
additional_subject3 SMALLINT UNSIGNED UNIQUE DEFAULT NULL,


FOREIGN KEY (school_affiliation_no) REFERENCES SCHOOL_DATA(affiliation_no),
FOREIGN KEY (exam_centre_no) REFERENCES SCHOOL_DATA(affiliation_no),

FOREIGN KEY (main_subject1) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (main_subject2) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (main_subject3) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (main_subject4) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (main_subject5) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (additional_subject1) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (additional_subject2) REFERENCES SUBJECT(subject_code),
FOREIGN KEY (additional_subject3) REFERENCES SUBJECT(subject_code),

CONSTRAINT chk_gender CHECK (gender in ('M', 'F', 'O')),
CONSTRAINT chk_class CHECK (class = 10 or class = 12),
CONSTRAINT chk_cat_of_pwd CHECK (category_of_pwd in ('Y', 'N')),
CONSTRAINT chk_aadhar_no CHECK (aadhar_no BETWEEN 0 AND 999999999999),
CONSTRAINT chk_apaar_id CHECK (apaar_id BETWEEN 0 AND 999999999999),
CONSTRAINT chk_admit_card_id CHECK (admit_card_id REGEXP '[A-Za-z]{2}[0-9]{6}')
);
