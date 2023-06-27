from Utils.SavedInstanceUtils import *
from RuntimeContent import *
from uiautomator2 import Device

file = "../SavedInstance/com.alibaba.android.rimet_screen444time8000s.pickle"
file = "../SavedInstance/com.alibaba.android.rimet_restart0activity0&screen0&time3.41s.pickle"
runtime = SavedInstanceUtils.load_pickle(file)
print(runtime.call_map)