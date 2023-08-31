import os.path

from uiautomator2 import Device
from datetime import datetime


class Config(object):
    def __init__(self):
        self.CLICK_MAX_CNT = 4
        self.sleep_time_sec = 2  # 配置点击之后睡眠的时间
        self.device = None
        self.test_time = 3600  # 配置测试的时间,以秒为单位
        self.screen_similarity_threshold = 0.9  # 配置界面与界面之间相似度多少表示同一界面, 默认90%/0.9
        self.maxDepth = 6  # 配置点击的最大深度
        self.isDrawAppCallGraph = True  # 配置是否绘制App界面跳转图
        # self.target_pkg_name = "com.example.myapplication"
        self.target_pkg_name = "com.alibaba.android.rimet"
        # self.target_pkg_name = "com.ss.android.ugc.aweme" #抖音
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
        # self.target_pkg_name = "tv.danmaku.bili" #b站
        # self.target_pkg_name = "com.netease.edu.ucmooc" #MOOC
        # self.target_pkg_name = "com.cainiao.wireless" #菜鸟
        # self.target_pkg_name = "com.taobao.taobao" #淘宝
        # self.target_pkg_name = "com.taobao.mobile.dipei"#口碑
        # self.target_pkg_name = "com.taobao.trip"#飞猪旅行
        # self.target_pkg_name = "com.youku.phone"#优酷
        # self.target_pkg_name = "com.eg.android.AlipayGphone"#支付宝
        # self.target_pkg_name = "com.xiaomi.smarthome" #米家
        # self.target_pkg_name = "me.ele" #饿了么

        self.root_path = "collectData"
        self.start_time = datetime.now().strftime("%Y%m%d-%H%M%S")

        self.use_pickle_file_name = "./SavedInstance/com.eg.android.AlipayGphone_restart0activity28&screen78&time3601.86s.pickle"
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

    def get_CollectDataName(self):
        return self.target_pkg_name + "-" + self.start_time

    def get_collectDataPath(self):
        pkg_path = self.target_pkg_name + "-" + self.start_time
        return os.path.join(self.root_path, pkg_path)
