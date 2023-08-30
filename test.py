import unittest
from Utils.DrawGraphUtils import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        #TODO
        jsonFilePath = "./dumpjson/com.alibaba.android.rimet_restart0activity4&screen9&time85.02s.json"

        # TODO
        screenShotFilePath = "./Screenshot/ScreenshotPicture"
        # TODO 将svg文件保存到目标文件夹，文件夹不存在直接创建
        svgSaveFilePath = "./svgSaveDir"

        DrawGraphUtils.draw_callgraph(jsonFilePath, screenShotFilePath, svgSaveFilePath)


if __name__ == '__main__':
    unittest.main()
