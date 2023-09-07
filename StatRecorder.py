import time
from Utils.LogUtils import *
from Config import *
from RuntimeContent import *
class StatRecorder(object):
    def __init__(self):
        self.total_eles_cnt = 0
        self.stat_screen_set = set()
        self.stat_activity_set = set()
        self.start_time = -1
        self.end_time = -1
        self.restart_cnt = 0
        self.webview_set = set()

    def __new__(cls, *args, **kwargs):
        if not hasattr(StatRecorder, "_instance"):
            StatRecorder._instance = object.__new__(cls)
        return StatRecorder._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(StatRecorder, '_instance'):
            StatRecorder._instance = StatRecorder(*args, **kwargs)
        return StatRecorder._instance

    def set_start_time(self):
        self.start_time = time.time()

    def inc_total_ele_cnt(self):
        self.total_eles_cnt +=1

    def add_stat_screen_set(self, ck_eles_text:str):
        self.stat_screen_set.add(ck_eles_text)

    def add_webview_set(self, webview_text:str):
        self.webview_set.add(webview_text)

    def add_stat_stat_activity_set(self, cur_activity):
        self.stat_activity_set.add(cur_activity)

    def count_time(self):
        self.end_time = time.time()
        if self.end_time - self.start_time > Config.get_instance().test_time:
            raise Exception

    def print_result(self):
        LogUtils.log_info("@" * 100)
        LogUtils.log_info("@" * 100)
        LogUtils.log_info(f"总共点击的activity个数 {len(self.stat_activity_set)}")
        LogUtils.log_info(f"总共点击的Screen个数: {len(self.stat_screen_set)}")
        LogUtils.log_info(f"总共点击的组件个数: {self.total_eles_cnt}")
        LogUtils.log_info(f"总共触发的WebView个数: {len(self.webview_set)}")
        self.end_time = time.time()
        LogUtils.log_info(f"时间为 {self.end_time - self.start_time}")

    def printAcoverage(self):
        LogUtils.log_info("@" * 100)
        LogUtils.log_info("@" * 100)
        screen_map = RuntimeContent.get_instance().get_screen_map()
        for screen_uid, screen_node in screen_map.items():
            clickable_eles = screen_node.get_diff_or_clickable_eles()
            if clickable_eles is None or len(clickable_eles) == 0:
                print(f"{screen_uid} 没有可点击组件")
            else:
                total_cnt = len(screen_node.get_diff_or_clickable_eles())
                click_cnt = screen_node.already_clicked_cnt
                res = click_cnt/total_cnt
                print(f"{screen_uid} 的覆盖率为 {res}")

    def print_coverage(self):
        LogUtils.log_info("@" * 100)
        LogUtils.log_info("@" * 100)
        screen_depth_map = RuntimeContent.get_instance().screen_depth_map
        for screen_uid, depth in screen_depth_map.items():
            if depth > Config.get_instance().maxDepth:
                continue
            screen_node = RuntimeContent.get_instance().get_screen_map().get(screen_uid)
            if screen_node is not None:
                clickable_eles = screen_node.get_diff_or_clickable_eles()
                if clickable_eles is None or len(clickable_eles) == 0:
                    print(f"{screen_uid} 没有可点击组件")
                else:
                    total_cnt = len(screen_node.get_diff_or_clickable_eles())
                    click_cnt = screen_node.already_clicked_cnt
                    res = click_cnt/total_cnt
                    print(f"{screen_uid} 的覆盖率为 {res}")

    def to_string_result(self):
        assert (self.end_time != -1)
        diff_time = self.end_time - self.start_time
        return f"_restart{self.restart_cnt}activity{len(self.stat_activity_set)}&screen{len(self.stat_screen_set)}&time{round(diff_time, 2)}s"

    def get_stat_screen_set(self):
        return self.stat_screen_set

    def get_stat_activity_set(self):
        return self.stat_activity_set

    def get_total_eles_cnt(self):
        return self.total_eles_cnt

    def inc_restart_cnt(self):
        self.restart_cnt +=1

    def get_webview_set(self):
        return self.webview_set



