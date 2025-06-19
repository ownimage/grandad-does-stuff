import unittest
import json
from pathlib import Path
from unittest.mock import MagicMock

from solarcontrolar.givenergy import GivEnergy


class TestGivenergy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_setting_write_validate_bad_return_value(self):
        # GIVEN
        setting_id = 10
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.json.return_value = {'data': {'value': False}}

        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200

        mock_response_3 = MagicMock()
        mock_response_3.status_code = 200
        mock_response_3.json.return_value = {'data': {'value': -6}}

        mock_requests = MagicMock()
        mock_requests.post.side_effect = [mock_response_1, mock_response_2, mock_response_3]

        subject = GivEnergy('API_KEY', 'INVERTER_ID', mock_requests)
        # WHEN
        actual = subject.setting_write_validate(setting_id, True, 'function_name')
        # THEN
        self.assertEqual(actual, True)


if __name__ == '__main__':
    unittest.main()
