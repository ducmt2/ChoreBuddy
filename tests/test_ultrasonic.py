import sys
import logging.config
import unittest

sys.path.append("..")

from utils.ultrasonic import detect_object

logging.config.fileConfig("../logging.conf")


class DbTest(unittest.TestCase):
    def test_detect(self):
        assert detect_object(1) == False
        assert detect_object(1000) == True


if __name__ == "__main__":
    unittest.main()
