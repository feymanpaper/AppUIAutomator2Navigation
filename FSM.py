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
 

def get_state():
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)
    if cur_screen_pkg_name != target_pkg_name:
        if cur_screen_pkg_name == "com.google.android.apps.nexuslauncher":
            return 5
        else:
            return 1
    
    if d(packageName = "com.google.android.inputmethod.latin").exists():
       return 2
    
    cur_screen_node = get_screennode_from_screenmap(screen_map, cur_screen_all_text, screen_compare_strategy)
    if cur_screen_node is not None:
        return 3
    else:
        return 4

def print_state(state_map, state):
    print(f"状态为{state} {state_map[state]}")
   
def do_transition(state):
    if state == 1:
        handle_exit_app()
    elif state == 2:
        handle_inputmethod()
    elif state == 3:
        handle_exist_screen()
    elif state == 4:
        handle_new_screen()
    else:
        raise Exception

def handle_exit_app():
    press_back()

def handle_inputmethod():
    press_back()

def build_screen_call_graph():
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)
    # 初始化cur_screen_node信息
    cur_screen_node = ScreenNode()
    cur_screen_node.info = cur_screen_info
    # cur_screen_node.sig = cur_screen_sig
    cur_screen_node.all_text = cur_screen_all_text
    cur_screen_node.pkg_name = cur_screen_pkg_name
    cur_screen_node.activity_name = cur_activity
    clickable_eles, res_merged_diff = get_merged_clickable_elements(d, ele_uuid_map, cur_activity)
    cur_screen_node.merged_diff = res_merged_diff
    cur_screen_node.clickable_elements = clickable_eles
    # 将cur_screen加入到全局记录的screen_map
    screen_map[cur_screen_all_text] = cur_screen_node
    # 将cur_screen加入到last_screen的子节点
    # last_screen_node = screen_map.get(last_screen_all_text)
    last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text, screen_compare_strategy)
    last_screen_node.add_child(cur_screen_node)

    stat_activity_set.add(cur_activity) #统计结果用
    stat_screen_set.add(cur_screen_all_text) #统计结果用
    return cur_screen_node

def print_screen_info(cur_screen_node, is_new):
    print("*"*100)
    if is_new:
        print(f"该screen为新: {cur_screen_node.all_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
    else:
        print(f"该screen已存在: {cur_screen_node.all_text[0:-1]}--总共{len(cur_screen_node.clickable_elements)}, 减少{cur_screen_node.merged_diff}")
    print("*"*100)


def handle_new_screen():
    cur_screen_node = build_screen_call_graph()
    print_screen_info(cur_screen_node, True)
    click_one_ele(cur_screen_node)


def handle_exist_screen():
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)
    cur_screen_node = get_screennode_from_screenmap(screen_map, cur_screen_all_text, screen_compare_strategy)
    print_screen_info(cur_screen_node, False)
    if cur_screen_node.is_screen_clickable_finished():
        press_back()
    else:
        click_one_ele(cur_screen_node)


