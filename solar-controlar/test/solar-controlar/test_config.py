import unittest
import json
from pathlib import Path
from solarcontrolar.config import Config

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a temporary config file."""
        cls.config_path = Path("test_config.json")
        cls.config_data = {"key": "value", "nested": {"inner_key": "inner_value"}}
        cls.config_path.write_text(json.dumps(cls.config_data, indent=4))

    def test_load_config(self):
        """Verify Config loads data correctly."""
        config = Config(filename=str(self.config_path))
        self.assertEqual(config.get_data(), json.loads(self.config_path.read_text()))

    def test_create_instance_with_data(self):
        """Verify Config initializes correctly when data is passed."""
        initial_data = {"setting": "enabled", "threshold": 42}
        config = Config(data=initial_data)

        self.assertEqual(config.get_data(), initial_data)
        self.assertIsNot(config.get_data(), initial_data)  # Ensure deep copy

    def test_with_data(self):
        """Ensure with_data creates a new instance with a modified copy."""
        config = Config(filename=str(self.config_path))
        new_data = config.get_data()
        new_data["extra"] = "test"

        new_config = config.with_data(new_data)

        # Verify new instance retains copied data but isn't the same object
        self.assertEqual(new_config.get_data(), new_data)
        self.assertIsNot(new_config.get_data(), config.get_data())

    def test_save_config(self):
        """Verify that save() correctly writes data to the file."""
        config = Config(filename=str(self.config_path))
        modified_data = config.get_data()
        modified_data["new_key"] = "new_value"

        new_config = config.with_data(modified_data)
        new_config.save()

        # Verify file now contains updated data
        self.assertEqual(json.loads(self.config_path.read_text())["new_key"], "new_value")

    @classmethod
    def tearDownClass(cls):
        """Clean up test file."""
        cls.config_path.unlink()

if __name__ == "__main__":
    unittest.main()