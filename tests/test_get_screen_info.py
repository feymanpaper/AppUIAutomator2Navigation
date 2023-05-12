import sys 
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET

def get_screen_info(d):
    current_screen = d.app_current()
    # current_screen = d.current_app()
    pkg_name = current_screen['package']
    act_name = current_screen['activity']
    all_text = get_screen_all_text(d)
    all_info = pkg_name + '\n' + act_name + '\n' + all_text
    return pkg_name, act_name, all_text, all_info

all_text = []
d = Device()
current_screen = d.app_current()
umap = {}
print(get_screen_info(d))
print(type(current_screen['package']))