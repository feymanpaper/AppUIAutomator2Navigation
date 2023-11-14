from Config import Config
import os
from StatRecorder import *

class FileUtils:
    @classmethod
    def save_coverage(cls, depth, a, b):
        file_name = cls.__get_cov_file_path()
        cls.__write_cov(file_name, depth, a, b)

    @classmethod
    def save_result(cls):
        file_name = cls.__get_cov_file_path()
        sr = StatRecorder.get_instance()
        ans = ""
        ans += f"总共点击的activity个数 {len(sr.stat_activity_set)}\n"
        ans += f"总共点击的Screen个数: {len(sr.stat_screen_set)}\n"
        ans += f"总共点击的组件个数: {sr.total_eles_cnt}\n"
        ans += f"总共触发的WebView个数: {len(sr.webview_set)}\n"
        cls.__write_res(file_name, ans)


    @staticmethod
    def __get_cov_file_path():
        config_path = Config.get_instance().get_collectDataPath()
        cov_file_name = "coverage.txt"
        return os.path.join(config_path, cov_file_name)

    @staticmethod
    def __write_res(file_path, res):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        fw.write(res)
        fw.close()

    @staticmethod
    def __write_cov(file_path:str, depth, a, b):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        fw = open(file_path, 'a', encoding='utf-8')
        cov = a/b
        fw.write(f"{depth}:{a}/{b}={cov}" + "\n")
        fw.close()
