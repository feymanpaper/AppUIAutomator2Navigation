from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time
from Node import *
from utils import *


def dfs_click(cur_ele:str, node:Node):
    #--------------------------------------
    # 点击前检测策略

    # 检查描述信息
    # if(cur_ele.get("content-desc") == "返回"):
    #     return 
    # 记录状态
    x, y = get_location(cur_ele)
    #获取当前组件的uuid
    uuid = get_uuid(cur_ele, d, umap)
    #当前activity
    cur_activity = get_current_activity(d)
    #当前activity，用node来表示activity_graph中的一个节点
    cur_node = None
    #建图activity_graph
    if node_map.get(cur_activity, False) == False:
        cur_node = Node(cur_activity)
        node_map[cur_activity] = cur_node
        node.add_child(cur_node)
    else:
        cur_node = node_map.get(cur_activity)

    #--------------------------------------
    #判断当前组件是否需要访问
    #1.如果没访问过，即vis_map[uuid]=False，就直接访问
    #2.如果访问过了，即vis_map[uuid]=True,还得判断该组件是否是
    #当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(next_activity)
    #的所有组件是否访问完毕
    if vis_map.get(uuid, False) == True:
        if cur_node.call_map.get(uuid, None) is not None:
            # 如果有部分没有完成
            if not cur_node.is_all_childen_finish():
                print("yes")
            else:
                return 
        else:
            return
        
    #--------------------------------------
    #准备处理该组件
    print("处理--"+ uuid)
    vis_map[uuid] = True
    #如果当前节点，即cur_node表示的当前activity是第一次访问
    #需要设置一下cur_node的total_cnt
    if cur_node.total_cnt == -1:
        #将clickable_element放到class，优化
        #todo
        if activity_clickable_map.get(cur_activity, None) is None:
            res = get_clickable_elements(d, umap)
            activity_clickable_map[cur_activity] = res
            cur_node.total_cnt = len(res)
        else:
            res = activity_clickable_map[cur_activity]
            cur_node.total_cnt = len(res)
    cur_node.click_cnt +=1
    # d(resourceId = cur_ele.get("resource-id")).click()
    d.click(x,y)
    time.sleep(3)

    #--------------------------------------
    #跳转后的判断逻辑

    #EditText点击之后会有输入框，此时无法点击其他组件
    #因此需要back消除输入框，然后return
    if("EditText" in cur_ele.get("class")):
        d.press("back")
        return 
    
    next_activity = get_current_activity(d)
    # 判断当前app是否变成了其他app，即跳出了测试的app
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

    #如果触发了新的界面，这个时候要判断是否存在环，存在环就不加call_map
    #表示虽然该组件能触发新界面，但是会产生环，因此不能将next_activity加入call_map
    if cur_node.find_ancestor(next_activity):
        print("产生环" + next_activity)
    else:
        cur_node.call_map[uuid] = next_activity

    #-----------------------------------
    #遍历页面(next_activity)所有可点击的组件
    clickable_elements = None
    if activity_clickable_map.get(next_activity, None) is None:
        clickable_elements = get_clickable_elements(d, umap)
        activity_clickable_map[next_activity] = clickable_elements
    else:
        clickable_elements = activity_clickable_map[next_activity]

    print("界面-" + next_activity + " 可点击个数为" + str(len(clickable_elements)))
    for next_ele in clickable_elements:
        dfs_click(next_ele, cur_node)
        # print(ET.tostring(element))
        # print("*"*100)
    print("回退界面-" + get_current_activity(d))
    d.press("back")
    time.sleep(3)


root = Node("root")
# node_map : {key: cur_activity, value: cur_node}
node_map = {}
# umap: {key:uid, value:cnt}
umap = {}
# vis_map: {key:element, value:true/false}
vis_map = {}
# activity_clickable_map:{key:activity_name, value = clickable_elements}
activity_clickable_map = {}



d = Device()
# curr_pkg_name = get_current_window_package(d)
curr_pkg_name = "com.example.myapplication"
# curr_pkg_name = "com.alibaba.android.rimet"
d.app_start(curr_pkg_name)
time.sleep(3)
clickable_elements = get_clickable_elements(d, umap)
cnt = 0
for element in clickable_elements:
    # print(ET.tostring(element))
    # print("*"*100)
    dfs_click(element, root)
    print("结束一轮")

