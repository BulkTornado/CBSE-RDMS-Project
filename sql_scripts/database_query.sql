CREATE DATABASE CBSE_EXAM_RESULT_YXXXX;
USE CBSE_EXAM_RESULT_YXXXX;


CREATE TABLE COURSES(

    course_code SMALLINT UNSIGNED PRIMARY KEY,
    course_name VARCHAR(50) UNIQUE NOT NULL,

    marks_theory TINYINT UNSIGNED NOT NULL,
    marks_practical_assessment TINYINT UNSIGNED DEFAULT 0 NOT NULL,
    marks_internal_assessment TINYINT UNSIGNED DEFAULT 0 NOT NULL,

    grade ENUM(10, 12) NOT NULL,

    CONSTRAINT chk_valid_marks CHECK(
        (
            marks_theory BETWEEN 0 AND 100
            AND marks_practical_assessment BETWEEN 0 AND 100
            AND marks_internal_assessment BETWEEN 0 AND 100
        )
        AND -- sum is always 100
        (
            marks_theory + marks_practical_assessment + marks_internal_assessment = 100
        )
    )
);


CREATE TABLE AFFILIATED_SCHOOLS(

    affiliation_no INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name_of_institution VARCHAR(80) NOT NULL,

    state VARCHAR(40) NOT NULL,
    district VARCHAR(40) NOT NULL,
    postal_address VARCHAR(255) NOT NULL,
    pin_code MEDIUMINT UNSIGNED NOT NULL,

    website VARCHAR(100) DEFAULT '' NOT NULL,

    year_of_foundation YEAR NOT NULL,
    date_of_first_opening_of_school DATE NOT NULL,

    head_of_institution VARCHAR(50) NOT NULL,

    status_of_the_school ENUM('Middle Class','Secondary Level', 'Senior Secondary Level')
        DEFAULT 'Senior Secondary Level' NOT NULL,
    school_type ENUM('KV', 'GOVT', 'JNV', 'STSS', 'INDEPENDENT') DEFAULT 'INDEPENDENT' NOT NULL,
    affiliation_period_start DATE NOT NULL,
    affiliation_period_end DATE NOT NULL,

    remarks VARCHAR(255) DEFAULT '' NOT NULL,

    CONSTRAINT chk_pin_code CHECK (pin_code BETWEEN 100000 AND 999999)
);


CREATE TABLE REGISTERED_STUDENTS(

    exam_roll_no INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

    school_affiliation_no INT UNSIGNED NOT NULL,
    exam_centre_no INT UNSIGNED NOT NULL,

    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) DEFAULT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('M', 'F', 'O') NOT NULL,
    class ENUM(10, 12) NOT NULL,

    aadhar_no BIGINT UNSIGNED UNIQUE NOT NULL,
    apaar_id BIGINT UNSIGNED UNIQUE NOT NULL,

    category_of_pwd ENUM('Y', 'N') NOT NULL,
    -- admit card starts with 2 english letters and rest filled with integers from 0 to 9
    admit_card_id CHAR(8) UNIQUE NOT NULL,

    FOREIGN KEY (school_affiliation_no)
        REFERENCES AFFILIATED_SCHOOLS(affiliation_no),
    FOREIGN KEY (exam_centre_no)
        REFERENCES AFFILIATED_SCHOOLS(affiliation_no),

    CONSTRAINT chk_aadhar_no
        CHECK (aadhar_no BETWEEN 0 AND 999999999999),
    CONSTRAINT chk_apaar_id
        CHECK (apaar_id BETWEEN 0 AND 999999999999),
    CONSTRAINT chk_admit_card_id
        CHECK (admit_card_id REGEXP '[A-Za-z]{2}[0-9]{6}')
);


CREATE TABLE EXAM_RESULTS (
    exam_roll_no INT UNSIGNED NOT NULL,
    course_code SMALLINT UNSIGNED NOT NULL,

    subject_type ENUM('MAIN','ADDITIONAL') NOT NULL,

    marks_theory TINYINT UNSIGNED NOT NULL,
    marks_practical TINYINT UNSIGNED DEFAULT 0 NOT NULL,
    marks_internal TINYINT UNSIGNED DEFAULT 0 NOT NULL,

    PRIMARY KEY (exam_roll_no, course_code),

    FOREIGN KEY (exam_roll_no)
        REFERENCES REGISTERED_STUDENTS(exam_roll_no)
        ON DELETE CASCADE,

    FOREIGN KEY (course_code)
        REFERENCES COURSES(course_code),

    CONSTRAINT chk_valid_marks CHECK(
        (
            marks_theory BETWEEN 0 AND 100
            AND marks_practical BETWEEN 0 AND 100
            AND marks_internal BETWEEN 0 AND 100
        )
        AND -- sum is always 100
        (
            marks_theory + marks_practical + marks_internal = 100
        )
    )
);
