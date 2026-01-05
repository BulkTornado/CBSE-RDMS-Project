import datetime
import json
import sys
from pathlib import Path

ROOT_DIR                = Path('.')
PATH_TO_CONFIG          = ROOT_DIR / 'config.json'

CURRENT_YEAR: int = datetime.date.today().year - 1

CONFIG = {
    "host": "",
    "user": "",
    "passwd": "",
    "database": "CBSE_EXAM_RESULT_YXXXX",
    "setup_completed": False
}


def main():
    if not PATH_TO_CONFIG.exists():
        print("config.json doesn't exists, creating config.json file first.")
        PATH_TO_CONFIG.touch()
        print("config.json has been created, continuing with setting-up your configs.")

    host        = input("Enter host(press Enter to set host as 'localhost'): ") or "localhost"
    user        = input("Enter username(press Enter to set user as 'root'): ") or "root"
    passwd      = input("Enter password: ")
    database    = CONFIG.get("database").replace("XXXX", str(CURRENT_YEAR))
    setup_completed = bool(input("Press Enter if set up has not been completed before, else enter 1: "))


    CONFIG["host"]             = host
    CONFIG["user"]             = user
    CONFIG["passwd"]           = passwd
    CONFIG["database"]         = database
    CONFIG["setup_completed"]  = setup_completed

    with open("config.json", "w") as f:
        json.dump(CONFIG, f, indent=4)

    print("Configuration has been set.")

if __name__ == '__main__':
    main()
