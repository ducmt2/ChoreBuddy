import os
import sys
import logging.config
import unittest

sys.path.append("..")

from database.db import DbHandler, UserRole, ChoreStatus

logging.config.fileConfig("../logging.conf")


class DbTest(unittest.TestCase):
    def setUp(self):
        self.db = DbHandler("test.json")

        self.db.add_new_user("John", UserRole.CHILD)
        self.db.add_new_user("Hayun", UserRole.CHILD)
        self.db.add_new_user("Sung", UserRole.PARENT)

        self.db.add_new_chore("John", "Do the job A.")
        self.db.add_new_chore("John", "Do the job B.")
        self.db.add_new_chore("Hayun", "Do the job C.")
        self.db.add_new_chore("Hayun", "Do the job D.")

    def test_user(self):
        assert self.db.get_role_by_user("John") == UserRole.CHILD
        assert self.db.add_new_user("Young", UserRole.PARENT) == True
        assert self.db.update_user("Sung", "Sungwoo", UserRole.PARENT) == True

    def test_chore(self):
        assert self.db.get_ready_chores_by_user("John")[0]["task"] == "Do the job A."
        assert self.db.get_progress_chore_by_user("John") == None

        chore = self.db.get_ready_chores_by_user("Hayun")[0]
        assert chore["name"] == "Hayun"
        self.db.update_chore_status_by_id(chore.doc_id, ChoreStatus.IN_PROGRESS)
        assert self.db.get_progress_chore_by_user("Hayun").doc_id == chore.doc_id

    def test_value(self):
        assert self.db.get_current_user() == ""
        assert self.db.save_current_user("hello world") == False
        assert self.db.get_current_user() == ""
        assert self.db.save_current_user("John") == True
        assert self.db.get_current_user() == "John"
        assert self.db.save_current_user("Hayun") == True
        assert self.db.get_current_user() == "Hayun"

    def tearDown(self):
        try:
            os.remove("test.json")
        except:
            pass


if __name__ == "__main__":
    unittest.main()
