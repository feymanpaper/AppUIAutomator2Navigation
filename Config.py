import os

from uiautomator2 import Device
class Config(object):
    def __init__(self):

        # 自动收集时的手动设置数据
        # 要跑的app的路径
        self.app_path = "E:\\adv_data_set\\app300"
        # 跑出来的数据存放地址
        self.app_data_path = "G:\\app_audit\\"
        # 每个app跑的时间，以秒为单位
        self.ever_app_run_time = 60*15

        # 自动收集的运行时数据,不需要改动
        self.cur_app_path = ""


        self.CLICK_MAX_CNT = 4
        self.sleep_time_sec = 2
        self.device = None
        # self.target_pkg_name = "com.example.myapplication"
        self.target_pkg_name = ""
        # app_data_path/packagename_timestamp
        # self.target_pkg_name = "net.csdn.csdnplus"
        # self.target_pkg_name = "com.sina.weibo"
        # self.target_pkg_name = "com.youku.phone"
        # self.target_pkg_name = "cn.damai"
        # self.target_pkg_name = "com.ss.android.lark"
        # self.target_pkg_name = "com.cloudy.component"
        # self.target_pkg_name = "com.jingyao.easybike"
        # self.target_pkg_name = "com.cainiao.wireless"
        # self.target_pkg_name = "com.xingin.xhs"
        # self.target_pkg_name = "com.yipiao"
        # self.target_pkg_name = "app.podcast.cosmos"
        # self.target_pkg_name = "com.hunantv.imgo.activity"


        self.log_file_name = "./Log/" + self.target_pkg_name + "_1.log"
        self.use_pickle_file_name = "./SavedInstance/" + self.target_pkg_name + "_1.pickle"
        self.is_saved_start = False


    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            Config._instance = object.__new__(cls)
        return Config._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(Config, '_instance'):
            Config._instance = Config(*args, **kwargs)
        return Config._instance

    def get_target_pkg_name(self):
        return self.target_pkg_name

    def get_CLICK_MAX_CNT(self):
        return self.CLICK_MAX_CNT

    def get_sleep_time_sec(self):
        return self.sleep_time_sec

    def get_log_file_name(self):
        return self.log_file_name

    def get_pickle_file_name(self):
        return self.use_pickle_file_name

    def set_device(self, device):
        self.device = device

    def get_device(self):
        if self.device is None:
            self.set_device(Device())
        return self.device