from DeviceHelper import *
from Utils.OCRUtils import *
from Utils.ScreenshotUtils import *
ans = is_exist_privacy_policy_ele()
print(ans)

path = ScreenshotUtils.screen_shot("aaaa")
print(path)
ans = cal_privacy_ele_loc(path)
print(ans)

