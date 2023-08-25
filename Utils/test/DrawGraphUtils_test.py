import unittest
from Utils.DrawGraphUtils import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)
        DrawGraphUtils.draw_callgraph()

if __name__ == '__main__':
    unittest.main()
