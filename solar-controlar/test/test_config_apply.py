import unittest
from unittest.mock import MagicMock, patch
import datetime
from solarcontrolar.config import Config
from solarcontrolar.givenergy import GivEnergy
import config_apply


class TestConfigApply(unittest.TestCase):

    def setUp(self):
        self.now = datetime.datetime(2025, 6, 5, 12, 0, 0)
        self.formatted_date = "2025-06-05 12:00:00"

        self.mock_config = MagicMock()
        self.mock_config.get_data.return_value = {"charge_to_percentage": 80, "discharge_to_percentage": 20}

        self.mock_givenergy = MagicMock()
        self.mock_givenergy.battery_level.return_value = 50
        self.mock_givenergy.set_timed_charge.return_value = True
        self.mock_givenergy.set_timed_export.return_value = False
        self.mock_givenergy.set_timed_charge.__name__ = "set_timed_charge"
        self.mock_givenergy.set_timed_export.__name__ = "set_timed_export"

        self.formatted_date = self.now.strftime("%Y-%m-%d %H:%M:%S")

        self.now = MagicMock()
        self.now.strftime.return_value = self.formatted_date

        config_apply.pytz = MagicMock()
        config_apply.pytz.timezone.return_value = MagicMock()

        config_apply.datetime = MagicMock()
        config_apply.datetime.datetime = MagicMock()
        config_apply.datetime.datetime.now.return_value = self.now
        config_apply.datetime.datetime.strftime.return_value = self.formatted_date

    def test_get_current_time(self):
        now, formatted_date = config_apply.get_current_time()

        self.assertEqual(now, self.now)
        self.assertEqual(formatted_date, self.formatted_date)

        config_apply.pytz.timezone.assert_called_with("Europe/London")
        config_apply.datetime.datetime.now.assert_called_with(config_apply.pytz.timezone.return_value)
        self.now.strftime.assert_called_with("%Y-%m-%d %H:%M:%S")


    def test_charge_to_percentage(self):
        """Tests different battery levels and tolerance settings for charge."""
        test_cases = [
            (True, 70, 80, 5, "2025-06-05 12:00:00 battery_level=70 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 70, 80, 5, "2025-06-05 12:00:00 battery_level=70 target_percentage=80 set_timed_charge(True)"),
            (True, 74, 80, 5, "2025-06-05 12:00:00 battery_level=74 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 74, 80, 5, "2025-06-05 12:00:00 battery_level=74 target_percentage=80 set_timed_charge(True)"),
            (True, 75, 80, 5, "2025-06-05 12:00:00 battery_level=75 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 76, 80, 5, "2025-06-05 12:00:00 battery_level=76 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 80, 80, 5, "2025-06-05 12:00:00 battery_level=80 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 84, 80, 5, "2025-06-05 12:00:00 battery_level=84 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 85, 80, 5, "2025-06-05 12:00:00 battery_level=85 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 86, 80, 5, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 86, 80, 5, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 set_timed_charge(False)"),
            (True, 90, 80, 5, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 90, 80, 5, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 set_timed_charge(False)"),

            (True, 75, 80, 3, "2025-06-05 12:00:00 battery_level=75 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 75, 80, 3, "2025-06-05 12:00:00 battery_level=75 target_percentage=80 set_timed_charge(True)"),
            (True, 76, 80, 3, "2025-06-05 12:00:00 battery_level=76 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 76, 80, 3, "2025-06-05 12:00:00 battery_level=76 target_percentage=80 set_timed_charge(True)"),
            (True, 77, 80, 3, "2025-06-05 12:00:00 battery_level=77 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 80, 80, 3, "2025-06-05 12:00:00 battery_level=80 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 81, 80, 3, "2025-06-05 12:00:00 battery_level=81 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 83, 80, 3, "2025-06-05 12:00:00 battery_level=83 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 86, 80, 3, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 86, 80, 3, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 set_timed_charge(False)"),
            (True, 90, 80, 3, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 90, 80, 3, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 set_timed_charge(False)"),
        ]

        for value_changed, battery_level, target, tolerance, expected_msg in test_cases:
            self.mock_config.get_data.return_value["charge_to_percentage"] = target
            self.mock_givenergy.battery_level.return_value = battery_level
            self.mock_givenergy.set_timed_charge.return_value = value_changed
            # WHEN
            msg = config_apply.charge_to_percentage(self.mock_config, self.mock_givenergy, tolerance, self.formatted_date)
            # THEN
            self.assertEqual(expected_msg, msg)

    def test_limit_timed_export(self):
        """Tests different battery levels and tolerance settings for charge."""
        test_cases = [
            (16, 0, 100, 5, True, "2025-06-05 12:00:00 battery_level=100 is within tolerance=5 of target_percentage=100 NO CHANGE"),
            (16, 0, 99, 5, True, "2025-06-05 12:00:00 battery_level=99 is within tolerance=5 of target_percentage=100 NO CHANGE"),
            (16, 0, 95, 5, True, "2025-06-05 12:00:00 battery_level=95 is within tolerance=5 of target_percentage=100 NO CHANGE"),
            (16, 0, 94, 5, True, "2025-06-05 12:00:00 battery_level=94 target_percentage=100 CHANGE set_timed_export(False)"),
            (16, 0, 90, 5, True, "2025-06-05 12:00:00 battery_level=90 target_percentage=100 CHANGE set_timed_export(False)"),
            (16, 0, 10, 5, True, "2025-06-05 12:00:00 battery_level=10 target_percentage=100 CHANGE set_timed_export(False)"),
            (16, 0, 0, 5, True, "2025-06-05 12:00:00 battery_level=0 target_percentage=100 CHANGE set_timed_export(False)"),

            (16, 0, 100, 5, False, "2025-06-05 12:00:00 battery_level=100 is within tolerance=5 of target_percentage=100 NO CHANGE"),
            (16, 0, 99, 5, False, "2025-06-05 12:00:00 battery_level=99 is within tolerance=5 of target_percentage=100 NO CHANGE"),
            (16, 0, 95, 5, False, "2025-06-05 12:00:00 battery_level=95 is within tolerance=5 of target_percentage=100 NO CHANGE"),
            (16, 0, 94, 5, False, "2025-06-05 12:00:00 battery_level=94 target_percentage=100 set_timed_export(False)"),
            (16, 0, 90, 5, False, "2025-06-05 12:00:00 battery_level=90 target_percentage=100 set_timed_export(False)"),
            (16, 0, 10, 5, False, "2025-06-05 12:00:00 battery_level=10 target_percentage=100 set_timed_export(False)"),
            (16, 0, 0, 5, False, "2025-06-05 12:00:00 battery_level=0 target_percentage=100 set_timed_export(False)"),

            (17, 30, 100, 5, True, "2025-06-05 12:00:00 battery_level=100 target_percentage=50 CHANGE set_timed_export(True)"),
            (17, 30, 56, 5, True, "2025-06-05 12:00:00 battery_level=56 target_percentage=50 CHANGE set_timed_export(True)"),
            (17, 30, 55, 5, True, "2025-06-05 12:00:00 battery_level=55 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 50, 5, True, "2025-06-05 12:00:00 battery_level=50 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 50, 5, True, "2025-06-05 12:00:00 battery_level=50 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 45, 5, True, "2025-06-05 12:00:00 battery_level=45 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 44, 5, True, "2025-06-05 12:00:00 battery_level=44 target_percentage=50 CHANGE set_timed_export(False)"),
            (17, 30, 10, 5, True, "2025-06-05 12:00:00 battery_level=10 target_percentage=50 CHANGE set_timed_export(False)"),
            (17, 30, 0, 5, True, "2025-06-05 12:00:00 battery_level=0 target_percentage=50 CHANGE set_timed_export(False)"),

            (17, 30, 100, 5, False, "2025-06-05 12:00:00 battery_level=100 target_percentage=50 set_timed_export(True)"),
            (17, 30, 56, 5, False, "2025-06-05 12:00:00 battery_level=56 target_percentage=50 set_timed_export(True)"),
            (17, 30, 55, 5, False, "2025-06-05 12:00:00 battery_level=55 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 50, 5, False, "2025-06-05 12:00:00 battery_level=50 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 50, 5, False, "2025-06-05 12:00:00 battery_level=50 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 45, 5, False, "2025-06-05 12:00:00 battery_level=45 is within tolerance=5 of target_percentage=50 NO CHANGE"),
            (17, 30, 44, 5, False, "2025-06-05 12:00:00 battery_level=44 target_percentage=50 set_timed_export(False)"),
            (17, 30, 10, 5, False, "2025-06-05 12:00:00 battery_level=10 target_percentage=50 set_timed_export(False)"),
            (17, 30, 0, 5, False, "2025-06-05 12:00:00 battery_level=0 target_percentage=50 set_timed_export(False)"),

            (17, 30, 52, 1, False, "2025-06-05 12:00:00 battery_level=52 target_percentage=50 set_timed_export(True)"),
            (17, 30, 51, 1, False, "2025-06-05 12:00:00 battery_level=51 is within tolerance=1 of target_percentage=50 NO CHANGE"),
            (17, 30, 50, 1, False, "2025-06-05 12:00:00 battery_level=50 is within tolerance=1 of target_percentage=50 NO CHANGE"),
            (17, 30, 49, 1, False, "2025-06-05 12:00:00 battery_level=49 is within tolerance=1 of target_percentage=50 NO CHANGE"),
            (17, 30, 48, 1, False, "2025-06-05 12:00:00 battery_level=48 target_percentage=50 set_timed_export(False)"),
         ]

        for hour, minute, battery_level, tolerance, value_changed, expected_msg in test_cases:
            # GIVEN
            self.mock_givenergy.battery_level.return_value = battery_level
            self.mock_givenergy.set_timed_export.return_value = value_changed
            # WHEN
            msg = config_apply.limit_timed_export(self.mock_givenergy, hour, minute, tolerance, self.formatted_date)
            # THEN
            self.assertEqual(expected_msg, msg)

if __name__ == "__main__":
    unittest.main()