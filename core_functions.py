from Screen import *
from ScreenCompareStrategy import *

# 只检测一层环
def check_cycle(cur_node: ScreenNode, last_node:ScreenNode, screen_compare_strategy: ScreenCompareStrategy):
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
        