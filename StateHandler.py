from RuntimeContent import *
import time
from Config import *
from RestartException import RestartException
from core_functions import *
from DeviceHelper import *
from StatRecorder import *
import random
from StateChecker import *

class StateHandler(object):
    @classmethod
    def click_one_ele(cls,content):
        # 遍历cur_screen的所有可点击组件
        cur_screen_node = get_cur_screen_node_from_context(content)
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()
        last_screen_node = RuntimeContent.get_instance().get_last_screen_node()
        if last_screen_node.ck_eles_text == cur_screen_node.ck_eles_text:
            print("回到自己")
            last_screen_node.update_callmap_item(RuntimeContent.get_instance().get_last_clickable_ele_uid())
            pass
        elif check_cycle(cur_screen_node, last_screen_node, ScreenCompareStrategy(LCSComparator())) == True:
            # 产生了回边
            last_screen_node.cycle_set.add(RuntimeContent.get_instance().get_last_clickable_ele_uid())
            print("产生回边")
            last_screen_node.update_callmap_item(RuntimeContent.get_instance().get_last_clickable_ele_uid())
            pass
        else:
            if last_screen_node.ck_eles_text != "root":
                # call_map会更新
                last_screen_node.call_map[RuntimeContent.get_instance().get_last_clickable_ele_uid()] = cur_screen_node
            # else:
            #     first_screen_text = ck_eles_text

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
            if loc_x >= 60 and loc_x <= 70 and loc_y == 162:
                cur_screen_node.already_clicked_cnt += 1
                clickable_ele_idx += 1
                continue
            if loc_x >= 998 and loc_x <= 1010 and loc_y >= 155 and loc_y <= 165:
                cur_screen_node.already_clicked_cnt += 1
                clickable_ele_idx += 1
                continue

            # for clickable_ele_idx, cur_clickable_ele_uid in enumerate(cur_screen_node_clickable_eles):
            # --------------------------------------
            # 判断当前组件是否需要访问
            # 1.如果没访问过，即vis_map[uid]=False，就直接访问
            # 2.如果访问过了，即vis_map[uid]=True,还得判断该组件是否是
            # 当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
            # 的所有组件是否访问完毕

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
                clickable_ele_idx += 1
                cur_screen_node.already_clicked_cnt += 1
                continue

            if cur_screen_node.ele_vis_map.get(cur_clickable_ele_uid, False) == False:
                # 拿到该组件的坐标x, y
                cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(cur_clickable_ele_uid)
                loc_x, loc_y = get_location(cur_clickable_ele_dict)
                cur_screen_node.ele_vis_map[cur_clickable_ele_uid] = True
                # 点击该组件
                print(f"正常点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                StatRecorder.get_instance().inc_total_ele_cnt()
                RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
                RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

                if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 1
                else:
                    cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1
                d = Config.get_instance().get_device()
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
                    target_screen_all_text = target_screen_node.ck_eles_text

                    if check_is_error_clickable_ele(cur_clickable_ele_uid) == True:
                        print(f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        clickable_ele_idx += 1
                        continue

                    if check_is_errorscreen(target_screen_all_text, ScreenCompareStrategy(LCSComparator())) == True:
                        print(f"该组件会触发error screen因此跳过&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        cur_screen_node.already_clicked_cnt += 1
                        clickable_ele_idx += 1
                        continue
                    if cur_screen_node.is_cur_callmap_finish(target_screen_all_text, ScreenCompareStrategy(LCSComparator())) == False:
                        # click_map指示存在部分没完成
                        cur_clickable_ele_dict = RuntimeContent.get_instance().get_ele_uid_map_by_uid(
                            cur_clickable_ele_uid)
                        loc_x, loc_y = get_location(cur_clickable_ele_dict)
                        print(f"clickmap没完成点击组件&{clickable_ele_idx}: {cur_clickable_ele_uid}")
                        StatRecorder.get_instance().inc_total_ele_cnt()
                        RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
                        RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)

                        if cur_screen_node.ele_uid_cnt_map.get(cur_clickable_ele_uid, None) is None:
                            cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] = 0
                        else:
                            cur_screen_node.ele_uid_cnt_map[cur_clickable_ele_uid] += 1
                        d = Config.get_instance().get_device()
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

    @classmethod
    def get_permission_screen_node(cls, content):
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        screen_text = get_screen_text(content)
        cur_screen_node = ScreenNode()
        # cur_screen_node.info = cur_screen_info
        cur_screen_node.pkg_name = cur_screen_pkg_name
        cur_screen_node.activity_name = cur_activity
        d = Config.get_instance().get_device()
        cur_ck_eles = content["cur_ck_eles"]
        merged_diff = content["merged_diff"]
        cur_screen_node.screen_text = screen_text
        cur_screen_node.clickable_elements = cur_ck_eles
        cur_screen_node.ck_eles_text = ck_eles_text
        cur_screen_node.merged_diff = merged_diff
        return cur_screen_node

    @classmethod
    def add_exist_screen_call_graph(cls, content):
        # cur_screen_pkg_name, cur_activity, ck_eles_text, cur_screen_info = get_screen_info(d)
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        cur_screen_node = get_cur_screen_node_from_context(content)
        # 将cur_screen加入到last_screen的子节点
        last_screen_node = RuntimeContent.get_instance().get_last_screen_node()
        last_screen_node.add_child(cur_screen_node)
        return cur_screen_node

    @classmethod
    def handle_exist_screen(cls, content):
        cur_screen_node = cls.add_exist_screen_call_graph(content)
        print_screen_info(content, False)
        cls.click_one_ele(content)

    @classmethod
    def handle_new_screen(cls, content):
        cur_screen_node = cls.add_new_screen_call_graph(content)
        content["cur_screen_node"] = cur_screen_node
        print_screen_info(content, True)
        cls.click_one_ele(content)

    @classmethod
    def handle_outsystem_special_screen(cls, content):
        cur_screen_node = cls.add_new_screen_call_graph(content)
        content["cur_screen_node"] = cur_screen_node
        print_screen_info(content, True)
        cls.random_click_one_ele(content)
    @classmethod
    def handle_special_screen(cls, content):
        cur_screen_node = cls.add_exist_screen_call_graph(content)
        print_screen_info(content, False)
        cls.random_click_one_ele(content)

    @classmethod
    def handle_system_permission_screen(cls,content):
        cur_screen_node = cls.add_new_screen_call_graph(content)
        content["cur_screen_node"] = cur_screen_node
        RuntimeContent.get_instance().append_screen_list(content["ck_eles_text"])
        print_screen_info(content, False)
        cls.random_click_one_ele(content)

    @classmethod
    def add_new_screen_call_graph(cls, content):
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)
        screen_text = get_screen_text_from_context(content)
        last_screen_node = RuntimeContent.get_instance().get_last_screen_node()
        # 初始化cur_screen_node信息
        cur_screen_node = ScreenNode()
        cur_screen_node.pkg_name = cur_screen_pkg_name
        cur_screen_node.screen_text = screen_text
        cur_screen_node.activity_name = cur_activity
        cur_ck_eles = content["cur_ck_eles"]
        merged_diff = content["merged_diff"]
        last_clickable_elements = last_screen_node.get_exactly_clickable_eles()
        sim = content.get("sim", None)
        most_similar_screen_node = content.get("most_similar_screen_node", None)
        if sim is not None and sim >= 0.70:
            # TODO
            most_sim_clickable_elements = most_similar_screen_node.get_exactly_clickable_eles()
            diff_list = get_two_clickable_eles_diff(cur_ck_eles, most_sim_clickable_elements)
            cur_screen_node.diff_clickable_elements = diff_list
        #     cur_screen_node.clickable_elements = clickable_eles
        #     # diff_text = get_screen_all_text_from_dict(diff_list, ele_uid_map)
        #     # ck_eles_text = diff_text
        #     cur_screen_node.all_text = ck_eles_text
        #     screen_map[ck_eles_text] = cur_screen_node
        # else:
        cur_screen_node.clickable_elements = cur_ck_eles
        cur_screen_node.ck_eles_text = ck_eles_text
        cur_screen_node.merged_diff = merged_diff

        # 将cur_screen加入到全局记录的screen_map
        RuntimeContent.get_instance().put_screen_map(ck_eles_text, cur_screen_node)
        # 将cur_screen加入到last_screen的子节点
        last_screen_node.add_child(cur_screen_node)
        return cur_screen_node

    @classmethod
    def random_click_one_ele(cls, content):
        # TODO
        print("可能产生了不可去掉的框")
        cur_screen_node = get_cur_screen_node_from_context(content)

        cur_screen_node_clickable_eles = cur_screen_node.get_diff_or_clickable_eles()
        cur_screen_pkg_name, cur_activity, ck_eles_text = get_screen_info_from_context(content)

        # TODO
        candidate = None
        if cur_screen_node.candidate_random_clickable_eles is None or len(
                cur_screen_node.candidate_random_clickable_eles) == 0:
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
        RuntimeContent.get_instance().set_last_screen_node(cur_screen_node)
        RuntimeContent.get_instance().set_last_clickable_ele_uid(cur_clickable_ele_uid)
        d = Config.get_instance().get_device()
        d.click(loc_x, loc_y)
        time.sleep(Config.get_instance().get_sleep_time_sec())

    @classmethod
    def handle_exit_app(cls, content):
        cls.press_back()

    @classmethod
    def handle_double_press(cls, content):
        cls.double_press_back()

    @classmethod
    def handle_inputmethod(cls, content):
        cls.press_back()

    @classmethod
    def handle_WebView_screen(cls, content):
        cls.press_back()

    @classmethod
    def handle_finish_screen(cls, content):
        cls.press_back()

    @classmethod
    def handle_error_screen(cls, content):
        cls.press_back()

    @classmethod
    def handle_restart(cls, content):
        RuntimeContent.get_instance().append_error_screen_list(RuntimeContent.get_instance().get_last_screen_node().ck_eles_text)
        RuntimeContent.get_instance().append_error_clickable_ele_uid_list(
            RuntimeContent.get_instance().get_last_clickable_ele_uid())
        raise RestartException("重启机制")

    @staticmethod
    def press_back():
        d = Config.get_instance().get_device()
        d.press("back")
        print("进行回退")
        time.sleep(Config.get_instance().get_sleep_time_sec())
        return

    @staticmethod
    def double_press_back():
        d = Config.get_instance().get_device()
        d.press("back")
        d.press("back")
        time.sleep(Config.get_instance().get_sleep_time_sec())
        return

