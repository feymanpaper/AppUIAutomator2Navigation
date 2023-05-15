import sys
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET


all_text = []
d = Device()
umap = {}
print(get_screen_all_clickable_text_and_loc(d))