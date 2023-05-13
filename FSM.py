# cur_activity
# for....所有能点击的组件:
#   click()
# 否则当前没东西可点了，back ，不写成dfs
from utils import *
from Screen import *
from ScreenCompareStrategy import *
import time
import signal
from core_functions import *
import random
import logging


def handle_exit_app(content):
    press_back()

def handle_double_press(content):
    double_press_back()
def handle_inputmethod(content):
    press_back()

def handle_exit_screen(content):
    press_back()

def handle_system_permission_screen(content):
    cur_screen_node = add_new_screen_call_graph(content)
    content["cur_screen_node"] = cur_screen_node
    screen_list.append(content["cur_screen_all_text"])
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
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info_from_context(content)
    cur_screen_node = ScreenNode()
    cur_screen_node.info = cur_screen_info
    cur_screen_node.pkg_name = cur_screen_pkg_name
    cur_screen_node.activity_name = cur_activity
    clickable_eles, res_merged_diff = get_merged_clickable_elements(d, ele_uid_map, cur_activity)
    cur_screen_node.merged_diff = res_merged_diff
    cur_screen_node.clickable_elements = clickable_eles
    cur_screen_node.all_text = cur_screen_all_text


    stat_activity_set.add(cur_activity)  # 统计结果用
    stat_screen_set.add(cur_screen_all_text)  # 统计结果用
    return cur_screen_node

def add_new_screen_call_graph(content):
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info_from_context(content)
    last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text, screen_compare_strategy)

    # 初始化cur_screen_node信息
    cur_screen_node = ScreenNode()
    cur_screen_node.info = cur_screen_info
    # cur_screen_node.sig = cur_screen_sig
    cur_screen_node.pkg_name = cur_screen_pkg_name
    cur_screen_node.activity_name = cur_activity
    clickable_eles, res_merged_diff = get_merged_clickable_elements(d, ele_uid_map, cur_activity)
    last_clickable_elements = last_screen_node.clickable_elements
    # TODO
    is_overlap, diff_list = get_two_clickable_eles_diff(clickable_eles, cur_activity, last_clickable_elements, last_activity)
    if is_overlap is True:
        cur_screen_node.merged_diff = res_merged_diff
        cur_screen_node.clickable_elements = diff_list
        # diff_text = get_screen_all_text_from_dict(diff_list, ele_uid_map)
        # cur_screen_all_text = diff_text
        cur_screen_node.all_text = cur_screen_all_text
        screen_map[cur_screen_all_text] = cur_screen_node
    else:
        cur_screen_node.merged_diff = res_merged_diff
        cur_screen_node.clickable_elements = clickable_eles
        cur_screen_node.all_text = cur_screen_all_text
        screen_map[cur_screen_all_text] = cur_screen_node

    # 将cur_screen加入到全局记录的screen_map

    # 将cur_screen加入到last_screen的子节点
    # last_screen_node = screen_map.get(last_screen_all_text)

    last_screen_node.add_child(cur_screen_node)
    stat_activity_set.add(cur_activity) #统计结果用
    stat_screen_set.add(cur_screen_all_text) #统计结果用
    return cur_screen_node
def add_exist_screen_call_graph(content):
    # cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info_from_context(content)
    # cur_screen_node = get_screennode_from_screenmap(screen_map, cur_screen_all_text, screen_compare_strategy)
    cur_screen_node = get_cur_screen_node_from_context(content)
    # 将cur_screen加入到last_screen的子节点
    # last_screen_node = screen_map.get(last_screen_all_text)
    last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text, screen_compare_strategy)

    last_screen_node.add_child(cur_screen_node)
    return cur_screen_node


def random_click_one_ele(content):
    # TODO
    print("可能产生了不可去掉的框")
    cur_screen_node = get_cur_screen_node_from_context(content)
    cur_screen_node_clickable_eles = cur_screen_node.clickable_elements
    # cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)

    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info_from_context(content)

    # screen_list.append(cur_screen_all_text)

    global last_activity
    global last_clickable_ele_uid
    global last_screen_all_text
    global total_eles_cnt
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

    choose = random.randint(0, len(cur_screen_node_clickable_eles) - 1)
    cur_clickable_ele_uid = cur_screen_node_clickable_eles[choose]

    cur_clickable_ele_dict = ele_uid_map[cur_clickable_ele_uid]
    loc_x, loc_y = get_location(cur_clickable_ele_dict)
    cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
    # 点击该组件
    print(f"随机点击组件&{choose}: {cur_clickable_ele_uid}")
    total_eles_cnt += 1  # 统计的组件点击次数+1
    last_screen_all_text = cur_screen_all_text
    last_clickable_ele_uid = cur_clickable_ele_uid
    last_activity = cur_activity
    d.click(loc_x, loc_y)
    time.sleep(sleep_time_sec)

