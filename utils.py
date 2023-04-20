from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time
import hashlib
import re

system_view = [
    "com.android.systemui",
    "com.android.launcher",
    "com.google.android.apps.nexuslauncher",
    "com.android.settings",
    "com.google.android.googlequicksearchbox",
    "com.google.android.gms",
    "com.google.android.inputmethod.latin",
    "com.android.chrome"
]


# 获取当前界面所有的可点击组件的文本内容，如果该节点可点但没有文本
# 那大概率文本存在其子节点上
def get_screen_all_text(d):
    text = ""
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)   
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                temp_text = element.get("text")
                if temp_text:
                    text += temp_text + " "
                    # print(temp_text)
                else:
                    text += traverse_tree(element)
    return text

# 递归遍历节点的所有子节点
def traverse_tree(node):
    text = ""
    if node is None:
        return text
    if node.get("text"):
        text += node.get("text")
        # print(node.get("text"))
        return text
    for child in node:
        text += traverse_tree(child)
    return text

# screen_info = package_name + activity_name + screen_all_text
def get_screen_info(d):
    current_screen = d.current_app()
    pkg_name = current_screen['package']
    act_name = current_screen['activity']
    all_text = get_screen_all_text(d)
    all_info = pkg_name + '\n' + act_name + '\n' + all_text
    return pkg_name, act_name, all_text, all_info


# 从screen_map里得到取出和screen_text满足相似度阈值且相似度最高的screen_node
def get_screennode_from_screenmap(screen_map:dict, screen_text:str, screen_compare_strategy):
    if screen_map.get(screen_text, False) is False:
        # 如果没有,则遍历找满足相似度阈值的 
        max_similarity = 0
        for candidate_screen_text in screen_map.keys():
            res_node = None
            simi_flag, cur_similarity =  screen_compare_strategy.compare_screen(screen_text, candidate_screen_text)
            if simi_flag is True:
                if cur_similarity > max_similarity:
                    max_similarity = cur_similarity
                    res_node = screen_map.get(candidate_screen_text)
        # 返回的要么是None, 要么是相似性最大的screen_node
        return res_node

    # 说明该节点之前存在screen_map
    else:
        return screen_map.get(screen_text)     


# # 对screen_info进行sha256签名,生成消息摘要
# def get_signature(screen_info):
#     signature = hashlib.sha256(screen_info.encode()).hexdigest()
#     return signature

def get_clickable_elements(d, umap, cur_activity):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    cnt = 0
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                cnt +=1
                uid = get_unique_id(element, d, cur_activity)
                # uid并不能唯一标识一个组件，因此如果uid相同，umap会被覆盖成最后一个
                umap[uid] = cnt
                clickable_elements.append(element)
    return clickable_elements

# uid
# activity + pkg + class + resourceId + text
def get_unique_id(ele, d, cur_activity):
    # acitivity_name = get_current_activity(d)
    class_name = ele.get("class")
    res_id = ele.get("resource-id")
    pkg_name = ele.get("package")
    text = ele.get("text")
    
    res = cur_activity + "-" +pkg_name + "-" + class_name + "-" +res_id + "-" + text  
    return res

# uuid
# uid + cnt
def get_uuid(ele, d, umap, cur_activity):
    uid = get_unique_id(ele, d, cur_activity)
    cnt = umap.get(uid)
    uuid = uid + "&&&" + str(cnt)
    return uuid

def get_uuid_cnt(uuid):
    # print(uuid)
    start = uuid.find("&&&")
    res = ""
    if start != -1:
        res = uuid[start+3 : ]
    return int(res)

#获取页面的坐标
def get_location(ele):
    bounds = ele.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2
    return x, y 


#不全，没有resoure-id
def print_current_window_all_clickable_elements(d):
    clickable_elements = d(clickable=True)
    for ele in clickable_elements:
        print(ele.info.get('text'))

#com.alibaba.android.rimet
def get_current_window_package(d):
    current_app = d.current_app()
    return current_app['package']

def get_current_activity(d):
    current_app = d.current_app()
    return current_app["activity"]



def get_top_activity(d):
    output = d.shell("dumpsys window | grep mCurrentFocus").output
    pattern = r"{(.*)}"
    # Using re.search() to find the first occurrence of the pattern in the string
    match = re.search(pattern, output)

    # If a match is found, print the matched substring
    if match:
        return match.group(1)
    else:
        return None


def print_current_window_detailed_elements(d):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                clickable_elements.append(element)
    for element in clickable_elements:
        print(ET.tostring(element))
        print("*"*100)
    print("*"*100)
    print(len(clickable_elements))
    bounds = element.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2