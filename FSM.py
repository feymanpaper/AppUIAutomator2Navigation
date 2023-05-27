from uiautomator2 import Device
from utils import *
from ScreenNode import *
from ScreenCompareStrategy import *
import signal
import time
from RestartException import RestartException
from StatRecorder import *
from core_functions import *
from StateChecker import *
from DeviceHelper import *
from JsonHelper import *
from Config import *
from StateHandler import *
from RuntimeContent import *
import random
import logging
import sys


def suppress_keyboard_interrupt_message():
    old_excepthook = sys.excepthook

    def new_hook(exctype, value, traceback):
        if exctype != KeyboardInterrupt:
            old_excepthook(exctype, value, traceback)
        else:
            print('\nKeyboardInterrupt ...')
            print('do something after Interrupt ...')
            StatRecorder.get_instance().print_result()
            file_name = Config.get_instance().get_target_pkg_name() + "_" + "interupt"
            dump_screen_map_to_json(file_name)
    sys.excepthook = new_hook


def handle_exit_app(content):
    press_back()

def handle_double_press(content):
    double_press_back()
def handle_inputmethod(content):
    press_back()

def handle_WebView_screen(content):
    press_back()

def handle_exit_screen(content):
    press_back()

def handle_restart(content):
    RuntimeContent.get_instance().append_error_screen_list(content["cur_screen_all_text"])
    RuntimeContent.get_instance().append_error_clickable_ele_uid_list(last_clickable_ele_uid)
    raise RestartException("重启机制")

def handle_system_permission_screen(content):
    cur_screen_node = add_new_screen_call_graph(content)
    content["cur_screen_node"] = cur_screen_node
    RuntimeContent.get_instance().append_screen_list(content["cur_screen_all_text"])
    print_screen_info(content, False)
    random_click_one_ele(content)

def handle_special_screen(content):
    cur_screen_node = add_exist_screen_call_graph(content)
    print_screen_info(content, False)
    random_click_one_ele(content)

def handle_outsystem_special_screen(content):
    cur_screen_node = add_new_screen_call_graph(content)
    content["cur_screen_node"] = cur_screen_node
    print_screen_info(content, True)
    random_click_one_ele(content)

def handle_new_screen(content):
    cur_screen_node = add_new_screen_call_graph(content)
    content["cur_screen_node"] = cur_screen_node
    print_screen_info(content, True)
    click_one_ele(content)

def handle_exist_screen(content):
    cur_screen_node = add_exist_screen_call_graph(content)
    print_screen_info(content, False)
    click_one_ele(content)

def get_permission_screen_node(content):
    cur_screen_pkg_name, cur_activity, cur_screen_all_text = get_screen_info_from_context(content)
    cur_screen_node = ScreenNode()
    # cur_screen_node.info = cur_screen_info
    cur_screen_node.pkg_name = cur_screen_pkg_name
    cur_screen_node.activity_name = cur_activity
    clickable_eles, res_merged_diff = get_merged_clickable_elements(d, cur_activity)
    cur_screen_node.merged_diff = res_merged_diff
    cur_screen_node.clickable_elements = clickable_eles
    cur_screen_node.all_text = cur_screen_all_text
    return cur_screen_node

