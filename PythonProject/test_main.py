import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from main import authenticate

class TestAuthenticate(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"portal_url": "https://example.com", "username": "user", "password": "pass"}')
    @patch("main.GIS")
    def test_authenticate_success(self, mock_gis, mock_file):
        # Setup mock GIS object and its users.me.username
        mock_gis_instance = MagicMock()
        mock_gis_instance.users.me.username = "user"
        mock_gis.return_value = mock_gis_instance

        gis = authenticate("dummy_path.json")
        mock_file.assert_called_once_with("dummy_path.json")
        mock_gis.assert_called_once_with("https://example.com", "user", "pass")
        self.assertEqual(gis.users.me.username, "user")

    @patch("builtins.open", new_callable=mock_open, read_data='{"portal_url": "https://example.com", "username": "user", "password": "pass"}')
    @patch("main.GIS")
    def test_authenticate_invalid_json(self, mock_gis, mock_file):
        # Simulate invalid JSON structure
        mock_file.return_value.read.return_value = '{"portal_url": "https://example.com", "username": "user"}'  # missing password
        with patch("json.load", side_effect=lambda f: json.loads(f.read())):
            with self.assertRaises(KeyError):
                authenticate("dummy_path.json")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_authenticate_file_not_found(self, mock_file):
        with self.assertRaises(FileNotFoundError):
            authenticate("missing_file.json")

if __name__ == "__main__":
    unittest.main()