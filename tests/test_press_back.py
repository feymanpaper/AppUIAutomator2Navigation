import sys
sys.path.append("..")
from utils import *
from uiautomator2 import Device
import xml.etree.ElementTree as ET
from FSM import *

all_text = []
d = Device()
ele_uid_map = {}



press_back()