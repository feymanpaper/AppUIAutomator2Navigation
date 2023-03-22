from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time

system_view = [
    "com.android.systemui",
    "com.android.launcher",
    "com.google.android.apps.nexuslauncher",
    "com.android.settings",
    "com.google.android.googlequicksearchbox",
    "com.google.android.gms",
    "com.google.android.inputmethod.latin"
]



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
    uuid = uid + "-" + str(cnt)
    return uuid

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