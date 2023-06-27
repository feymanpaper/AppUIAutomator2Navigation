from StateHandler import *
from DeviceHelper import *
import hashlib


class FSM:
    # state_map = {
    #     1: "不是当前要测试的app,即app跳出了测试的app",
    #     2: "发现当前界面有文本输入法框",
    #     3: "当前Screen已经存在",
    #     4: "当前Screen已经点完",
    #     5: "当前Screen不存在,新建Screen",
    #     6: "出现了不可回退的框, 启用随机点",
    #     7: "出现了不可回退的框, 需要重启?",
    #     8: "出现了不可回退的框, 启用double_press_back",
    #     9: "出现了系统权限页面",
    #     10: "出现了系统外不可回退的框",
    #     11: "当前Screen为WebView",
    #     12: "当前Screen为error不该点",
    #     100: "完成"
    # }

    reverse_state_map = {
        1: "STATE_ExitApp",
        2: "STATE_InputMethod",
        3: "STATE_ExistScreen",
        4: "STATE_FinishScreen",
        5: "STATE_NewScreen",
        6: "STATE_SpecialScreen",
        7: "STATE_Restart",
        8: "STATE_DoublePress",
        9: "STATE_PermissonScreen",
        10: "STATE_OutsystemSpecialScreen",
        11: "STATE_WebViewScreen",
        12: "STATE_ErrorScreen",
        100: "完成"
    }

    STATE_ExitApp = 1
    STATE_InputMethod = 2
    STATE_ExistScreen = 3
    STATE_FinishScreen = 4
    STATE_NewScreen = 5
    STATE_SpecialScreen = 6
    STATE_Restart = 7
    STATE_DoublePress = 8
    STATE_PermissonScreen = 9
    STATE_OutsystemSpecialScreen = 10
    STATE_WebViewScreen = 11
    STATE_ErrorScreen = 12

    def update_stat(self, cur_activity, ck_eles_text):
        StatRecorder.get_instance().add_stat_stat_activity_set(cur_activity)
        StatRecorder.get_instance().add_stat_screen_set(ck_eles_text)

    def get_screen_content(self):

        cur_screen_pkg_name = get_screen_package()
        cur_activity = get_screen_activity()
        screen_text = get_screen_text()
        cur_ck_eles = get_clickable_elements()
        pre_len = len(cur_ck_eles)
        cur_ck_eles = remove_dup(cur_ck_eles)
        cur_ck_eles = merged_clickable_elements(cur_ck_eles)
        after_len = len(cur_ck_eles)
        ck_eles_text = to_string_ck_els(cur_ck_eles)
        if RuntimeContent.get_instance().get_first_screen_ck_eles_text() is None:
            RuntimeContent.get_instance().set_first_screen_ck_ele_text(ck_eles_text)
        content = {}
        content["cur_screen_pkg_name"] = cur_screen_pkg_name
        content["cur_activity"] = cur_activity
        content["ck_eles_text"] = ck_eles_text
        content["screen_text"] = screen_text
        content["cur_ck_eles"] = cur_ck_eles
        content["merged_diff"] = pre_len - after_len
        return content

    def do_transition(self, state, content):
        if state == self.STATE_ExitApp:
            StateHandler.handle_exit_app(content)
        elif state == self.STATE_InputMethod:
            StateHandler.handle_inputmethod(content)
        elif state == self.STATE_ExistScreen:
            StateHandler.handle_exist_screen(content)
        elif state == self.STATE_FinishScreen:
            StateHandler.handle_finish_screen(content)
        elif state == self.STATE_NewScreen:
            StateHandler.handle_new_screen(content)
        elif state == self.STATE_SpecialScreen:
            StateHandler.handle_special_screen(content)
        elif state == self.STATE_Restart:
            # TODO 重启机制
            StateHandler.handle_restart(content)
        elif state == self.STATE_DoublePress:
            StateHandler.handle_double_press(content)
        elif state == self.STATE_PermissonScreen:
            StateHandler.handle_system_permission_screen(content)
        elif state == self.STATE_OutsystemSpecialScreen:
            StateHandler.handle_outsystem_special_screen(content)
        elif state == self.STATE_WebViewScreen:
            StateHandler.handle_WebView_screen(content)
        elif state == self.STATE_ErrorScreen:
            StateHandler.handle_error_screen(content)
        else:
            raise Exception("意外情况")

    def get_hash(self, data):
        data_sha = hashlib.sha256(data.encode('utf-8')).hexdigest()
        return data_sha

    def take_screenshot(self, hash):
        cur_app_path = Config.get_instance().cur_app_path
        png_name = hash + ".png"
        os.system("adb shell screencap /sdcard/%s" % (png_name))
        os.system("adb pull /sdcard/%s %s" % (
            png_name, os.path.join(cur_app_path, png_name)))
        os.system("adb shell rm /sdcard/%s" % (png_name))

    def take_xml(self, hash):
        cur_app_path = Config.get_instance().cur_app_path
        xml_name = hash + ".xml"
        xml_text = get_dump_xml_text()
        xml_file = open(os.path.join(cur_app_path, xml_name), "w+", encoding='utf-8')
        xml_file.write(xml_text)
        xml_file.flush()
        xml_file.close()

    def xml_png_collector(self, ck_eles_text):
        if Config.get_instance().target_pkg_name == "":
            return
        cur_app_path = Config.get_instance().cur_app_path
        hash = self.get_hash(ck_eles_text)
        # 截屏
        self.take_screenshot(hash)
        # 截取xml文件
        self.take_xml(hash)

    def get_state(self):

        content = self.get_screen_content()
        cur_activity = content["cur_activity"]
        cur_screen_pkg_name = content["cur_screen_pkg_name"]
        ck_eles_text = content["ck_eles_text"]
        self.update_stat(cur_activity, ck_eles_text)
        Logger.get_instance().print(f"当前Screen为: {ck_eles_text}")

        self.xml_png_collector(ck_eles_text)

        if cur_screen_pkg_name != Config.get_instance().get_target_pkg_name():
            if check_is_in_home_screen(cur_screen_pkg_name) and check_is_first_scrren_finish():
                return self.STATE_Restart, content
            if check_is_in_home_screen(cur_screen_pkg_name):
                return 100, content
            if cur_screen_pkg_name == "com.google.android.packageinstaller":
                return self.STATE_PermissonScreen, content
            else:
                if check_pattern_state(3, [self.STATE_ExitApp]):
                    return self.STATE_Restart, content
                # if check_pattern_state(3, [self.STATE_ExitApp]):
                #     return self.STATE_OutsystemSpecialScreen, content
                else:
                    return self.STATE_ExitApp, content

        if check_is_inputmethod_in_cur_screen() == True:
            return self.STATE_InputMethod, content

        if check_is_in_webview(cur_activity) and check_pattern_state(4, [self.STATE_DoublePress,
                                                                         self.STATE_WebViewScreen]):
            return self.STATE_Restart, content
        if check_is_in_webview(cur_activity) and check_pattern_state(1, [self.STATE_WebViewScreen]):
            return self.STATE_DoublePress, content
        if check_is_in_webview(cur_activity):
            return self.STATE_WebViewScreen, content
        # temp_screen_node = get_screennode_from_screenmap_by_similarity(screen_map, ck_eles_text, screen_compare_strategy)
        # if temp_screen_node is not None and len(temp_screen_node.clickable_elements) == clickable_cnt:
        #     cur_screen_node = temp_screen_node
        # else:
        #     cur_screen_node = None
        sim, most_similar_screen_node = get_max_similarity_screen_node(ck_eles_text,
                                                                       ScreenCompareStrategy(LCSComparator(0.5)))
        content["cur_screen_node"] = most_similar_screen_node
        content["most_similar_screen_node"] = most_similar_screen_node
        content["sim"] = sim
        RuntimeContent.get_instance().append_screen_list(ck_eles_text)

        # if cur_screen_node is not None:
        if sim >= 0.90:
            cur_screen_node = most_similar_screen_node
            RuntimeContent.get_instance().put_screen_map(ck_eles_text, cur_screen_node)

            if check_is_errorscreen(ck_eles_text, ScreenCompareStrategy(LCSComparator())) and check_pattern_state(4, [
                self.STATE_ErrorScreen, self.STATE_DoublePress]):
                return self.STATE_Restart, content
            if check_is_errorscreen(ck_eles_text, ScreenCompareStrategy(LCSComparator())) and check_pattern_state(1, [
                self.STATE_ErrorScreen]) and check_screen_list_reverse(2):
                return self.STATE_DoublePress, content
            if check_is_errorscreen(ck_eles_text, ScreenCompareStrategy(LCSComparator())):
                return self.STATE_ErrorScreen, content

            # TODO k为6,表示出现了连续6个以上的pattern,且所有组件已经点击完毕,避免一些情况:页面有很多组件点了没反应,这个时候应该继续点而不是随机点
            # if check_state_list_reverse(self.STATE_ExitApp, state_list, self.STATE_FinishScreen) and check_screen_list_reverse(self.STATE_OutsystemSpecialScreen, screen_list) and cur_screen_node.is_screen_clickable_finished():
            #     return self.STATE_Restart, content
            if cur_screen_node.is_screen_clickable_finished() and check_pattern_state(10, [self.STATE_FinishScreen,
                                                                                           self.STATE_SpecialScreen,
                                                                                           self.STATE_DoublePress]):
                return self.STATE_Restart, content
            if cur_screen_node.is_screen_clickable_finished() and check_pattern_state(1, [self.STATE_SpecialScreen,
                                                                                          self.STATE_DoublePress]) and check_screen_list_reverse(
                3):
                return self.STATE_SpecialScreen, content
            if cur_screen_node.is_screen_clickable_finished() and check_pattern_state(1,
                                                                                      [
                                                                                          self.STATE_FinishScreen]) and check_screen_list_reverse(
                2):
                return self.STATE_DoublePress, content
            # 4说明已经点完, press_back
            if cur_screen_node.is_screen_clickable_finished():
                return self.STATE_FinishScreen, content
            # 3说明未点完, 触发点一个组件
            else:
                return self.STATE_ExistScreen, content
        else:
            # 放到后面建立完成之后在添加
            # screen_map[ck_eles_text] = cur_screen_node
            return self.STATE_NewScreen, content

    def print_state(self, state):
        # Logger.get_instance().print(f"状态为{self.reverse_state_map[state]} {self.state_map[state]}")
        Logger.get_instance().print(f"状态为{self.reverse_state_map[state]}")

    def start(self):
        stat_map = {}
        state = -1
        while True:
            if len(StatRecorder.get_instance().get_stat_screen_set()) % 10 == 0 and stat_map.get(
                    len(StatRecorder.get_instance().get_stat_screen_set()), False) is False:
                stat_map[len(StatRecorder.get_instance().get_stat_screen_set())] = True
                StatRecorder.get_instance().print_result()

            state, content = self.get_state()
            RuntimeContent.get_instance().append_state_list(state)
            Logger.get_instance().print("\n")
            Logger.get_instance().print("-" * 50)
            self.print_state(state)
            self.do_transition(state, content)
            Logger.get_instance().print("-" * 50)
            Logger.get_instance().print("\n")
