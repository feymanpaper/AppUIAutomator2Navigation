import sys 
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET


all_text = []
d = Device()
umap = {}

temp_screen_pkg, temp_activity, temp_screen_info = get_screen_info(d)
all_text = get_screen_all_text(d)
temp_screen_sig = get_signature(temp_screen_info)
print(f"{temp_screen_pkg}  {temp_activity}  {all_text}  {temp_screen_sig}")

print(len(get_clickable_elements(d, {}, temp_activity)))