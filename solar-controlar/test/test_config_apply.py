# import unittest
# from unittest.mock import MagicMock, patch
# import datetime
# from solarcontrolar.config import Config
# from solarcontrolar.givenergy import GivEnergy
# import config_apply
#
#
# class TestConfigApply(unittest.TestCase):
#
#     def setUp(self):
#         self.now = datetime.datetime(2025, 6, 5, 12, 0, 0)
#         self.formatted_date = "2025-06-05 12:00:00"
#
#         self.mock_givenergy = MagicMock()
#         self.mock_givenergy.battery_level.return_value = 50
#         self.mock_givenergy.set_timed_charge.return_value = True
#         self.mock_givenergy.set_timed_export.return_value = False
#         self.mock_givenergy.set_timed_charge.__name__ = "set_timed_charge"
#         self.mock_givenergy.set_timed_export.__name__ = "set_timed_export"
#
#         self.formatted_date = self.now.strftime("%Y-%m-%d %H:%M:%S")
#
#         self.now = MagicMock()
#         self.now.strftime.return_value = self.formatted_date
#
#         config_apply.get_config = MagicMock(return_value={"charge_to_percentage": 80})
#         settings = {
#             "battery_capacity_kWh": 9.6,
#             "battery_min_kWh": 0.4,
#             "solar_forecast_multiplier": 0.9,
#             "tolerance_percent": 1,
#             "last_30mins_discharge_target": 16
#         }
#         config_apply.get_settings = MagicMock(return_value=settings)
#
#         config_apply.pytz = MagicMock()
#         config_apply.pytz.timezone.return_value = MagicMock()
#
#         config_apply.datetime = MagicMock()
#         config_apply.datetime.datetime = MagicMock()
#         config_apply.datetime.datetime.now.return_value = self.now
#         config_apply.datetime.datetime.strftime.return_value = self.formatted_date
#
#     def test_get_current_time(self):
#         now, formatted_date = config_apply.get_current_time()
#
#         self.assertEqual(now, self.now)
#         self.assertEqual(formatted_date, self.formatted_date)
#
#         config_apply.pytz.timezone.assert_called_with("Europe/London")
#         config_apply.datetime.datetime.now.assert_called_with(config_apply.pytz.timezone.return_value)
#         self.now.strftime.assert_called_with("%Y-%m-%d %H:%M:%S")
#
#     def test_charge_to_percentage(self):
#         """Tests different battery levels and tolerance settings for charge."""
#         test_cases = [
#             (True, 70, 80, 5, "2025-06-05 12:00:00 battery_level=70 target_percentage=80 CHANGE set_timed_charge(True)"),
#             (False, 70, 80, 5, "2025-06-05 12:00:00 battery_level=70 target_percentage=80 set_timed_charge(True)"),
#             (True, 74, 80, 5, "2025-06-05 12:00:00 battery_level=74 target_percentage=80 CHANGE set_timed_charge(True)"),
#             (False, 74, 80, 5, "2025-06-05 12:00:00 battery_level=74 target_percentage=80 set_timed_charge(True)"),
#             (True, 75, 80, 5, "2025-06-05 12:00:00 battery_level=75 is within tolerance=5 of target_percentage=80 NO CHANGE"),
#             (True, 76, 80, 5, "2025-06-05 12:00:00 battery_level=76 is within tolerance=5 of target_percentage=80 NO CHANGE"),
#             (True, 80, 80, 5, "2025-06-05 12:00:00 battery_level=80 is within tolerance=5 of target_percentage=80 NO CHANGE"),
#             (True, 84, 80, 5, "2025-06-05 12:00:00 battery_level=84 is within tolerance=5 of target_percentage=80 NO CHANGE"),
#             (True, 85, 80, 5, "2025-06-05 12:00:00 battery_level=85 is within tolerance=5 of target_percentage=80 NO CHANGE"),
#             (True, 86, 80, 5, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 CHANGE set_timed_charge(False)"),
#             (False, 86, 80, 5, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 set_timed_charge(False)"),
#             (True, 90, 80, 5, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 CHANGE set_timed_charge(False)"),
#             (False, 90, 80, 5, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 set_timed_charge(False)"),
#
#             (True, 75, 80, 3, "2025-06-05 12:00:00 battery_level=75 target_percentage=80 CHANGE set_timed_charge(True)"),
#             (False, 75, 80, 3, "2025-06-05 12:00:00 battery_level=75 target_percentage=80 set_timed_charge(True)"),
#             (True, 76, 80, 3, "2025-06-05 12:00:00 battery_level=76 target_percentage=80 CHANGE set_timed_charge(True)"),
#             (False, 76, 80, 3, "2025-06-05 12:00:00 battery_level=76 target_percentage=80 set_timed_charge(True)"),
#             (True, 77, 80, 3, "2025-06-05 12:00:00 battery_level=77 is within tolerance=3 of target_percentage=80 NO CHANGE"),
#             (True, 80, 80, 3, "2025-06-05 12:00:00 battery_level=80 is within tolerance=3 of target_percentage=80 NO CHANGE"),
#             (True, 81, 80, 3, "2025-06-05 12:00:00 battery_level=81 is within tolerance=3 of target_percentage=80 NO CHANGE"),
#             (True, 83, 80, 3, "2025-06-05 12:00:00 battery_level=83 is within tolerance=3 of target_percentage=80 NO CHANGE"),
#             (True, 86, 80, 3, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 CHANGE set_timed_charge(False)"),
#             (False, 86, 80, 3, "2025-06-05 12:00:00 battery_level=86 target_percentage=80 set_timed_charge(False)"),
#             (True, 90, 80, 3, "2025-06-05 12:00:00 battery_level=90 target_percentage=80 CHANGE set_timed_charge(False)"),
#             (False, 90, 81, 3, "2025-06-05 12:00:00 battery_level=90 target_percentage=81 set_timed_charge(False)"),
#         ]
#
#         for value_changed, battery_level, target, tolerance, expected_msg in test_cases:
#             config_apply.givEnergy = MagicMock()
#             config_apply.givEnergy.battery_level.return_value = battery_level
#             config_apply.get_config = MagicMock(return_value={"charge_to_percentage": target})
#
#             self.mock_givenergy.battery_level.return_value = battery_level
#             self.mock_givenergy.set_timed_charge.return_value = value_changed
#             # WHEN
#             msg = config_apply.charge_to_percentage(self.mock_givenergy, tolerance, self.formatted_date)
#             # THEN
#             self.assertEqual(expected_msg, msg)
#
#     def test_limit_timed_export(self):
#         """Tests different battery levels and tolerance settings for charge."""
#         test_cases = [
#             (100, 20, 5, True, "2025-06-05 12:00:00 battery_level=100 target_percentage=20 CHANGE set_timed_export(True)"),
#             (26, 20, 5, True, "2025-06-05 12:00:00 battery_level=26 target_percentage=20 CHANGE set_timed_export(True)"),
#             (25, 20, 5, True, "2025-06-05 12:00:00 battery_level=25 is within tolerance=5 of target_percentage=20 NO CHANGE"),
#             (20, 20, 5, True, "2025-06-05 12:00:00 battery_level=20 is within tolerance=5 of target_percentage=20 NO CHANGE"),
#             (15, 20, 5, True, "2025-06-05 12:00:00 battery_level=15 is within tolerance=5 of target_percentage=20 NO CHANGE"),
#             (14, 20, 5, True, "2025-06-05 12:00:00 battery_level=14 target_percentage=20 CHANGE set_timed_export(False)"),
#             (6, 20, 5, True, "2025-06-05 12:00:00 battery_level=6 target_percentage=20 CHANGE set_timed_export(False)"),
#
#             (100, 20, 5, False, "2025-06-05 12:00:00 battery_level=100 target_percentage=20 set_timed_export(True)"),
#             (26, 20, 5, False, "2025-06-05 12:00:00 battery_level=26 target_percentage=20 set_timed_export(True)"),
#             (25, 20, 5, False, "2025-06-05 12:00:00 battery_level=25 is within tolerance=5 of target_percentage=20 NO CHANGE"),
#             (20, 20, 5, False, "2025-06-05 12:00:00 battery_level=20 is within tolerance=5 of target_percentage=20 NO CHANGE"),
#             (15, 20, 5, False, "2025-06-05 12:00:00 battery_level=15 is within tolerance=5 of target_percentage=20 NO CHANGE"),
#             (14, 20, 5, False, "2025-06-05 12:00:00 battery_level=14 target_percentage=20 set_timed_export(False)"),
#             (6, 20, 5, False, "2025-06-05 12:00:00 battery_level=6 target_percentage=20 set_timed_export(False)"),
#
#             (100, 20, 3, False, "2025-06-05 12:00:00 battery_level=100 target_percentage=20 set_timed_export(True)"),
#             (24, 20, 3, False, "2025-06-05 12:00:00 battery_level=24 target_percentage=20 set_timed_export(True)"),
#             (23, 20, 3, False, "2025-06-05 12:00:00 battery_level=23 is within tolerance=3 of target_percentage=20 NO CHANGE"),
#             (20, 20, 3, False, "2025-06-05 12:00:00 battery_level=20 is within tolerance=3 of target_percentage=20 NO CHANGE"),
#             (17, 20, 3, False, "2025-06-05 12:00:00 battery_level=17 is within tolerance=3 of target_percentage=20 NO CHANGE"),
#             (16, 20, 3, False, "2025-06-05 12:00:00 battery_level=16 target_percentage=20 set_timed_export(False)"),
#             (6, 20, 3, False, "2025-06-05 12:00:00 battery_level=6 target_percentage=20 set_timed_export(False)"),
#
#         ]
#
#         for battery_level, target_percentage, tolerance, value_changed, expected_msg in test_cases:
#             # GIVEN
#             self.mock_givenergy.battery_level.return_value = battery_level
#             self.mock_givenergy.set_timed_export.return_value = value_changed
#             # WHEN
#             msg = config_apply.limit_timed_export(self.mock_givenergy, target_percentage, tolerance, self.formatted_date)
#             # THEN
#             self.assertEqual(expected_msg, msg)
#
#     def test_main(self):
#         test_cases = [
#             (0, 0, "2025-06-05 00:00:00 no action"),
#             (3, 0, "charge_to_percentage"),
#             (7, 0, "2025-06-05 07:00:00 no action"),
#             (16, 15, "limit_timed_export"),
#             (18, 45, "full_discharge"),
#             (20, 0, "2025-06-05 20:00:00 no action"),
#         ]
#
#         for hour, minute, expected_msg in test_cases:
#             # GIVEN
#             config_apply.get_givenergy = MagicMock()
#             working_datetime = datetime.datetime(2025, 6, 5, hour, minute, 0)
#             config_apply.get_current_time = MagicMock()
#             config_apply.get_current_time.return_value = datetime.datetime(2025, 6, 5, hour, minute, 0), working_datetime.strftime("%Y-%m-%d %H:%M:%S")
#             config_apply.charge_to_percentage = MagicMock()
#             config_apply.charge_to_percentage.return_value = "charge_to_percentage"
#             config_apply.limit_timed_export = MagicMock()
#             config_apply.limit_timed_export.return_value = "limit_timed_export"
#             config_apply.full_discharge = MagicMock()
#             config_apply.full_discharge.return_value = "full_discharge"
#             # WHEN
#             msg = config_apply.main()
#             # THEN
#             self.assertEqual(expected_msg, msg)
#
#
# if __name__ == "__main__":
#     unittest.main()
