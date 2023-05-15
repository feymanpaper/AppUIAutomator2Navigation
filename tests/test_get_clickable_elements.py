import sys 
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET


all_text = []
d = Device()
ele_uid_map = {}

temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = get_screen_info(d)

clickable_eles = get_clickable_elements(d, ele_uid_map, temp_activity)


print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")

#
print(len(clickable_eles))
for idx, ele_id in enumerate(clickable_eles):
    # ele_dict = ele_uid_map[ele_id]
    # text = ele_dict.get("text")
    # print(f"{idx} - {text}")
    print(f"{idx}--{ele_id}")
# print(len(clickable_eles))
# x, y = get_location(ele_uid_map[clickable_eles[12]])
# d.click(x, y)
# print("fck")