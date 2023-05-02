from Screen import *
from ScreenCompareStrategy import *

# 只检测一层环
def check_cycle(cur_node: ScreenNode, last_node:ScreenNode, screen_compare_strategy: ScreenCompareStrategy):
    if screen_compare_strategy.compare_screen(cur_node.all_text, last_node.all_text)[0] == True:
        return True
    if cur_node.children is None or len(cur_node.children) == 0:
        return False
    for child in cur_node.children:
        if screen_compare_strategy.compare_screen(child.all_text, last_node.all_text)[0] == True:
            return True
    return False
        # else:
        #     res = check_cycle(child, last_node)
        #     if res == True:
        #         return True

def is_non_necessary_click(cur_clickable_ele):
    if cur_clickable_ele.get("resource-id") == "com.alibaba.android.rimet:id/toolbar":
        return True
    if cur_clickable_ele.get("resource-id") == "com.alibaba.android.rimet:id/back_layout":
        return True
    if "相机" in cur_clickable_ele.get("text"):
        return True
    if "照片" in cur_clickable_ele.get("text"):
        return True
    if "拍照" in cur_clickable_ele.get("text"):
        return True
    if "手机文件" in cur_clickable_ele.get("text"):
        return True
    
    return False
