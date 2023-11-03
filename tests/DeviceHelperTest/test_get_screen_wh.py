import unittest
from unittest.mock import patch
from utils.DeviceUtils import get_screen_wh

class TestGetScreenWh(unittest.TestCase):
    @patch("utils.DeviceUtils.get_device_info")
    def test_get_screen_wh(self, get_device_info_mock):
        get_device_info_mock.return_value = {"displayWidth":20, "displayHeight":20, "otherProperties":1000}
        res = get_screen_wh()
        self.assertEqual(res, (20, 20))
        get_device_info_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()