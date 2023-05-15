
import time
import hashlib

def get_screen_all_text_from_dict(clickable_eles, ele_uid_map):
    text = ""
    for ele_uid in clickable_eles:
        ele_dict = ele_uid_map[ele_uid]
        text += ele_dict.get("text")
    return text


def get_screennode_from_screenmap(screen_map: dict, screen_text: str):
    if screen_map.get(screen_text, None) is None:
        return None
    else:
        return screen_map.get(screen_text)


# 从screen_map里得到取出和screen_text满足相似度阈值且相似度最高的screen_node
def get_screennode_from_screenmap_by_similarity(screen_map: dict, screen_text: str, screen_compare_strategy):
    if screen_map.get(screen_text, False) is False:
        # 如果没有,则遍历找满足相似度阈值的 
        max_similarity = 0
        res_node = None
        for candidate_screen_text in screen_map.keys():
            simi_flag, cur_similarity = screen_compare_strategy.compare_screen(screen_text, candidate_screen_text)
            if simi_flag is True:
                if cur_similarity > max_similarity:
                    max_similarity = cur_similarity
                    res_node = screen_map.get(candidate_screen_text)
        # 返回的要么是None, 要么是相似性最大的screen_node
        return res_node

    # 说明该节点之前存在screen_map
    else:
        return screen_map.get(screen_text)


# def get_screennode_from_diffmap(diff_map: dict, screen_map, screen_compare_strategy):
#     for screen_text in diff_map.keys():
#         res = get_screennode_from_screenmap(screen_map, screen_text, screen_compare_strategy)
#         if res is not None:
#             return res
#     return None



