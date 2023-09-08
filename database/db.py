import logging
from enum import Enum
from tinydb import Query, TinyDB, table


class UserRole(Enum):
    CHILD = "Child"
    PARENT = "Parent"
    UNKNOWN = "Unknown"


class ChoreStatus(Enum):
    READY = "Ready"
    IN_PROGRESS = "In progress"
    DONE = "Done"


class DbHandler:
    def __init__(self, path) -> None:
        self._db = TinyDB(path)
        self._users = self._db.table("users")
        self._chores = self._db.table("chores")
        self._values = self._db.table("values")

    #
    # "users": { "name": <user name>, "role": <role> }
    # role: CHILD, PARENT, UNKNOWN
    #

    def get_role_by_user(self, name: str) -> UserRole:
        users = self._users.search(Query().name == name)
        logging.debug("DB: role_by_user(%s) => %s", name, users)

        if len(users) > 1:
            return UserRole.UNKNOWN

        if len(users) == 0:
            return UserRole.UNKNOWN

        return UserRole[users[0]["role"]]

    def get_children(self) -> list:
        results = self._users.search(Query().role == UserRole.CHILD.name)
        logging.debug("DB: users.search(CHILD) => %s", results)
        return results

    def add_new_user(self, name: str, role: UserRole) -> bool:
        users = self._users.search(Query().name == name)
        logging.debug("DB: users.search(%s) => %s", name, users)

        if len(users) != 0:
            return False

        docid = self._users.insert({"name": name, "role": role.name})
        logging.debug("DB: add_new_user(%s,%s) => %d", name, role.name, docid)
        return True

    def update_user(self, name: str, new_name: str, role: UserRole) -> bool:
        users = self._users.search(Query().name == name)
        logging.debug("DB: users.search(%s) => %s", name, users)

        if len(users) > 1:
            return False

        if len(users) == 0:
            return False

        docids = self._users.update(
            {"name": new_name, "role": role.name}, (Query().name == name)
        )
        logging.debug("DB: update_user(%s,%s) => %s", new_name, role.name, docids)
        return True

    #
    # "chores": { "name": <user name>, "task": <chore>, "status": <status> }
    # status: READY, IN_PROGRESS, DONE
    #

    def count_chores_by_user(self, name: str, status: ChoreStatus) -> int:
        Chore = Query()
        chores = self._chores.search(
            (Chore.name == name) & (Chore.status == status.name)
        )
        logging.debug("DB: chores_by_user(%s, %s) => %s", name, status.name, chores)
        return len(chores)

    def get_ready_chores_by_user(self, name: str) -> list:
        Chore = Query()
        chores = self._chores.search(
            (Chore.name == name) & (Chore.status == ChoreStatus.READY.name)
        )
        logging.debug("DB: ready_chores_by_user(%s) => %s", name, chores)
        return chores

    def get_progress_chore_by_user(self, name: str) -> table.Document:
        Chore = Query()
        chores = self._chores.search(
            (Chore.name == name) & (Chore.status == ChoreStatus.IN_PROGRESS.name)
        )
        logging.debug("DB: progress_chores_by_user(%s) => %s", name, chores)

        if len(chores) > 1:
            return None

        if len(chores) == 0:
            return None

        return chores[0]

    def add_new_chore(self, name: str, task: str) -> bool:
        user = self._users.get(Query().name == name)
        logging.debug("DB: users.get(%s) => %s", name, user)

        if user == None:
            return False

        Chore = Query()
        chores = self._chores.search((Chore.name == name) & (Chore.task == task))
        logging.debug("DB: chores.search(%s, %s) => %s", name, task, chores)

        if len(chores) != 0:
            return False

        docid = self._chores.insert(
            {
                "name": name,
                "task": task,
                "status": ChoreStatus.READY.name,
            }
        )
        logging.debug("DB: add_new_user(%s,%s) => %d", name, task, docid)
        return True

    def update_chore(self, id: int, name: str, task: str, status: ChoreStatus) -> bool:
        chore = self._chores.get(doc_id=id)
        logging.debug("DB: chores.get(%d) => %s", id, chore)

        if chore == None:
            return False

        docids = self._chores.update(
            {"name": name, "task": task, "status": status.name}, doc_ids=[id]
        )
        logging.debug(
            "DB: update_chore(%s,%s,%s) => %s", name, task, status.name, docids
        )
        return True

    def update_chore_status_by_id(self, id: int, status: ChoreStatus) -> bool:
        chores = self._chores.update({"status": status.name}, doc_ids=[id])
        logging.debug(
            "DB: update_chore_status_by_id(%d,%s) => %s", id, status.name, chores
        )
        return True if len(chores) == 1 else False

    #
    # "values": { "name": <user name> }
    #

    def get_current_user(self) -> str:
        user = self._values.get(doc_id=1)
        logging.debug("DB: get_current_user() => %s", user)

        if user == None:
            return ""

        return user["name"]

    def save_current_user(self, name: str) -> bool:
        user = self._users.get(Query().name == name)
        logging.debug("DB: users.get(%s) => %s", name, user)

        if user == None:
            return False

        current_user = self._values.get(doc_id=1)
        logging.debug("DB: values.get() => %s", current_user)

        if current_user == None:
            self._values.insert({"name": name})
        else:
            self._values.update({"name": name}, doc_ids=[1])

        logging.debug("DB: save_current_user(%s)", name)
        return True