def add_new_screen_call_graph(content):
    cur_screen_pkg_name, cur_activity, cur_screen_all_text = get_screen_info_from_context(content)
    last_screen_node = get_screennode_from_screenmap_by_similarity(last_screen_all_text, screen_compare_strategy)
    # screen_map[last_screen_all_text] = last_screen_node

    # 初始化cur_screen_node信息
    cur_screen_node = ScreenNode()
    # cur_screen_node.info = cur_screen_info
    # cur_screen_node.sig = cur_screen_sig
    cur_screen_node.pkg_name = cur_screen_pkg_name
    cur_screen_node.activity_name = cur_activity
    clickable_eles, res_merged_diff = get_merged_clickable_elements(d, cur_activity)
    last_clickable_elements = last_screen_node.get_exactly_clickable_eles()

    sim = content["sim"]
    most_similar_screen_node = content["most_similar_screen_node"]
    if sim >= 0.70:
    # TODO
        most_sim_clickable_elements = most_similar_screen_node.get_exactly_clickable_eles()
        diff_list = get_two_clickable_eles_diff(clickable_eles, most_sim_clickable_elements)
        cur_screen_node.diff_clickable_elements = diff_list
    #     cur_screen_node.merged_diff = res_merged_diff
    #     cur_screen_node.clickable_elements = clickable_eles
    #     # diff_text = get_screen_all_text_from_dict(diff_list, ele_uid_map)
    #     # cur_screen_all_text = diff_text
    #     cur_screen_node.all_text = cur_screen_all_text
    #     screen_map[cur_screen_all_text] = cur_screen_node
    # else:
    cur_screen_node.merged_diff = res_merged_diff
    cur_screen_node.clickable_elements = clickable_eles
    cur_screen_node.all_text = cur_screen_all_text

    # 将cur_screen加入到全局记录的screen_map
    RuntimeContent.get_instance().put_screen_map(cur_screen_all_text, cur_screen_node)
    # 将cur_screen加入到last_screen的子节点
    last_screen_node.add_child(cur_screen_node)
    return cur_screen_node
def add_exist_screen_call_graph(content):
    # cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)
    cur_screen_pkg_name, cur_activity, cur_screen_all_text = get_screen_info_from_context(content)
    cur_screen_node = get_cur_screen_node_from_context(content)
    # 将cur_screen加入到last_screen的子节点
    last_screen_node = get_screennode_from_screenmap_by_similarity(last_screen_all_text, screen_compare_strategy)
    # screen_map[last_screen_all_text] = last_screen_node

    last_screen_node.add_child(cur_screen_node)
    return cur_screen_node


def random_click_one_ele(content):
    # TODO
    print("可能产生了不可去掉的框")
    cur_screen_node = get_cur_screen_node_from_context(content)

    cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()
    cur_screen_pkg_name, cur_activity, cur_screen_all_text = get_screen_info_from_context(content)

    global last_activity
    global last_clickable_ele_uid
    global last_screen_all_text
    global first_activity
    global first_screen_text
    # last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text, screen_compare_strategy)
    # if check_cycle(cur_screen_node, last_screen_node, screen_compare_strategy) == True:
    #     # 产生了回边
    #     print("产生回边")
    #     pass
    # else:
    #     if last_screen_all_text != "root":
    #         # last_clickale_ele_uid = get_uid(last_clickable_ele, d, umap, last_activity)
    #         # last_clickale_ele_uid = get_unique_id(d, last_clickable_ele, last_activity)
    #         last_screen_node.call_map[last_clickable_ele_uid] = cur_screen_node
    #     else:
    #         first_activity = cur_activity
    #         first_screen_text = cur_screen_all_text
    #TODO
    candidate = None
    if cur_screen_node.candidate_random_clickable_eles is None or len(cur_screen_node.candidate_random_clickable_eles) == 0:
        candidate = cur_screen_node.build_candidate_random_clickable_eles()
    else:
        candidate = cur_screen_node.candidate_random_clickable_eles

    if candidate is None or len(candidate) == 0:
        return

    # choose = random.randint(0, len(cur_screen_node_clickable_eles) - 1)
    # cur_clickable_ele_uid = cur_screen_node_clickable_eles[choose]
    choose = random.randint(0, len(cur_screen_node.candidate_random_clickable_eles) - 1)
    cur_clickable_ele_uid = cur_screen_node.candidate_random_clickable_eles[choose]
    cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
    loc_x, loc_y = get_location(cur_clickable_ele_dict)
    cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
    # 点击该组件
    print(f"随机点击组件&{choose}: {cur_clickable_ele_uid}")
    StatRecorder.get_instance().inc_total_ele_cnt()
    last_screen_all_text = cur_screen_all_text
    last_clickable_ele_uid = cur_clickable_ele_uid
    last_activity = cur_activity
    d.click(loc_x, loc_y)
    time.sleep(Config.get_instance().get_sleep_time_sec())

