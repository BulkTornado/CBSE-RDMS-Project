import json
import sys
from pathlib import Path

ROOT_DIR = Path('.')
PATH_TO_CONFIG = ROOT_DIR / 'config.json'
PATH_TO_ASSETS_DIR = ROOT_DIR / 'assets'
ASSETS = [
    PATH_TO_ASSETS_DIR / 'icon.png'
]
MISSING_ASSETS: list[str] = []

CONFIGS = {
  "host": "",
  "user": "",
  "passwd": "",
  "databases": [
        "CBSE-EXAM-RESULT-Y2023",
        "CBSE-EXAM-RESULT-Y2024",
        "CBSE-EXAM-RESULT-Y2025"
    ],
  "title": "CBSE Database Manager",
  "geometry": [700, 400],
  "assets": []
}


def check_for_missing_assets() -> bool:
    """
    :return: True if all assets exists, else False
    """

    for asset in ASSETS:
        if not asset.exists():
            MISSING_ASSETS.append(asset.absolute().__str__())

    if MISSING_ASSETS:
        return True
    return False


def main():
    if not PATH_TO_CONFIG.exists():
        print("config.json doesn't exists, creating config.json file first.")
        PATH_TO_CONFIG.touch()
        print("config.json has been created, continue with setting-up your configs.")

    if not PATH_TO_ASSETS_DIR.exists():
        print("Assets directory does not exists. Creating the directory now...")
        PATH_TO_ASSETS_DIR.mkdir()
        print(f"Assets directory has been created. Please go to my GitHub repo: ..., and from assets directory,\n"
              f"download all of the images and move them inside the following directory: {PATH_TO_ASSETS_DIR.absolute()}")
        print("Until then, program will not work properly. Exiting program execution now...")
        sys.exit()

    if check_for_missing_assets():
        print(f"The following assets are missing, go fix them somehow:\n\n\t{'\n\t'.join(MISSING_ASSETS)}\n")
        print(
            f"Please go to my GitHub repo: ..., and from assets directory, download the missing images and\n"
            f"move them inside the following directory: {PATH_TO_ASSETS_DIR.absolute()}"
        )
        print("\nTill no fix, program will not continue to work. Terminating script early...")
        sys.exit()

    host = input("Enter host(press Enter to set host as 'localhost'): ") or "localhost"
    user = input("Enter username(press Enter to set user as 'root'): ") or "root"
    passwd = input("Enter password: ")
    assets = [asset.absolute().__str__() for asset in ASSETS]


    CONFIGS["host"] = host
    CONFIGS["user"] = user
    CONFIGS["passwd"] = passwd
    CONFIGS["assets"] = assets

    with open("config.json", "w") as f:
        json.dump(CONFIGS, f, indent=4)

    print("Configuration has been set.")

if __name__ == '__main__':
    main()
