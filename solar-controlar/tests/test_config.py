import unittest

from solarcontrolar.config import Config

class TestConfig(unittest.TestCase):
    def test_list_int(self):
        config = Config()
        print(config.get_data())


if __name__ == '__main__':
    unittest.main()