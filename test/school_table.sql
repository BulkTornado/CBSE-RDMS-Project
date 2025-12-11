CREATE TABLE SCHOOL_DATA(

affiliation_no INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
name_of_institution VARCHAR(80) UNIQUE NOT NULL,

state VARCHAR(20) NOT NULL,
district VARCHAR(30) NOT NULL,
postal_address VARCHAR(100) NOT NULL,
pin_code MEDIUMINT UNSIGNED NOT NULL,

website VARCHAR(50) DEFAULT NULL,

year_of_foundation INT NOT NULL,
date_of_first_opening_of_school DATE NOT NULL,

head_of_institution VARCHAR(30) NOT NULL,

status_of_the_school VARCHAR(25) NOT NULL,
school_type VARCHAR(11) NOT NULL,
co_education CHAR(1) NOT NULL,
affiliation_period_start DATE NOT NULL,
affiliation_period_end DATE NOT NULL,

remarks VARCHAR(255) DEFAULT NULL,

CONSTRAINT chk_pin_code CHECK (pin_code BETWEEN 0 AND 999999),
CONSTRAINT chk_state CHECK (state IN (
    'Andaman and Nicobar Islands',
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chhattisgarh',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jharkhand',
    'Karnataka',
    'Kerala',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal'
)),
CONSTRAINT chk_yr_of_found CHECK (year_of_foundation BETWEEN 1800 AND 2100),
CONSTRAINT chk_status_of_school CHECK (status_of_the_school IN (
    'Middle Class',
    'Secondary Level',
    'Senior Secondary Level'
)),
CONSTRAINT chk_schl_type CHECK (school_type IN ('KV', 'GOVT', 'INDEPENDENT')),
CONSTRAINT chk_co_ed CHECK (co_education IN ('Y', 'N'))
);
