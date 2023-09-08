import os
import logging
import yaml

from dotenv import load_dotenv
from database.db import DbHandler, UserRole


def _read(file: str) -> dict():
    data = dict()
    with open(file, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    logging.info("buddy-yaml: %s", data)
    return data


def _clear() -> None:
    file = get_env()["db_path"]
    try:
        if os.path.isfile(file) == True:
            os.remove(file)
    except:
        logging.error("Error: delete the db file.")


def get_env() -> str:
    load_dotenv()
    env = {
        "db_path": os.environ.get("DB_FILE"),
        "data_path": os.environ.get("DATA_FILE"),
    }
    logging.debug("ENV: %s", env)
    return env


def initialize_db() -> None:
    _clear()
    data = _read(get_env()["data_path"])
    db = DbHandler(get_env()["db_path"])

    users = data["user"]
    for name in users["child"]:
        db.add_new_user(name, role=UserRole.CHILD)
    for name in users["parent"]:
        db.add_new_user(name, role=UserRole.PARENT)

    for chore in data["chore"]:
        name = chore["name"]
        for task in chore["task"]:
            db.add_new_chore(name, task)
