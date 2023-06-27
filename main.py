#!/usr/bin/python3

import threading
import time
import os
from androguard.core.bytecodes import apk
import shutil
import sys


# 为线程定义一个函数
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("%s: %s" % (threadName, time.ctime(time.time())))


def create_path_ifnotexist(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_timestamp():
    timestamp = int(round(time.time() * 1000000))
    return timestamp


def auto_uninstall_and_install(apk_path, package_name):
    pass


def my_func():
    while True:
        print("Running...")
        time.sleep(1)


def get_hash(data):
    import hashlib
    data_sha = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return data_sha

def take_xml(self, hash):
    cur_app_path = 'G:\\app_audit'
    xml_name = hash + ".xml"
    d = Config.get_instance().get_device()
    xml = d.dump_hierarchy()
    xml_text = get_dump_xml_text()
    xml_file = open(os.path.join(cur_app_path, xml_name), "w+")
    xml_file.write(xml_text)
    xml_file.flush()
    xml_file.close()


if __name__ == '__main__':
    data = "&我的 972 2152&上海 85 165&上海自助餐的天花板 563 165& 992 165&去开启 821 301& 981 301&西塔老太太 251 434&牛new寿喜烧 485 434&自助餐 686 434&鸿姐老火锅 873 434& 117 555& 328 555& 540 555& 751 555& 963 555& 117 758& 328 758& 540 758& 751 758& 963 758&关注NEW 95 1016& 281 1331& 479 1552& 451 1752& 281 1964& 800 1415& 998 1720& 970 1920& 800 2047&马上登录 931 2050&首页 108 2152&地图 324 2152& 540 2143&消息 756 2152"
    print(get_hash(data))
