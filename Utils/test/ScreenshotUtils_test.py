import unittest
from Utils.ScreenshotUtils import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here
        ScreenshotUtils.screen_shot(ScreenshotUtils.get_screen_uid())
        print(ScreenshotUtils.get_screen_uid())
        #TODO


if __name__ == '__main__':
    unittest.main()


