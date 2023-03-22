from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time
from utils import *


def dfs_click(cur_ele):
    x, y = get_location(cur_ele)
    uuid = get_uuid(cur_ele, d, umap)
    vis_map[uuid] = True
    pre_activity = get_current_activity(d)
    print("处理--"+ uuid)
    d.click(x,y)
    time.sleep(3)
    cur_activity = get_current_activity(d)
    if "WebView" in cur_activity:
        print("切换界面-" + cur_activity + " 但是回退")
        d.press("back")
        time.sleep(3)
        return 
    if pre_activity != cur_activity:
        print("切换界面-" + cur_activity)
    else:
        #该组件无法触发新的界面,return
        return 
    if get_current_window_package(d) != curr_pkg_name:
        print("回退界面-" + cur_activity)
        d.press("back")
        time.sleep(3)
        return
    clickable_elements = get_clickable_elements(d, umap)
    print("界面-" + cur_activity + " 可点击个数为" + str(len(clickable_elements)))
    for next_ele in clickable_elements:
        uuid = get_uuid(next_ele, d, umap)
        if vis_map.get(uuid, False) == False:
            dfs_click(next_ele)
        # print(ET.tostring(element))
        # print("*"*100)
    print("回退界面-" + get_current_activity(d))
    d.press("back")
    time.sleep(3)


# umap; {key:uid, value:cnt}
umap = {}
vis_map = {} 
d = Device()
# curr_pkg_name = get_current_window_package(d)
curr_pkg_name = "com.alibaba.android.rimet"
d.app_start(curr_pkg_name)
time.sleep(5)
clickable_elements = get_clickable_elements(d, umap)
cnt = 0
for element in clickable_elements:
    # print(ET.tostring(element))
    # print("*"*100)
    cnt += dfs_click(element)
    print("结束一轮")

