from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time
import hashlib

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
    signature = pkg_name + '\n' + act_name + '\n' + all_text
    return signature

# 对screen_info进行sha256签名,生成消息摘要
def get_signature(d):
    screen_info = get_screen_info(d)
    signature = hashlib.sha256(screen_info.encode()).hexdigest()
    return signature

def get_clickable_elements(d, umap):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    cnt = 0
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                cnt +=1
                uid = get_unique_id(element, d)
                # uid并不能唯一标识一个组件，因此如果uid相同，umap会被覆盖成最后一个
                umap[uid] = cnt
                clickable_elements.append(element)
    return clickable_elements

# uid
# activity + pkg + class + resourceId + text
def get_unique_id(ele, d):
    acitivity_name = get_current_activity(d)
    class_name = ele.get("class")
    res_id = ele.get("resource-id")
    pkg_name = ele.get("package")
    text = ele.get("text")
    res = acitivity_name + "-" +pkg_name + "-" + class_name + "-" +res_id + "-" + text  
    return res

# uuid
# uid + cnt
def get_uuid(ele, d, umap):
    uid = get_unique_id(ele, d)
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