from DeviceHelper import *
from Utils.OCRUtils import *
from Utils.ScreenshotUtils import *
pp_text_list = get_privacy_policy_ele_list()
if len(pp_text_list)>0:
    print(pp_text_list)
else:
    print("不存在")

path = ScreenshotUtils.screen_shot("aaaa")
print(path)
for pp_text in pp_text_list:
    ans = cal_privacy_ele_loc(path, pp_text)
    print(ans)

