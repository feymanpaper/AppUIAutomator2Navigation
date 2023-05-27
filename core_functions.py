from ScreenNode import *
from ScreenCompareStrategy import *
from utils import *
import time

# 检测多层环
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
    non_necessary_list = ["相机", "照片", "拍照", "手机文件", "相册", "拍摄", "关注", "粉丝", "进入小红市", "退出登陆", "注销",
                          "退出登录", "退出当前账号", "下载", "分享", "浏览器", "安装", "浮窗",
                          "image", 'Image', "photo", "Photo", "视频", "语音", "创建团队", "直播"]
    for non_necessary_str in non_necessary_list:
        if non_necessary_str in text:
            return True

    return False


def print_screen_info(content, is_new):
    cur_screen_node = get_cur_screen_node_from_context(content)
    print("*" * 100)
    if is_new:
        print(f"该screen为新: {cur_screen_node.all_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
        if cur_screen_node.diff_clickable_elements is not None:
            print(f"差分后的数量为 {len(cur_screen_node.diff_clickable_elements)}")

    else:
        print(f"该screen已存在: {cur_screen_node.all_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
        if cur_screen_node.diff_clickable_elements is not None:
            print(f"差分后的数量为 {len(cur_screen_node.diff_clickable_elements)}")

    print("*" * 100)


def print_state(state_map, state):
    print(f"状态为{state} {state_map[state]}")


# def get_two_clickable_eles_diff(cur_eles, cur_activity, last_eles, last_activity):
#     if last_eles is None or cur_eles is None or len(last_eles) == 0 or len(cur_eles) == 0:
#         return False, None
#     if cur_activity != last_activity:
#         return False, None
#     if len(cur_eles) <= len(last_eles):
#         return False, None
#
#     # union_eles = union(d, cur_eles, cur_activity, last_eles, last_activity)
#     intersection_eles = list(set(cur_eles).intersection(set(last_eles)))
#     is_overlap = False
#     if len(intersection_eles) / len(last_eles) >= 0.80:
#         diff_eles = []
#         is_overlap = True
#         diff_eles = list(set(cur_eles).difference(last_eles))
#         print(f"出现了重叠,可能为框,差分之后数量为{len(diff_eles)}")
#         return is_overlap, diff_eles
#     else:
#         return is_overlap, None

def get_two_clickable_eles_diff(cur_eles, last_eles):
    if last_eles is None or cur_eles is None or len(last_eles) == 0 or len(cur_eles) == 0:
        return None
    # if cur_activity != last_activity:
    #     return None
    # if len(cur_eles) <= len(last_eles):
    #     return False, None

    # union_eles = union(d, cur_eles, cur_activity, last_eles, last_activity)
    diff_eles = list(set(cur_eles).difference(last_eles))
    print(f"出现了重叠,可能为框,差分之后数量为{len(diff_eles)}")
    return diff_eles




def get_screen_info_from_context(content):
    cur_screen_pkg_name = content["cur_screen_pkg_name"]
    cur_activity = content["cur_activity"]
    cur_screen_all_text = content["cur_screen_all_text"]

    return cur_screen_pkg_name, cur_activity, cur_screen_all_text


def get_cur_screen_node_from_context(content):
    cur_screen_node = content["cur_screen_node"]
    return cur_screen_node


def print_result(stat_activity_set, stat_screen_set, total_eles_cnt, start_time):
    print("@" * 100)
    print("@" * 100)
    print(f"总共点击的activity个数 {len(stat_activity_set)}")
    print(f"总共点击的Screen个数: {len(stat_screen_set)}")
    print(f"总共点击的组件个数: {total_eles_cnt}")
    end_time = time.time()
    print(f"时间为 {end_time - start_time}")

