import datetime
import json
from pathlib import Path

PATH_TO_CONFIG          = Path() / 'config.json'

CURRENT_YEAR: int = datetime.date.today().year

CONFIG = {
    "host": "",
    "user": "",
    "passwd": "",
    "database": "",
    "setup_completed": False
}


def main():
    if not PATH_TO_CONFIG.exists():
        print("config.json doesn't exists, creating config.json file first.")
        PATH_TO_CONFIG.touch()
        print(
            f"config.json has been created at the following path: {PATH_TO_CONFIG.absolute()},\n"
            f"continuing with setting-up your configs."
        )

    host            = input("Enter host(press Enter to set host as 'localhost'): ") or "localhost"
    user            = input("Enter username(press Enter to set user as 'root'): ") or "root"
    passwd          = input("Enter password: ")
    database        = "CBSE_EXAM_RESULT_YXXXX".replace("XXXX", str(CURRENT_YEAR))
    setup_completed = bool(input("Press Enter if set up has not been completed before, else enter 1: "))


    CONFIG["host"]             = host
    CONFIG["user"]             = user
    CONFIG["passwd"]           = passwd
    CONFIG["database"]         = database
    CONFIG["setup_completed"]  = setup_completed


    with open(PATH_TO_CONFIG, "w") as f:
        json.dump(CONFIG, f, indent=4)

    print("Configuration has been set.")

if __name__ == '__main__':
    main()
