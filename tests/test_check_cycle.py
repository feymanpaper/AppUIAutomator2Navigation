import sys 
sys.path.append("..")

from core_functions import *
from utils import *
from ScreenCompareStrategy import *
import unittest

class TestCheckCycle(unittest.TestCase):
    def test_case1(self):
        s1 = ScreenNode()
        s1.all_text = "1"
        s2 = ScreenNode()
        s2.all_text = "2"
        s1.add_child(s2)
        s2.add_child(s1)
        lcs_comp = ScreenCompareStrategy(LCSComparator())
        res1 = check_cycle(s1, s2, lcs_comp)
        res2 = check_cycle(s2, s1, lcs_comp)

        self.assertTrue(res1)
        self.assertTrue(res2)

    def test_case2(self):
        s1 = ScreenNode()
        s1.all_text = "1"
        s2 = ScreenNode()
        s2.all_text = "2"
        s3 = ScreenNode()
        s3.all_text = "3"
        s4 = ScreenNode()
        s4.all_text = "4"
        lcs_comp = ScreenCompareStrategy(LCSComparator())
        s1.add_child(s2)
        s2.add_child(s3)
        s3.add_child(s4)
        s4.add_child(s1)
        

        self.assertFalse(check_cycle(s3, s2, lcs_comp))
        self.assertFalse(check_cycle(s3, s1, lcs_comp))
        self.assertFalse(check_cycle(s2, s1, lcs_comp))


if __name__ == '__main__':
    unittest.main()

