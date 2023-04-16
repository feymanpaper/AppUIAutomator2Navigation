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

temp_screen_sig = get_signature(temp_screen_info)

print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}  {temp_screen_sig}")


# for ele in clickable_eles:
#     print(ele.get('package'))