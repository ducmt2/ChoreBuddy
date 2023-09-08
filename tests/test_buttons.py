import sys
import logging.config
import unittest

sys.path.append("..")

from utils.buttons import get_button_pressed, ButtonState

logging.config.fileConfig("../logging.conf")


class DbTest(unittest.TestCase):
    def test_button(self):
        assert get_button_pressed(1) == ButtonState.NONE


if __name__ == "__main__":
    unittest.main()
