import sys
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET
from FSM import *


def press_back():
    d.press("back")
    print("进行回退")
    time.sleep(5)
    return

all_text = []
d = Device()
ele_uid_map = {}
press_back()
while True:
    press_back()