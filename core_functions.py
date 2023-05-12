from Screen import *
from ScreenCompareStrategy import *
from utils import *


# 只检测一层环
def check_cycle(cur_node: ScreenNode, last_node: ScreenNode, screen_compare_strategy: ScreenCompareStrategy):
    if screen_compare_strategy.compare_screen(cur_node.all_text, last_node.all_text)[0] == True:
        return True
    # if cur_node.children is None or len(cur_node.children) == 0:
    #     return False
    if cur_node.call_map is None or len(cur_node.call_map) == 0 or cur_node.call_map is {}:
        return False
    # for child in cur_node.children:
    #     if screen_compare_strategy.compare_screen(child.all_text, last_node.all_text)[0] == True:
    #         return True
    #     else:
    #         res = check_cycle(child, last_node, screen_compare_strategy)
    #         if res == True:
    #             return True
    for child in cur_node.call_map.values():
        if screen_compare_strategy.compare_screen(child.all_text, last_node.all_text)[0] == True:
            return True
        else:
            res = check_cycle(child, last_node, screen_compare_strategy)
            if res == True:
                return True
    return False


def is_non_necessary_click(cur_clickable_ele_dict):
    if cur_clickable_ele_dict.get("resource-id") == "com.alibaba.android.rimet:id/toolbar":
        return True
    if cur_clickable_ele_dict.get("resource-id") == "com.alibaba.android.rimet:id/back_layout":
        return True

    text = cur_clickable_ele_dict.get("text")

    # TODO 暂时忽略钉钉创建团队的场景
    non_necessary_list = ["相机", "照片", "拍照", "手机文件", "相册", "拍摄", "关注", "粉丝", "进入小红市", "退出登陆", "退出登录", "退出当前账号",
                          "image", 'Image', "photo", "Photo", "视频", "语音", "创建团队", "直播"]
    for non_necessary_str in non_necessary_list:
        if non_necessary_str in text:
            return True

    return False


def print_screen_info(content, is_new):
    cur_screen_node = get_cur_screen_node_from_context(content)
    print("*" * 100)
    if is_new:
        print(
            f"该screen为新: {cur_screen_node.all_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
    else:
        print(
            f"该screen已存在: {cur_screen_node.all_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
    print("*" * 100)


def print_state(state_map, state):
    print(f"状态为{state} {state_map[state]}")


# def get_two_clickable_eles_diff(d, cur_eles, cur_activity, last_eles, last_activity):
#     if last_eles is None or cur_eles is None or len(last_eles) == 0 or len(cur_eles) == 0:
#         return False, None
#     if cur_activity != last_activity:
#         return False, None
#     if len(cur_eles) <= len(last_eles):
#         return False, None
#
#     # union_eles = union(d, cur_eles, cur_activity, last_eles, last_activity)
#     union_eles = list(set(cur_eles).union(set(last_eles)))
#     is_overlap = False
#     if len(union_eles) / len(last_eles) >= 0.90:
#         diff_eles = []
#         is_overlap = True
#         diff_eles = list(set(cur_eles).difference(last_eles))
#         print(f"出现了重叠,可能为框,差分之后数量为{len(diff_eles)}")
#         return is_overlap, diff_eles
#     else:
#         return is_overlap, None

# def check_screen_list(screen_list):
#     if screen_list is None:
#         return False
#     if len(screen_list) >= 5:
#         last_text = screen_list[-1]
#         if  screen_list[-2] == last_text and \
#             screen_list[-3] == last_text and \
#             screen_list[-4] == last_text and \
#             screen_list[-5] == last_text:
#             return True
#     else:
#         return False

def check_state_list_reverse(k, state_list, target) -> bool:
    if k > len(state_list):
        return False
    for i in range(k):
        if state_list[len(state_list) - 1 - i] != target:
            return False
    return True

def check_screen_list_reverse(k, screen_list) -> bool:
    if k <= 1:
        return False
    if screen_list is None or len(screen_list) == 0:
        return False
    if len(screen_list) < k:
        return False
    # step为1, 2, 3
    for step in range(1, 4, 1):
        res = check_screen_list_by_pattern_reverse(k, screen_list, step)
        if res is True:
            return True
    return False


def check_screen_list_by_pattern_reverse(k, screen_list, step) -> bool:
    l = 0
    for i in range(step):
        l += 1
    for cnt in range(0, k - 1, 1):
        for i in range(step):
            if l >= len(screen_list):
                return False
            elif screen_list[len(screen_list) - 1 - l] != screen_list[len(screen_list) - 1 - i]:
                return False
            else:
                l += 1
    return True


def check_screen_list_order(k, screen_list) -> bool:
    if k <= 1:
        raise Exception
    if screen_list is None or len(screen_list) == 0:
        raise Exception
    if len(screen_list) < k:
        return False
    # step为1, 2, 3
    for step in range(1, 4, 1):
        res = check_screen_list_by_pattern_order(k, screen_list, step)
        if res is True:
            return True
    return False


def check_screen_list_by_pattern_order(k, screen_list, step) -> bool:
    l = 0
    for i in range(step):
        l += 1
    for cnt in range(0, k - 1, 1):
        for i in range(step):
            if l >= len(screen_list):
                return False
            elif screen_list[l] != screen_list[i]:
                return False
            else:
                l += 1
    return True


def get_screen_info_from_context(content):
    cur_screen_pkg_name = content["cur_screen_pkg_name"]
    cur_activity = content["cur_activity"]
    cur_screen_all_text = content["cur_screen_all_text"]
    cur_screen_info = content["cur_screen_info"]

    return cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info


def get_cur_screen_node_from_context(content):
    cur_screen_node = content["cur_screen_node"]
    return cur_screen_node