def click_one_ele(content):
    # 遍历cur_screen的所有可点击组件
    cur_screen_node = get_cur_screen_node_from_context(content)
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info_from_context(content)
    cur_screen_node_clickable_eles = cur_screen_node.clickable_elements

    # screen_list.append(cur_screen_all_text)
    global last_activity
    global last_clickable_ele_uid
    global last_screen_all_text
    global total_eles_cnt

    global first_activity
    global first_screen_text

    last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text, screen_compare_strategy)
    if check_cycle(cur_screen_node, last_screen_node, screen_compare_strategy) == True:
        #产生了回边
        print("产生回边")
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

    

    clickable_ele_idx = 0
    while clickable_ele_idx < len(cur_screen_node_clickable_eles):
        # TODO 仅调试使用
        # if clickable_ele_idx <= 6:
        #     clickable_ele_idx+=1
        #     continue

        cur_clickable_ele_uid = cur_screen_node_clickable_eles[clickable_ele_idx]
    # for clickable_ele_idx, cur_clickable_ele_uid in enumerate(cur_screen_node_clickable_eles):
        #--------------------------------------
        #判断当前组件是否需要访问
        #1.如果没访问过，即vis_map[uid]=False，就直接访问
        #2.如果访问过了，即vis_map[uid]=True,还得判断该组件是否是
        #当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
        #的所有组件是否访问完毕

        # 表示该组件已经访问过
        # +1是因为下标从0开始
        cur_screen_node.already_clicked_cnt = clickable_ele_idx + 1
        # uid = get_uid(cur_clickable_ele, d, umap, cur_activity)
        cur_screen_ele_dict = ele_uid_map[cur_clickable_ele_uid]
        if is_non_necessary_click(cur_screen_ele_dict):
            cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
            if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
            else:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1
            print(f"省略组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            clickable_ele_idx +=1
            continue

        if cur_screen_node.ele_vis_map.get(cur_clickable_ele_uid, False) == False:
            # 拿到该组件的坐标x, y
            cur_clickable_ele_dict = ele_uid_map[cur_clickable_ele_uid]
            loc_x, loc_y = get_location(cur_clickable_ele_dict)
            cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
            #点击该组件
            print(f"正常点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            total_eles_cnt +=1 #统计的组件点击次数+1
            last_screen_all_text = cur_screen_all_text
            last_clickable_ele_uid = cur_clickable_ele_uid
            last_activity = cur_activity

            if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
            else:
                cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

            d.click(loc_x, loc_y)
            time.sleep(sleep_time_sec)
            return 

        else:
            if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) is not None and cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid) > CLICK_MAX_CNT:
                print(f"该组件点击次数过多不点了&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            elif cur_screen_node.call_map.get(cur_clickable_ele_uid, None) is not None:
                target_screen_node = cur_screen_node.call_map.get(cur_clickable_ele_uid, None)
                target_screen_all_text = target_screen_node.all_text
                if cur_screen_node.is_cur_callmap_finish(target_screen_all_text, screen_compare_strategy) == False:
                    # click_map指示存在部分没完成
                    cur_clickable_ele_dict = ele_uid_map[cur_clickable_ele_uid]
                    loc_x, loc_y = get_location(cur_clickable_ele_dict)
                    print(f"clickmap没完成点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                    total_eles_cnt +=1 #统计的组件点击次数+1
                    
                    last_screen_all_text = cur_screen_all_text
                    last_clickable_ele_uid = cur_clickable_ele_uid
                    last_activity = cur_activity

                    if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                        cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 0
                    else:
                        cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1

                    d.click(loc_x, loc_y) 
                    time.sleep(sleep_time_sec)
                    return 
                
                else:
                    print(f"clickmap--该界面点击完成&{clickable_ele_idx}: {cur_clickable_ele_uid}")
            else:
                print(f"已点击过&{clickable_ele_idx}: {cur_clickable_ele_uid}")

        clickable_ele_idx +=1
        

def press_back():
    d.press("back")
    print("进行回退")
    time.sleep(sleep_time_sec)
    return

def double_press_back():
    d.press("back")
    d.press("back")
    time.sleep(sleep_time_sec)
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
        raise Exception("重启机制???")
    elif state == 8:
        handle_double_press(content)
    elif state == 9:
        handle_system_permission_screen(content)
    elif state == 10:
        handle_outsystem_special_screen(content)
    else:
        raise Exception("意外情况")

def get_state():
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)

    content = {}
    content["cur_screen_pkg_name"] = cur_screen_pkg_name
    content["cur_activity"] = cur_activity
    content["cur_screen_all_text"] = cur_screen_all_text
    content["cur_screen_info"] = cur_screen_info

    if cur_screen_pkg_name != target_pkg_name:
        if check_is_in_home_screen(cur_screen_pkg_name):
            return 100, content
        elif cur_screen_pkg_name == "com.google.android.packageinstaller":
            return 9, content
        else:
            if check_state_list_reverse(3, state_list, 1):
                return 10, content
            else:
                return 1, content

    if check_is_inputmethod_in_cur_screen(d) == True:
        return 2, content

    cur_screen_node = get_screennode_from_screenmap(screen_map, cur_screen_all_text, screen_compare_strategy)
    content["cur_screen_node"] = cur_screen_node
    screen_list.append(cur_screen_all_text)

    if cur_screen_node is not None:
        # TODO k为6,表示出现了连续6个以上的pattern,且所有组件已经点击完毕,避免一些情况:页面有很多组件点了没反应,这个时候应该继续点而不是随机点
        if check_screen_list_reverse(30, screen_list) and cur_screen_node.is_screen_clickable_finished():
            return 7, content
        if check_state_list_reverse(2, state_list, 4) and check_screen_list_reverse(8, screen_list) and cur_screen_node.is_screen_clickable_finished():
            return 6, content
        if check_state_list_reverse(2, state_list, 4) and check_screen_list_reverse(4, screen_list) and cur_screen_node.is_screen_clickable_finished():
            return 8, content
        # 4说明已经点完, press_back
        if cur_screen_node.is_screen_clickable_finished():
            return 4, content
        # 3说明未点完, 触发点一个组件
        else:
            return 3, content
    else:
        return 5, content


def FSM():
    
    # state
    # 1: 不是当前要测试的app,即app跳出了测试的app
    # 2: 发现当前界面有文本输入法框
    # 3: 当前Screen已经存在
    # 4: 当前Screen不存在

    state_map = {
        1: "不是当前要测试的app,即app跳出了测试的app",
        2: "发现当前界面有文本输入法框",
        3: "当前Screen已经存在",
        4: "当前Screen已经点完",
        5: "当前Screen不存在,新建Screen",
        6: "出现了不可回退的框, 启用随机点",
        7: "出现了不可回退的框, 需要重启?",
        8: "出现了不可回退的框, 启用double_press_back",
        9: "出现了系统权限页面",
        10: "出现了系统外不可回退的框"
    }
    state = -1
    stat_map = {}
    while True:
        if len(stat_screen_set) % 10 == 0 and stat_map.get(len(stat_screen_set), False) is False:
            stat_map[len(stat_screen_set)] = True
            print("@"*100)
            print("@"*100)
            print(f"总共点击的activity个数 {len(stat_activity_set)}")
            print(f"总共点击的Screen个数: {len(stat_screen_set)}")
            print(f"总共点击的组件个数: {total_eles_cnt}")
            end_time = time.time()
            print(f"时间为 {end_time - start_time}")

        state, content = get_state()
        state_list.append(state)
        print()
        print("-"*50)
        print_state(state_map, state)
        do_transition(state, content)
        print("-"*50)
        print()



if __name__ == "__main__":
    # try:
    #     testTimeOut()
    # except Exception as e:
    #     print(1)
    # 存储着整个app所有screen(ScrennNode) {key:screen_sig, val:screen_node}
    screen_map = {}

    # 全局记录每个组件的uid {key:cur_clickable_ele_uid, val:clickable_ele}
    ele_uid_map = {}

    CLICK_MAX_CNT = 4
    sleep_time_sec = 4
    # 统计结果用
    total_eles_cnt = 0
    stat_screen_set = set()
    # total_screen_cnt = 0
    stat_activity_set = set()
    # total_activity_cnt = 0
    # 启动app开始执行
    d = Device()
    screen_compare_strategy = ScreenCompareStrategy(LCSComparator())
    # curr_pkg_name = "com.example.myapplication"
    # target_pkg_name = "com.alibaba.android.rimet"
    target_pkg_name = "net.csdn.csdnplus"
    # target_pkg_name = "com.sina.weibo"
    # target_pkg_name = "com.youku.phone"
    # target_pkg_name = "cn.damai"
    # target_pkg_name = "com.ss.android.lark"
    # target_pkg_name = "com.cloudy.component"
    # target_pkg_name = "com.jingyao.easybike"
    # target_pkg_name = "com.cainiao.wireless"
    # target_pkg_name = "com.xingin.xhs"
    # target_pkg_name = "com.yipiao"
    # target_pkg_name = "app.podcast.cosmos"
    screen_list = []
    state_list = []
    # 第一个activity
    first_activity = None
    first_screen_text = None

    root = ScreenNode()
    root.all_text = "root"
    screen_map["root"] = root

    last_screen_all_text = root.all_text
    cur_clickable_ele_uid = None
    last_activity = None

    d.app_start(target_pkg_name)
    time.sleep(sleep_time_sec)

    try:
        start_time = time.time()
        FSM()
    except Exception as e:
        print(e)
        logging.exception(e)
        print("@"*100)
        print("@"*100)
        print(f"总共点击的activity个数 {len(stat_activity_set)}")
        print(f"总共点击的Screen个数: {len(stat_screen_set)}")
        print(f"总共点击的组件个数: {total_eles_cnt}")
        end_time = time.time()
        print(f"时间为 {end_time - start_time}")
    print("end")