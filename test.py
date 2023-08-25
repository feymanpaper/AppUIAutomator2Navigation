import unittest
from Utils.DrawGraphUtils import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        #TODO
        jsonFilePath = "./dumpjson/com.alibaba.android.rimet_restart2activity9&screen39&time504.7s.json"
        #TODO
        screenShotFilePath = "./ScreenshotPicture"
        #TODO 将svg文件保存到目标文件夹，文件夹不存在直接创建
        svgSaveFilePath = "./svgSaveDir"
        DrawGraphUtils.draw_callgraph()


if __name__ == '__main__':
    unittest.main()
