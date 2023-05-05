import random

from core_functions import *
from utils import *
from ScreenCompareStrategy import *
import unittest


class TestStateList(unittest.TestCase):
    def test_case1(self):
        # state_list = [1,2,3]
        # self.assertFalse(check_state_list(state_list))
        # state_list = [1,2,3,3,3,3,3]
        # self.assertTrue(check_state_list(state_list))
        # state_list = [3,3,3,3]
        # self.assertFalse(check_state_list(state_list))
        # state_list = [1,2,3,3,3,3,3,3,3,4,3,3,3,3,3]
        # self.assertTrue(check_state_list(state_list))
        # state_list = [1,2,3,4,5]
        screen_list = ["a", "b", "c", "d", "e"]
        check_screen_list(screen_list)
        print(screen_list[-4])
        print(random.randint(0, 0))

if __name__ == '__main__':
    unittest.main()