def click_one_ele(cur_screen_node):
    # 遍历cur_screen的所有可点击组件
    cur_screen_node_clickable_eles = cur_screen_node.clickable_elements
    cur_screen_pkg_name, cur_activity, cur_screen_all_text, cur_screen_info = get_screen_info(d)

    global last_activity
    global last_clickable_ele
    global last_screen_all_text
    global total_eles_cnt

    global first_activity
    global first_screen_text

    last_screen_node = get_screennode_from_screenmap(screen_map, last_screen_all_text, screen_compare_strategy)
    if check_cycle(cur_screen_node, last_screen_node, screen_compare_strategy) == True:
        #产生了回边
        pass
    else:
        if last_screen_all_text != "root":
            # last_clickale_ele_uuid = get_uuid(last_clickable_ele, d, umap, last_activity)
            last_clickale_ele_uuid = get_unique_id(d, last_clickable_ele, last_activity)
            last_screen_node.call_map[last_clickale_ele_uuid] = cur_screen_all_text
        else:
            first_activity = cur_activity
            first_screen_text = cur_screen_all_text

    

    clickable_ele_idx = 0
    while clickable_ele_idx < len(cur_screen_node_clickable_eles):
        cur_clickable_ele = cur_screen_node_clickable_eles[clickable_ele_idx]
    # for clickable_ele_idx, cur_clickable_ele in enumerate(cur_screen_node_clickable_eles):

        #--------------------------------------
        #判断当前组件是否需要访问
        #1.如果没访问过，即vis_map[uuid]=False，就直接访问
        #2.如果访问过了，即vis_map[uuid]=True,还得判断该组件是否是
        #当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
        #的所有组件是否访问完毕

        # 表示该组件已经访问过
        # +1是因为下标从0开始
        cur_screen_node.already_clicked_cnt = clickable_ele_idx + 1
        # uuid = get_uuid(cur_clickable_ele, d, umap, cur_activity)
        uuid = get_unique_id(d, cur_clickable_ele, cur_activity)
     
        if is_non_necessary_click(cur_clickable_ele):
            ele_vis_map[uuid] = True
            print(f"省略组件&{clickable_ele_idx}: {uuid}")
            clickable_ele_idx +=1
            continue

        if ele_vis_map.get(uuid, False) == False:
            # 拿到该组件的坐标x, y
            loc_x, loc_y = get_location(cur_clickable_ele)
            ele_vis_map[uuid] = True
            #点击该组件
            print(f"正常点击组件&{clickable_ele_idx}: {uuid}")
            total_eles_cnt +=1 #统计的组件点击次数+1
            last_screen_all_text = cur_screen_all_text
            last_clickable_ele = cur_clickable_ele
            last_activity = cur_activity
            d.click(loc_x, loc_y)
            time.sleep(sleep_time_sec)
            return 

        else:
            if cur_screen_node.call_map.get(uuid, None) is not None:
                target_screen_all_text = cur_screen_node.call_map.get(uuid)
                if cur_screen_node.is_all_children_finish(target_screen_all_text, screen_compare_strategy) == False:
                    # click_map指示存在部分没完成
                    loc_x, loc_y = get_location(cur_clickable_ele)
    
                    print(f"clickmap没完成点击组件&{clickable_ele_idx}: {uuid}")
                    total_eles_cnt +=1 #统计的组件点击次数+1
                    
                    last_screen_all_text = cur_screen_all_text
                    last_clickable_ele = cur_clickable_ele
                    last_activity = cur_activity

                    d.click(loc_x, loc_y) 
                    time.sleep(sleep_time_sec)
                    return 
                
                else:
                    print(f"clickmap--该界面点击完成&{clickable_ele_idx}: {uuid}")
            else:
                print(f"已点击过&{clickable_ele_idx}: {uuid}")

        clickable_ele_idx +=1
        

def press_back():
    d.press("back")
    time.sleep(sleep_time_sec)
    return

def FSM():
    
    # state
    # 1: 不是当前要测试的app,即app跳出了测试的app
    # 2: 发现当前界面有文本输入法框
    # 3: 当前Screen已经存在
    # 4: 当前Screen不存在 
    state = -1
    state_map = {
        1: "不是当前要测试的app,即app跳出了测试的app",
        2: "发现当前界面有文本输入法框",
        3: "当前Screen已经存在",
        4: "当前Screen不存在"
    }
 
    while True:
        state = get_state()
        print()
        print("-"*50)
        print_state(state_map, state)
        do_transition(state)
        print("-"*50)
        print()



if __name__ == "__main__":
    # try:
    #     testTimeOut()
    # except Exception as e:
    #     print(1)
    # 存储着整个app所有screen(ScrennNode) {key:screen_sig, val:screen_node}
    screen_map = {}
    # 全局记录每个组件的uuid {key:uuid, val:clickable_ele}
    ele_uuid_map = {}
    # 全局记录组件是否有被点击过 {key:uuid, val:true/false}
    ele_vis_map = {}

    sleep_time_sec = 5
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
    target_pkg_name = "com.alibaba.android.rimet"
    # target_pkg_name = "com.ss.android.lark"
    # target_pkg_name = "com.cloudy.component"
    # target_pkg_name = "com.jingyao.easybike"

    # 第一个activity
    first_activity = None
    first_screen_text = None

    root = ScreenNode()
    root.all_text = "root"
    screen_map["root"] = root

    last_screen_all_text = root.all_text
    last_clickable_ele = None
    last_activity = None

    d.app_start(target_pkg_name)
    time.sleep(sleep_time_sec)

    try:
        FSM()
    except Exception as e:
        print("@"*100)
        print("@"*100)
        print(f"总共点击的activity个数 {len(stat_activity_set)}")
        print(f"总共点击的Screen个数: {len(stat_screen_set)}")
        print(f"总共点击的组件个数: {total_eles_cnt}")