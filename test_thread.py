import threading
import time
from Config import *
from services.privacy_policy_hook.mq_producer import *

class MyThread(threading.Thread):
    def __init__(self,  daemon: bool):
        threading.Thread.__init__(self, daemon=daemon)
        # self.is_stop=False
        self._stop_event = threading.Event()

    def run(self):
        while not self.is_stop:
        # while not self._stop_event.is_set():
            print("线程开始执行")
            time.sleep(5)
            print("线程执行完成")
        print("线程终止")

    def stop(self):
        # self.is_stop = True
        self._stop_event.set()


# def restart_thread(thread):
#     thread.stop()
#     new_thread = MyThread(daemon=True)
#     new_thread.start()


d = Device()
queue = Queue()
frida_hook_service = FridaHookService('FridaHookService', queue, daemon=True)
d.app_start("com.alibaba.wireless.lstretailer", use_monkey=True)
frida_hook_service.start()


while True:
    time.sleep(10)
    d.app_stop("com.alibaba.wireless.lstretailer")
    print("重启")
    time.sleep(1)
    d.app_start("com.alibaba.wireless.lstretailer", use_monkey=True)
    restart_thread(frida_hook_service)

# # 创建并启动线程
# thread = MyThread(daemon=True)
# thread.start()
#
# # 等待一段时间后重启线程
# time.sleep(10)
# restart_thread(thread)
# print("主线程结束")