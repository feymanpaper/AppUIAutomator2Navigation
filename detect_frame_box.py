from uiautomator2 import Device
import xml.etree.ElementTree as ET

# uiautomator2的文档
# https://github.com/openatx/uiautomator2
# 检测服务的文档
# https://uq2wogygth.feishu.cn/wiki/NU2XwrwjNie7U3knKXIciGORnfh

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

# 获取当前界面所有可点击的组件
def get_clickable_elements(d, ele_uuid_map, activity_name):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                uid = get_unique_id(d, element, activity_name)
                ele_uuid_map[uid] = element
                clickable_elements.append(element)
    return clickable_elements


# uid
# activity + pkg + class + resourceId + loc + text
def get_unique_id(d, ele, activity_name):
    class_name = ele.get("class")
    res_id = ele.get("resource-id")
    pkg_name = ele.get("package")
    text = ele.get("text")
    loc_x, loc_y = get_location(ele)
    uid = activity_name + "-" +pkg_name + "-" + class_name + "-" +res_id + "-" + "(" + str(loc_x) + "," + str(loc_y) + ")" + "-" + text  
    return uid

# 获取组件的位置
def get_location(ele):
    bounds = ele.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2
    return x, y 

if __name__ == "__main__":
    d = Device()
    umap = {}

    # 以下是打印当前页面可点击组件的相关代码,如果需要可以取消注释
    # current_screen = d.current_app()
    # pkg_name = current_screen['package']
    # activity_name = current_screen['activity']
    # clickable_eles = get_clickable_elements(d, umap, activity_name)

    # for ele in clickable_eles:
    #     uid = get_unique_id(d, ele, activity_name)
    #     # 打印组件的信息
    #     print(uid)
    #     # 点击该组件
    #     loc_x, loc_y = get_location(ele)
    #     d.click(loc_x, loc_y)

    #TODO
    # while不断循环, 直到检测到有广告/弹框
    # 1.对app当前界面截图
    # 2.将图片上传到服务器,检测是否有广告/弹框
    # 3.如果有, 服务器返回需要点击的位置; 然后将该位置转换为和 get_location() 一致的坐标x, y; 然后d.click(x, y) 点击该位置.
    # 4.如果没有, 服务器返回空list, 不做处理
    while True:
        ...
