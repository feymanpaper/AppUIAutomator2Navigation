from DeviceHelper import *
from Utils.OCRUtils import *
from Utils.ScreenshotUtils import *
is_pp_exist, pp_text = get_privacy_policy_ele_list()
if is_pp_exist:
    print(pp_text)
else:
    print("不存在")

path = ScreenshotUtils.screen_shot("aaaa")
print(path)
ans = cal_privacy_ele_loc(path, pp_text)
print(ans)

