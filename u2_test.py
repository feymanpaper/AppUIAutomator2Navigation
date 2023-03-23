from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time
from Node import *
from utils import *


def dfs_click(cur_ele:str, node:Node):
    # 点击前检测策略
    # 检查描述信息
    if(cur_ele.get("content-desc") == "返回"):
        return 
    # 记录状态
    x, y = get_location(cur_ele)
    uuid = get_uuid(cur_ele, d, umap)
    vis_map[uuid] = True
    cur_activity = get_current_activity(d)
    cur_node = None
    if node_map.get(cur_activity, False) == False:
        cur_node = Node(cur_activity)
        node_map[cur_activity] = cur_node
        node.add_child(cur_node)
    else:
        cur_node = node_map.get(cur_activity)

    print("处理--"+ uuid)
    d.click(x,y)
    time.sleep(3)
    next_activity = get_current_activity(d)
    # 点击后检测策略
    # 判断当前app是否变成了其他app
    if get_current_window_package(d) != curr_pkg_name:
        print("回退界面-" + next_activity)
        d.press("back")
        time.sleep(3)
        return
    # 暂时忽略WebviewAcitivity
    if "WebView" in next_activity:
        print("切换界面-" + next_activity + " 但是回退")
        d.press("back")
        time.sleep(3)
        return 
    # 如果activity没有变化，则return，这个有问题，比如dialog和fragment有问题，后面需要改
    if cur_activity == next_activity:
        return 
    print("切换界面-" + next_activity)
    # 如果触发了新的，这个时候要判断是否存在环
    if cur_node.find_ancestor(next_activity):
        print("产生环-" + next_activity + " 但是回退")
        d.press("back")
        time.sleep(3)
        return 
    
    clickable_elements = get_clickable_elements(d, umap)
    print("界面-" + next_activity + " 可点击个数为" + str(len(clickable_elements)))
    for next_ele in clickable_elements:
        uuid = get_uuid(next_ele, d, umap)
        if vis_map.get(uuid, False) == False:
            dfs_click(next_ele, cur_node)
        # print(ET.tostring(element))
        # print("*"*100)
    print("回退界面-" + get_current_activity(d))
    d.press("back")
    time.sleep(3)


# umap; {key:uid, value:cnt}
root = Node("root")
node_map = {}
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
    dfs_click(element, root)
    print("结束一轮")