def click_one_ele(content):
    # 遍历cur_screen的所有可点击组件
    cur_screen_node = get_cur_screen_node_from_context(content)
    cur_screen_pkg_name, cur_activity, cur_screen_all_text = get_screen_info_from_context(content)

    cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()

    global last_activity
    global last_clickable_ele_uid
    global last_screen_all_text

    global first_activity
    global first_screen_text

    last_screen_node = get_screennode_from_screenmap_by_similarity(last_screen_all_text, screen_compare_strategy)
    # screen_map[last_screen_all_text] = last_screen_node
    # last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text)
    if last_screen_node.all_text == cur_screen_node.all_text:
        print("回到自己")
        last_screen_node.update_callmap_item(last_clickable_ele_uid)
        pass
    elif check_cycle(cur_screen_node, last_screen_node, screen_compare_strategy) == True:
        #产生了回边
        last_screen_node.cycle_set.add(last_clickable_ele_uid)
        print("产生回边")
        last_screen_node.update_callmap_item(last_clickable_ele_uid)
        pass
    else:
        if last_screen_all_text != "root":
            # last_clickale_ele_uid = get_uid(last_clickable_ele, d, umap, last_activity)
            # last_clickale_ele_uid = get_unique_id(d, last_clickable_ele, last_activity)

            #call_map会更新
            last_screen_node.call_map[last_clickable_ele_uid] = cur_screen_node
        else:
            first_activity = cur_activity
            first_screen_text = cur_screen_all_text

    

    clickable_ele_idx = cur_screen_node.already_clicked_cnt
    while clickable_ele_idx < len(cur_screen_node_clickable_eles):
        cur_clickable_ele_uid = cur_screen_node_clickable_eles[clickable_ele_idx]

        # TODO 仅调试使用
        # if clickable_ele_idx <= 0:
        #     cur_screen_node.already_clicked_cnt += 1
        #     clickable_ele_idx+=1
        #     continue
        cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)

        loc_x, loc_y = get_location(cur_clickable_ele_dict)
        if loc_x >=60 and loc_x <= 70 and loc_y == 162:
            cur_screen_node.already_clicked_cnt += 1
            clickable_ele_idx+=1
            continue
        if loc_x >= 998 and loc_x <= 1010 and loc_y >= 155 and loc_y <= 165:
            cur_screen_node.already_clicked_cnt += 1
            clickable_ele_idx += 1
            continue

    # for clickable_ele_idx, cur_clickable_ele_uid in enumerate(cur_screen_node_clickable_eles):
        #--------------------------------------
        #判断当前组件是否需要访问
        #1.如果没访问过，即vis_map[uid]=False，就直接访问
        #2.如果访问过了，即vis_map[uid]=True,还得判断该组件是否是
        #当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
        #的所有组件是否访问完毕

        # 表示该组件已经访问过
        # +1是因为下标从0开始
        # cur_screen_node.already_clicked_cnt = clickable_ele_idx + 1
        # uid = get_uid(cur_clickable_ele, d, umap, cur_activity)
        cur_screen_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
        if is_non_necessary_click(cur_screen_ele_dict):
            cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
            if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
            else:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1
            print(f"省略组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            clickable_ele_idx +=1
            cur_screen_node.already_clicked_cnt += 1
            continue

        if cur_screen_node.ele_vis_map.get(cur_clickable_ele_uid, False) == False:
            # 拿到该组件的坐标x, y
            cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
            loc_x, loc_y = get_location(cur_clickable_ele_dict)
            cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
            #点击该组件
            print(f"正常点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            StatRecorder.get_instance().inc_total_ele_cnt()
            last_screen_all_text = cur_screen_all_text
            last_clickable_ele_uid = cur_clickable_ele_uid
            last_activity = cur_activity

            if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
            else:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

            d.click(loc_x, loc_y)
            time.sleep(Config.get_instance().get_sleep_time_sec())
            return 

        else:
            # if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) is not None and cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) > Config.get_instance().get_CLICK_MAX_CNT():
            #     print(f"该组件点击次数过多不点了&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            #     cur_screen_node.already_clicked_cnt += 1
            #     clickable_ele_idx += 1
            if cur_screen_node.call_map.get(cur_clickable_ele_uid, None) is not None:
                target_screen_node = cur_screen_node.call_map.get(cur_clickable_ele_uid, None)
                target_screen_all_text = target_screen_node.all_text

                if check_is_error_clickable_ele(cur_clickable_ele_uid) == True:
                    print(f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    cur_screen_node.already_clicked_cnt += 1
                    clickable_ele_idx += 1
                    continue

                if check_is_errorscreen(target_screen_all_text, screen_compare_strategy) == True:
                    print(f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    cur_screen_node.already_clicked_cnt += 1
                    clickable_ele_idx += 1
                    continue
                if cur_screen_node.is_cur_callmap_finish(target_screen_all_text, screen_compare_strategy) == False:
                    # click_map指示存在部分没完成
                    cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
                    loc_x, loc_y = get_location(cur_clickable_ele_dict)
                    print(f"clickmap没完成点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    StatRecorder.get_instance().inc_total_ele_cnt()
                    
                    last_screen_all_text = cur_screen_all_text
                    last_clickable_ele_uid = cur_clickable_ele_uid
                    last_activity = cur_activity

                    if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                        cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 0
                    else:
                        cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

                    d.click(loc_x, loc_y) 
                    time.sleep(Config.get_instance().get_sleep_time_sec())
                    return 
                
                else:
                    print(f"clickmap--该界面点击完成&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    cur_screen_node.already_clicked_cnt += 1
                    clickable_ele_idx += 1
            else:
                print(f"已点击过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                cur_screen_node.already_clicked_cnt += 1
                clickable_ele_idx += 1

        # clickable_ele_idx +=1
        

def press_back():
    d.press("back")
    print("进行回退")
    time.sleep(Config.get_instance().get_sleep_time_sec())
    return

def double_press_back():
    d.press("back")
    d.press("back")
    time.sleep(Config.get_instance().get_sleep_time_sec())
    return



def do_transition(state, content):
    if state == 1:
        handle_exit_app(content)
    elif state == 2:
        handle_inputmethod(content)
    elif state == 3:
        handle_exist_screen(content)
    elif state == 4:
        handle_exit_screen(content)
    elif state == 5:
        handle_new_screen(content)
    elif state == 6:
        handle_special_screen(content)
    elif state == 7:
        # TODO 重启机制
        handle_restart(content)
    elif state == 8:
        handle_double_press(content)
    elif state == 9:
        handle_system_permission_screen(content)
    elif state == 10:
        handle_outsystem_special_screen(content)
    elif state == 11:
        handle_WebView_screen(content)
    else:
        raise Exception("意外情况")

def get_state():
    cur_screen_pkg_name, cur_activity, cur_screen_all_text = get_screen_info(d)
    StatRecorder.get_instance().add_stat_stat_activity_set(cur_activity)
    StatRecorder.get_instance().add_stat_screen_set(cur_screen_all_text)

    content = {}
    content["cur_screen_pkg_name"] = cur_screen_pkg_name
    content["cur_activity"] = cur_activity
    content["cur_screen_all_text"] = cur_screen_all_text
    if cur_screen_pkg_name != Config.get_instance().get_target_pkg_name():
        if check_is_in_home_screen(cur_screen_pkg_name):
            return 100, content
        elif cur_screen_pkg_name == "com.google.android.packageinstaller":
            return 9, content
        else:
            if check_pattern_state(3, [1]):
                return 10, content
            else:
                return 1, content

    if check_is_inputmethod_in_cur_screen(d) == True:
        return 2, content

    if check_is_in_webview(cur_activity) and check_pattern_state(5, [8, 11]):
        return 7, content
    if check_is_in_webview(cur_activity) and check_pattern_state(1, [11]):
        return 8, content
    if check_is_in_webview(cur_activity):
        return 11, content
    # temp_screen_node = get_screennode_from_screenmap_by_similarity(screen_map, cur_screen_all_text, screen_compare_strategy)
    # if temp_screen_node is not None and len(temp_screen_node.clickable_elements) == clickable_cnt:
    #     cur_screen_node = temp_screen_node
    # else:
    #     cur_screen_node = None
    sim, most_similar_screen_node = get_max_similarity_screen_node(cur_screen_all_text, default_screen_compare_strategy)
    content["cur_screen_node"] = most_similar_screen_node
    content["most_similar_screen_node"] = most_similar_screen_node
    content["sim"] = sim
    RuntimeContent.get_instance().append_screen_list(cur_screen_all_text)

    # if cur_screen_node is not None:
    if sim >= 0.90:
        cur_screen_node = most_similar_screen_node
        RuntimeContent.get_instance().put_screen_map(cur_screen_all_text, cur_screen_node)
        if check_is_errorscreen(cur_screen_all_text, screen_compare_strategy):
            return 4, content
        # TODO k为6,表示出现了连续6个以上的pattern,且所有组件已经点击完毕,避免一些情况:页面有很多组件点了没反应,这个时候应该继续点而不是随机点
        # if check_state_list_reverse(1, state_list, 4) and check_screen_list_reverse(10, screen_list) and cur_screen_node.is_screen_clickable_finished():
        #     return 7, content
        if cur_screen_node.is_screen_clickable_finished() and check_pattern_state(10, [4, 6, 8]):
            return 7, content
        if cur_screen_node.is_screen_clickable_finished() and check_pattern_state(1, [6,
                                                                                      8]) and check_screen_list_reverse(3):
            return 6, content
        if cur_screen_node.is_screen_clickable_finished() and check_pattern_state(1,
                                                                                  [4]) and check_screen_list_reverse(2):
            return 8, content
        # 4说明已经点完, press_back
        if cur_screen_node.is_screen_clickable_finished():
            return 4, content
        # 3说明未点完, 触发点一个组件
        else:
            return 3, content
    else:
        # 放到后面建立完成之后在添加
        # screen_map[cur_screen_all_text] = cur_screen_node
        return 5, content


def FSM():
    
    # state
    # 1: 不是当前要测试的app,即app跳出了测试的app
    # 2: 发现当前界面有文本输入法框
    # 3: 当前Screen已经存在
    # 4: 当前Screen不存在

    stat_map = {}
    state = -1
    while True:
        if len(StatRecorder.get_instance().get_stat_screen_set()) % 10 == 0 and stat_map.get(len(StatRecorder.get_instance().get_stat_screen_set()), False) is False:
            stat_map[len(StatRecorder.get_instance().get_stat_screen_set())] = True
            StatRecorder.get_instance().print_result()

        state, content = get_state()
        RuntimeContent.get_instance().append_state_list(state)
        print()
        print("-"*50)
        StateHandler.print_state(state)
        do_transition(state, content)
        print("-"*50)
        print()



if __name__ == "__main__":

    d = Device()
    screen_compare_strategy = ScreenCompareStrategy(LCSComparator())
    default_screen_compare_strategy = ScreenCompareStrategy(LCSComparator(0.5))

    # 第一个activity
    first_activity = None
    first_screen_text = None
    root = ScreenNode()
    root.all_text = "root"
    RuntimeContent.get_instance().put_screen_map("root", root)
    last_screen_all_text = root.all_text
    cur_clickable_ele_uid = None
    last_activity = None
    last_clickable_ele_uid = None

    suppress_keyboard_interrupt_message()
    # 计时开始
    StatRecorder.get_instance().set_start_time()

    restart_cnt = 0
    while True:
        ## 启动app
        d.app_start(Config.get_instance().get_target_pkg_name(), use_monkey=True)
        time.sleep(10)
        try:
            FSM()
        except RestartException as e:
            restart_cnt += 1
            print("需要重启")
            logging.exception(e)
            StatRecorder.get_instance().print_result()
            file_name = Config.get_instance().get_target_pkg_name() + "_" + str(restart_cnt)
            dump_screen_map_to_json(file_name)
            RuntimeContent.get_instance().clear_state_list()
            RuntimeContent.get_instance().clear_screen_list()
            d.app_stop(Config.get_instance().get_target_pkg_name())
            time.sleep(10)
        except Exception as e:
            break

    print("程序结束")

