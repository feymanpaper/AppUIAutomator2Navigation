from uiautomator2 import Device
from DeviceHelper import get_screen_info
from DeviceHelper import get_clickable_elements

all_text = []
d = Device()
ele_uid_map = {}

temp_screen_pkg, temp_activity, temp_all_text = get_screen_info()

clickable_eles = get_clickable_elements()


print(f"{temp_screen_pkg}  {temp_activity}  {temp_all_text}")

#
print(len(clickable_eles))
for idx, ele_id in enumerate(clickable_eles):
    # ele_dict = ele_uid_map[ele_id]
    # text = ele_dict.get("text")
    # print(f"{idx} - {text}")
    print(f"{idx}--{ele_id}")
# print(len(clickable_eles))
# x, y = get_location(ele_uid_map[clickable_eles[2]])
# d.click(x, y)
# print("fck")