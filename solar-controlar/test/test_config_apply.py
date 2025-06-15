import unittest
from unittest.mock import MagicMock, call

import datetime

from config_apply import ConfigApply

class TestConfigApply(unittest.TestCase):
    # Constants for test data
    TEST_DATA = {"test": "data"}
    API_KEY_ENV = "GIVENERGY_API_KEY"
    INVERTER_ID_ENV = "GIVENERGY_INVERTER_ID"
    API_KEY_VALUE = "API_KEY"
    INVERTER_ID_VALUE = "INVERTER_ID"
    INVALID_PARAM_ERROR = "Invalid parameter given"
    FIXED_DATETIME = datetime.datetime(2025, 6, 5, 12, 34, 56)
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def setUp(self):
        self.mock_config = self._mock_config()
        self.mock_os = self._mock_os()
        self.mock_givenergy, self.mock_givenergy_instance = self._mock_givenergy()
        self.mock_pytz, self.tz_instance = self._mock_pytz()
        self.mock_datetime = self._mock_datetime()

    def _mock_config(self, data=TEST_DATA):
        mock_config = MagicMock()
        mock_config.get_data.return_value = data
        return mock_config

    def _mock_os(self):
        """Reusable mock for os.getenv."""

        def mock_os_getenv_side_effect(param):
            if param == self.API_KEY_ENV:
                return self.API_KEY_VALUE
            elif param == self.INVERTER_ID_ENV:
                return self.INVERTER_ID_VALUE
            raise Exception(self.INVALID_PARAM_ERROR)

        mock_os = MagicMock()
        mock_os.getenv.side_effect = mock_os_getenv_side_effect
        return mock_os

    def _mock_givenergy(self, battery_level=50):
        mock_givenergy_instance = MagicMock()
        mock_givenergy_instance.battery_level.return_value = battery_level
        mock_givenergy = MagicMock(return_value=mock_givenergy_instance)
        return mock_givenergy, mock_givenergy_instance

    def _mock_pytz(self):
        tz_instance = MagicMock()
        mock_pytz = MagicMock()
        mock_pytz.timezone = MagicMock(return_value=tz_instance)
        return mock_pytz, tz_instance

    def _mock_datetime(self, fixed_datetime=FIXED_DATETIME):
        datetime = MagicMock()
        datetime.datetime = MagicMock()
        datetime.datetime.now = MagicMock(return_value=fixed_datetime)
        return datetime

    def test_get_config(self):
        # GIVEN
        subject = ConfigApply(config=self.mock_config)
        # WHEN
        actual = subject.get_config()
        # THEN
        self.assertEqual(actual, self.TEST_DATA)

    def test_get_givenergy(self):
        # GIVEN
        subject = ConfigApply(os=self.mock_os, GivEnergy=self.mock_givenergy)
        # WHEN
        actual = subject.get_givenergy()
        # THEN
        self.mock_os.getenv.assert_has_calls([call(self.API_KEY_ENV), call(self.INVERTER_ID_ENV)])
        self.mock_givenergy.assert_called_with(self.API_KEY_VALUE, self.INVERTER_ID_VALUE)
        self.assertEqual(actual, self.mock_givenergy_instance)

    def test_get_current_time(self):
        # GIVEN
        subject = ConfigApply(pytz=self.mock_pytz, datetime=self.mock_datetime)
        # WHEN
        actual_now, actual_string = subject.get_current_time()
        # THEN
        self.assertEqual(actual_now, self.FIXED_DATETIME)
        self.assertEqual(actual_string, self.FIXED_DATETIME.strftime(self.DATE_FORMAT))

    def test_charge_to_percentage(self):
        """Tests different battery levels and tolerance settings for charge."""
        test_cases = [
            (True, 70, 80, 5, "2025-06-05 12:34:56 battery_level=70 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 70, 80, 5, "2025-06-05 12:34:56 battery_level=70 target_percentage=80 set_timed_charge(True)"),
            (True, 74, 80, 5, "2025-06-05 12:34:56 battery_level=74 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 74, 80, 5, "2025-06-05 12:34:56 battery_level=74 target_percentage=80 set_timed_charge(True)"),
            (True, 75, 80, 5, "2025-06-05 12:34:56 battery_level=75 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 76, 80, 5, "2025-06-05 12:34:56 battery_level=76 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 80, 80, 5, "2025-06-05 12:34:56 battery_level=80 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 84, 80, 5, "2025-06-05 12:34:56 battery_level=84 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 85, 80, 5, "2025-06-05 12:34:56 battery_level=85 is within tolerance=5 of target_percentage=80 NO CHANGE"),
            (True, 86, 80, 5, "2025-06-05 12:34:56 battery_level=86 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 86, 80, 5, "2025-06-05 12:34:56 battery_level=86 target_percentage=80 set_timed_charge(False)"),
            (True, 90, 80, 5, "2025-06-05 12:34:56 battery_level=90 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 90, 80, 5, "2025-06-05 12:34:56 battery_level=90 target_percentage=80 set_timed_charge(False)"),

            (True, 75, 80, 3, "2025-06-05 12:34:56 battery_level=75 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 75, 80, 3, "2025-06-05 12:34:56 battery_level=75 target_percentage=80 set_timed_charge(True)"),
            (True, 76, 80, 3, "2025-06-05 12:34:56 battery_level=76 target_percentage=80 CHANGE set_timed_charge(True)"),
            (False, 76, 80, 3, "2025-06-05 12:34:56 battery_level=76 target_percentage=80 set_timed_charge(True)"),
            (True, 77, 80, 3, "2025-06-05 12:34:56 battery_level=77 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 80, 80, 3, "2025-06-05 12:34:56 battery_level=80 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 81, 80, 3, "2025-06-05 12:34:56 battery_level=81 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 83, 80, 3, "2025-06-05 12:34:56 battery_level=83 is within tolerance=3 of target_percentage=80 NO CHANGE"),
            (True, 86, 80, 3, "2025-06-05 12:34:56 battery_level=86 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 86, 80, 3, "2025-06-05 12:34:56 battery_level=86 target_percentage=80 set_timed_charge(False)"),
            (True, 90, 80, 3, "2025-06-05 12:34:56 battery_level=90 target_percentage=80 CHANGE set_timed_charge(False)"),
            (False, 90, 81, 3, "2025-06-05 12:34:56 battery_level=90 target_percentage=81 set_timed_charge(False)"),
        ]

        for value_changed, battery_level, target, tolerance, expected_msg in test_cases:
            # GIVEN
            mock_givenergy, mock_givenergy_instance = self._mock_givenergy(battery_level=battery_level)
            mock_givenergy_instance.set_timed_charge.return_value = value_changed
            subject = ConfigApply(pytz=self.mock_pytz, datetime=self.mock_datetime, GivEnergy=mock_givenergy, config=self._mock_config({"charge_to_percentage": target}))
            # WHEN
            msg = subject.charge_to_percentage(mock_givenergy_instance, tolerance, self.FIXED_DATETIME.strftime(self.DATE_FORMAT))
            # THEN
            self.assertEqual(expected_msg, msg)

    def test_limit_timed_export(self):
        """Tests different battery levels and tolerance settings for charge."""
        test_cases = [
            (100, 20, 5, True, "2025-06-05 12:34:56 battery_level=100 target_percentage=20 CHANGE set_timed_export(True)"),
            (26, 20, 5, True, "2025-06-05 12:34:56 battery_level=26 target_percentage=20 CHANGE set_timed_export(True)"),
            (25, 20, 5, True, "2025-06-05 12:34:56 battery_level=25 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (20, 20, 5, True, "2025-06-05 12:34:56 battery_level=20 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (15, 20, 5, True, "2025-06-05 12:34:56 battery_level=15 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (14, 20, 5, True, "2025-06-05 12:34:56 battery_level=14 target_percentage=20 CHANGE set_timed_export(False)"),
            (6, 20, 5, True, "2025-06-05 12:34:56 battery_level=6 target_percentage=20 CHANGE set_timed_export(False)"),

            (100, 20, 5, False, "2025-06-05 12:34:56 battery_level=100 target_percentage=20 set_timed_export(True)"),
            (26, 20, 5, False, "2025-06-05 12:34:56 battery_level=26 target_percentage=20 set_timed_export(True)"),
            (25, 20, 5, False, "2025-06-05 12:34:56 battery_level=25 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (20, 20, 5, False, "2025-06-05 12:34:56 battery_level=20 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (15, 20, 5, False, "2025-06-05 12:34:56 battery_level=15 is within tolerance=5 of target_percentage=20 NO CHANGE"),
            (14, 20, 5, False, "2025-06-05 12:34:56 battery_level=14 target_percentage=20 set_timed_export(False)"),
            (6, 20, 5, False, "2025-06-05 12:34:56 battery_level=6 target_percentage=20 set_timed_export(False)"),

            (100, 20, 3, False, "2025-06-05 12:34:56 battery_level=100 target_percentage=20 set_timed_export(True)"),
            (24, 20, 3, False, "2025-06-05 12:34:56 battery_level=24 target_percentage=20 set_timed_export(True)"),
            (23, 20, 3, False, "2025-06-05 12:34:56 battery_level=23 is within tolerance=3 of target_percentage=20 NO CHANGE"),
            (20, 20, 3, False, "2025-06-05 12:34:56 battery_level=20 is within tolerance=3 of target_percentage=20 NO CHANGE"),
            (17, 20, 3, False, "2025-06-05 12:34:56 battery_level=17 is within tolerance=3 of target_percentage=20 NO CHANGE"),
            (16, 20, 3, False, "2025-06-05 12:34:56 battery_level=16 target_percentage=20 set_timed_export(False)"),
            (6, 20, 3, False, "2025-06-05 12:34:56 battery_level=6 target_percentage=20 set_timed_export(False)"),
        ]

        for battery_level, target_percentage, tolerance, value_changed, expected_msg in test_cases:
            # GIVEN
            mock_givenergy, mock_givenergy_instance = self._mock_givenergy(battery_level=battery_level)
            mock_givenergy_instance.set_timed_export.return_value = value_changed
            subject = ConfigApply(pytz=self.mock_pytz, datetime=self.mock_datetime, GivEnergy=mock_givenergy)
            # WHEN
            msg = subject.limit_timed_export(mock_givenergy_instance, target_percentage, tolerance, self.FIXED_DATETIME.strftime(self.DATE_FORMAT))
            # THEN
            self.assertEqual(expected_msg, msg)

    def test_main(self):
        test_cases = [
            (0, 0, "2025-06-05 00:00:00 no action"),
            (3, 0, "2025-06-05 03:00:00 battery_level=50 target_percentage=10 CHANGE set_timed_charge(False)"),
            (7, 0, "2025-06-05 07:00:00 no action"),
            (16, 15, "2025-06-05 16:15:00 battery_level=50 target_percentage=16 CHANGE set_timed_export(True)"),
            (18, 45, "2025-06-05 18:45:00 battery_level=50 target_percentage=0 CHANGE set_timed_export(True)"),
            (20, 0, "2025-06-05 20:00:00 no action"),
        ]

        for hour, minute, expected_msg in test_cases:
            # GIVEN
            fixed_datetime = datetime.datetime(2025, 6, 5, hour, minute, 0)
            config = self._mock_config({"charge_to_percentage": 10})
            subject = ConfigApply(config=config, os=self.mock_os,  pytz=self.mock_pytz, datetime=self._mock_datetime(fixed_datetime), GivEnergy=self.mock_givenergy)
            # WHEN
            msg = subject.main()
            # THEN
            self.assertEqual(expected_msg, msg)
