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


    def test_apply_config_charge(self):
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

            msg = config_apply.apply_config(self.mock_config, self.mock_givenergy, "charge_to_percentage",
                               lambda lvl, tgt: lvl <= tgt, self.mock_givenergy.set_timed_charge,
                               tolerance, self.now, self.formatted_date)

            self.assertEqual(expected_msg, msg)

    def test_apply_config_discharge(self):
        """Tests different battery levels and tolerance settings for discharge."""
        test_cases = [
            (True, 10, 20, 5, "2025-06-05 12:00:00 battery_level=10 target_percentage=20 CHANGE set_timed_export(False)"),
            (False, 10, 20, 5, "2025-06-05 12:00:00 battery_level=10 target_percentage=20 set_timed_export(False)"),
            (True, 14, 20, 5, "2025-06-05 12:00:00 battery_level=14 target_percentage=20 CHANGE set_timed_export(False)"),
            (False, 14, 20, 5, "2025-06-05 12:00:00 battery_level=14 target_percentage=20 set_timed_export(False)"),
            (True, 15, 20, 5, "2025-06-05 12:00:00 battery_level=15 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (True, 20, 20, 5, "2025-06-05 12:00:00 battery_level=20 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (True, 25, 20, 5, "2025-06-05 12:00:00 battery_level=25 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (True, 26, 20, 5, "2025-06-05 12:00:00 battery_level=26 target_percentage=20 CHANGE set_timed_export(True)"),
            (False, 26, 20, 5, "2025-06-05 12:00:00 battery_level=26 target_percentage=20 set_timed_export(True)"),
            (True, 30, 20, 5, "2025-06-05 12:00:00 battery_level=30 target_percentage=20 CHANGE set_timed_export(True)"),
            (False, 30, 20, 5, "2025-06-05 12:00:00 battery_level=30 target_percentage=20 set_timed_export(True)"),

            (True, 10, 20, 3, "2025-06-05 12:00:00 battery_level=10 target_percentage=20 CHANGE set_timed_export(False)"),
            (False, 10, 20, 3, "2025-06-05 12:00:00 battery_level=10 target_percentage=20 set_timed_export(False)"),
            (True, 16, 20, 3, "2025-06-05 12:00:00 battery_level=16 target_percentage=20 CHANGE set_timed_export(False)"),
            (False, 16, 20, 3, "2025-06-05 12:00:00 battery_level=16 target_percentage=20 set_timed_export(False)"),
            (True, 17, 20, 3, "2025-06-05 12:00:00 battery_level=17 is within tolerance=3 of target_percentage=20 NO CHANGE"),
            (True, 20, 20, 3, "2025-06-05 12:00:00 battery_level=20 is within tolerance=3 of target_percentage=20 NO CHANGE"),
            (True, 23, 20, 3, "2025-06-05 12:00:00 battery_level=23 is within tolerance=3 of target_percentage=20 NO CHANGE"),
            (True, 24, 20, 3, "2025-06-05 12:00:00 battery_level=24 target_percentage=20 CHANGE set_timed_export(True)"),
            (False, 24, 20, 3, "2025-06-05 12:00:00 battery_level=24 target_percentage=20 set_timed_export(True)"),
            (True, 30, 20, 3, "2025-06-05 12:00:00 battery_level=30 target_percentage=20 CHANGE set_timed_export(True)"),
            (False, 30, 20, 3, "2025-06-05 12:00:00 battery_level=30 target_percentage=20 set_timed_export(True)"),        ]

        for value_changed, battery_level, target, tolerance, expected_msg in test_cases:
            self.mock_config.get_data.return_value["discharge_to_percentage"] = target
            self.mock_givenergy.battery_level.return_value = battery_level
            self.mock_givenergy.set_timed_export.return_value = value_changed

            msg = config_apply.apply_config(self.mock_config, self.mock_givenergy, "discharge_to_percentage",
                               lambda lvl, tgt: lvl >= tgt, self.mock_givenergy.set_timed_export,
                               tolerance, self.now, self.formatted_date)

            self.assertEqual(expected_msg, msg)

if __name__ == "__main__":
    unittest.main()