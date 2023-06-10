from uiautomator2 import Device
from JsonHelper import *
from StateHandler import *
from RuntimeContent import *
from DeviceHelper import *
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



def do_transition(state, content):
    if state == 1:
        StateHandler.handle_exit_app(content)
    elif state == 2:
        StateHandler.handle_inputmethod(content)
    elif state == 3:
        StateHandler.handle_exist_screen(content)
    elif state == 4:
        StateHandler.handle_exit_screen(content)
    elif state == 5:
        StateHandler.handle_new_screen(content)
    elif state == 6:
        StateHandler.handle_special_screen(content)
    elif state == 7:
        # TODO 重启机制
        StateHandler.handle_restart(content)
    elif state == 8:
        StateHandler.handle_double_press(content)
    elif state == 9:
        StateHandler.handle_system_permission_screen(content)
    elif state == 10:
        StateHandler.handle_outsystem_special_screen(content)
    elif state == 11:
        StateHandler.handle_WebView_screen(content)
    elif state == 12:
        StateHandler.handle_error_screen(content)
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

    if check_is_in_webview(cur_activity) and check_pattern_state(4, [8, 11]):
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

        if check_is_errorscreen(cur_screen_all_text, screen_compare_strategy) and check_pattern_state(4, [12, 8]):
            return 7, content
        if check_is_errorscreen(cur_screen_all_text, screen_compare_strategy) and check_pattern_state(1, [12]) and check_screen_list_reverse(2):
            return 8, content
        if check_is_errorscreen(cur_screen_all_text, screen_compare_strategy):
            return 12, content

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

    screen_compare_strategy = ScreenCompareStrategy(LCSComparator())
    default_screen_compare_strategy = ScreenCompareStrategy(LCSComparator(0.5))

    root = ScreenNode()
    root.all_text = "root"
    RuntimeContent.get_instance().set_last_screen_node(root)
    RuntimeContent.get_instance().put_screen_map("root", root)

    suppress_keyboard_interrupt_message()
    # 计时开始
    StatRecorder.get_instance().set_start_time()

    restart_cnt = 0
    while True:
        ## 启动app
        d = RuntimeContent.get_instance().get_device()
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
    StatRecorder.get_instance().print_result()

