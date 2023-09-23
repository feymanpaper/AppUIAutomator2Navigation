from utils.ScreenCompareStrategy import *
from Config import *
from RuntimeContent import *
from ScreenNode import *


def get_max_similarity_screen_node(ck_eles_text: str) -> tuple[float | ScreenNode]:
    screen_map = RuntimeContent.get_instance().get_screen_map()
    if screen_map.get(ck_eles_text, False) is False:
        # 如果没有,则遍历找满足相似度阈值的
        max_similarity = 0
        res_node = None
        for candidate_ck_eles_text in screen_map.keys():
            cur_similarity = get_text_similarity(ck_eles_text, candidate_ck_eles_text)
            if cur_similarity >= Config.get_instance().screen_similarity_threshold:
                if cur_similarity > max_similarity:
                    max_similarity = cur_similarity
                    res_node = screen_map.get(candidate_ck_eles_text)
        # 返回的要么是None, 要么是相似性最大的screen_node
        return max_similarity, res_node

    # 说明该节点之前存在screen_map
    else:
        return 1.0, screen_map.get(ck_eles_text)


def get_max_sim_from_screen_depth_map(ck_eles_text: str) -> tuple[float | int]:
    screen_depth_map = RuntimeContent.get_instance().screen_depth_map
    if screen_depth_map.get(ck_eles_text, False) is False:
        max_sim = 0
        res_depth = Config.get_instance().UndefineDepth
        for candidate_ck_eles_text in screen_depth_map.keys():
            cur_sim = get_text_similarity(ck_eles_text, candidate_ck_eles_text)
            if cur_sim >= Config.get_instance().screen_similarity_threshold:
                if cur_sim > max_sim:
                    max_sim = cur_sim
                    res_depth = screen_depth_map.get(candidate_ck_eles_text)
        return max_sim, res_depth
    return 1.0, screen_depth_map.get(ck_eles_text)


def get_screennode_from_screenmap_by_similarity(ck_eles_text: str) -> ScreenNode:
    screen_map = RuntimeContent.get_instance().get_screen_map()
    if screen_map.get(ck_eles_text, False) is False:
        # 如果没有,则遍历找满足相似度阈值的
        max_similarity = 0
        res_node = None
        for candidate_ck_eles_text in screen_map.keys():
            cur_similarity = get_text_similarity(ck_eles_text, candidate_ck_eles_text)
            if cur_similarity >= Config.get_instance().screen_similarity_threshold:
                if cur_similarity > max_similarity:
                    max_similarity = cur_similarity
                    res_node = screen_map.get(candidate_ck_eles_text)
        # 返回的要么是None, 要么是相似性最大的screen_node
        return res_node

    # 说明该节点之前存在screen_map
    else:
        return screen_map.get(ck_eles_text)


def get_text_similarity(text1: str, text2: str) -> float:
    screen_compare_strategy = ScreenCompareStrategy(LCSComparator())
    return screen_compare_strategy.compare_screen(text1, text2)


def is_text_similar(text1: str, text2: str) -> bool:
    screen_compare_strategy = ScreenCompareStrategy(LCSComparator())
    sim = screen_compare_strategy.compare_screen(text1, text2)
    if sim >= Config.get_instance().screen_similarity_threshold:
        return True
    return False
