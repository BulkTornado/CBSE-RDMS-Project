"""
This script is not supposed to be run by anyone else.
I am just fixing my stupid fuckery.
- BulkTornado, 2025-12-05
"""


import json
import datetime
from pathlib import Path
import pickle


PATH_TO_AFFILIATED_SCHOOL = Path() / "data" / "affiliated_schools.dat"
PATH_TO_TABULAR_DATA = Path() / "data"/ "tabular_data" / "affiliated_schools.txt"

DICTIONARY = {}
SCHOOLS = []

with open(PATH_TO_TABULAR_DATA, "r") as f:
    TEXT = f.readlines()

PARSED_DATA = list(
    map(
        lambda x: x.replace("\n", ""),
        TEXT[2:] # Avoiding the header and line partition(refer to the following excerpt below)
    )
)

"""
Since using the tablefmt="pipe" option, so data struc is:
|   affiliation_no | name_of_institution                             | state       | district         | postal_address                                                                           |   pin_code | website                                            |   year_of_foundation | date_of_first_opening_of_school   | head_of_institution    | status_of_the_school   | school_type   | affiliation_period_start   | affiliation_period_end   |
|-----------------:|:------------------------------------------------|:------------|:-----------------|:-----------------------------------------------------------------------------------------|-----------:|:---------------------------------------------------|---------------------:|:----------------------------------|:-----------------------|:-----------------------|:--------------|:---------------------------|:-------------------------|
|           300001 | PM SHRI KENDRIYA VIDYALAYA                      | BIHAR       | PATNA            | DANAPUR CANTT PATNA DISTT BIHAR                                                          |     801503 | www.kvdanapurpatna.org                             |                 1963 | 2009-01-25                        | SANJEEV KUMAR SINHA    | Senior Secondary Level | KV            | 2023-04-01                 | 2028-03-31               |
|           300003 | PM SHRI KENDRIYA VIDYALAYA                      | BIHAR       | PATNA            | KANKAR BAGH PATNA BIHAR                                                                  |     800020 | https://no1patna.kvs.ac.in/                        |                 1966 | 2009-01-25                        | MAHESHWAR PRASAD SINGH | Senior Secondary Level | KV            | 2024-04-01                 | 2029-03-31               |
...
so splitting based on "|" will give ["", affiliation_no, ..., ""]
"""
for i in range(len(PARSED_DATA)):
    DICTIONARY[f"rec{i+1}"] = tuple(
        map(
            lambda x: x.strip(),
            PARSED_DATA[i].split("|")[1:-1]
        )
    )
#print(json.dumps(DICTIONARY, indent=4))
#print(DICTIONARY)

for record in DICTIONARY.values():
    SCHOOLS.append(
        (
            int(record[0]),
            *record[1:5],
            int(record[5]),
            record[6],
            int(record[7]),
            datetime.date(*list(map(int, record[8].split('-')))),
            *record[9:12],
            datetime.date(*list(map(int, record[12].split('-')))),
            datetime.date(*list(map(int, record[13].split('-')))),
            record[-1]
        )
    )
#print(SCHOOLS)
with open(PATH_TO_AFFILIATED_SCHOOL, "wb") as f:
    pickle.dump(SCHOOLS, f)