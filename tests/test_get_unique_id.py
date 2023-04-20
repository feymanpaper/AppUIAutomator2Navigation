import sys 
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET


all_text = []
d = Device()
umap = {}

temp_screen_pkg, temp_activity, temp_all_text, temp_screen_info = get_screen_info(d)

clickable_eles = get_clickable_elements(d, umap, temp_activity)


print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")


# x, y = get_location(clickable_eles[8])
# d.click(x, y)

for ele in clickable_eles:
    uid = get_unique_id(d, ele, temp_activity)
    print(uid) 