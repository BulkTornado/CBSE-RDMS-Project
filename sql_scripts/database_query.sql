CREATE DATABASE CBSE_DATABASE;
USE CBSE_DATABASE;


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

    state ENUM(
    'ANDAMAN AND NICOBAR ISLANDS',
    'ANDHRA PRADESH',
    'ARUNACHAL PRADESH',
    'ASSAM',
    'BIHAR',
    'CHHATTISGARH',
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
    ) NOT NULL,
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

    remarks VARCHAR(255) DEFAULT NULL,

    CONSTRAINT chk_pin_code CHECK (pin_code BETWEEN 0 AND 999999)
);


CREATE TABLE REGISTERED_STUDENTS(

    exam_roll_no INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,

    school_affiliation_no INT UNSIGNED  NOT NULL, -- UNIQUE
    exam_centre_no INT UNSIGNED  NOT NULL, -- UNIQUE

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

    main_subject1 SMALLINT UNSIGNED  NOT NULL, -- UNIQUE
    main_subject2 SMALLINT UNSIGNED  NOT NULL, -- UNIQUE
    main_subject3 SMALLINT UNSIGNED  NOT NULL, -- UNIQUE
    main_subject4 SMALLINT UNSIGNED  NOT NULL, -- UNIQUE
    main_subject5 SMALLINT UNSIGNED  NOT NULL, -- UNIQUE
    additional_subject1 SMALLINT UNSIGNED  DEFAULT NULL, -- UNIQUE
    additional_subject2 SMALLINT UNSIGNED  DEFAULT NULL, -- UNIQUE
    additional_subject3 SMALLINT UNSIGNED  DEFAULT NULL, -- UNIQUE

    FOREIGN KEY (school_affiliation_no) REFERENCES AFFILIATED_SCHOOLS(affiliation_no),
    FOREIGN KEY (exam_centre_no) REFERENCES AFFILIATED_SCHOOLS(affiliation_no),

    FOREIGN KEY (main_subject1) REFERENCES COURSES(course_code),
    FOREIGN KEY (main_subject2) REFERENCES COURSES(course_code),
    FOREIGN KEY (main_subject3) REFERENCES COURSES(course_code),
    FOREIGN KEY (main_subject4) REFERENCES COURSES(course_code),
    FOREIGN KEY (main_subject5) REFERENCES COURSES(course_code),
    FOREIGN KEY (additional_subject1) REFERENCES COURSES(course_code),
    FOREIGN KEY (additional_subject2) REFERENCES COURSES(course_code),
    FOREIGN KEY (additional_subject3) REFERENCES COURSES(course_code),

    CONSTRAINT chk_aadhar_no CHECK (aadhar_no BETWEEN 0 AND 999999999999),
    CONSTRAINT chk_apaar_id CHECK (apaar_id BETWEEN 0 AND 999999999999),
    CONSTRAINT chk_admit_card_id CHECK (admit_card_id REGEXP '[A-Za-z]{2}[0-9]{6}')
);


CREATE TABLE EXAM_RESULTS(
    student_registration_no INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    main_subject_1 TINYINT UNSIGNED NOT NULL,
    main_subject_2 TINYINT UNSIGNED NOT NULL,
    main_subject_3 TINYINT UNSIGNED NOT NULL,
    main_subject_4 TINYINT UNSIGNED NOT NULL,
    main_subject_5 TINYINT UNSIGNED NOT NULL,
    additional_subject_1 TINYINT UNSIGNED NOT NULL,
    additional_subject_2 TINYINT UNSIGNED DEFAULT NULL,
    additional_subject_3 TINYINT UNSIGNED DEFAULT NULL,

    CONSTRAINT chk_valid_marks_range CHECK(
        (main_subject_1 BETWEEN 0 AND 100) AND
        (main_subject_2 BETWEEN 0 AND 100) AND
        (main_subject_3 BETWEEN 0 AND 100) AND
        (main_subject_4 BETWEEN 0 AND 100) AND
        (main_subject_5 BETWEEN 0 AND 100) AND
        (additional_subject_1 BETWEEN 0 AND 100) AND
        (additional_subject_2 BETWEEN 0 AND 100) AND
        (additional_subject_3 BETWEEN 0 AND 100)
    )
);
