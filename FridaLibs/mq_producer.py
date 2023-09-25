import threading, time
from queue import Queue
import sys
import frida
import re
from Config import *
from urllib.parse import unquote

lock = threading.Lock()

class Producer(threading.Thread):
    def __init__(self, t_name: str, queue: Queue, daemon: bool):
        threading.Thread.__init__(self, name=t_name, daemon=daemon)
        self.data = queue

    def is_http(self, test_str):
        # 使用re模块进行匹配
        pattern = r'http[s]?(?:://|%3A%2F%2F)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|[#]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        matches = re.findall(pattern, test_str)
        if not matches:
            return None
        # 对url编码进行解码
        decoded_urls = [unquote(match) for match in matches]
        # 返回url列表
        return decoded_urls

    def on_message(self, message, data):
        with lock:
            if message.get('type') == 'send':
                payload = message.get('payload')
                if payload is not None:
                    res = self.is_http(payload)
                    if res:
                        print()
                        print("*" * 50 + f"Producer{self.name}" + "*" * 50)
                        print(res)
                        print("*" * 50 + f"Producer{self.name}" + "*" * 50)
                        print()
                        self.data.put(res)
                        # print("%s: %s is producing %d to the queue!" % (time.ctime(), self.name, message))

    def run(self):
        # device = frida.get_usb_device()
        # 连接模拟器
        device = frida.get_remote_device()
        # 启动`demo02`这个app
        appName = Config.get_instance().app_name
        pid = device.attach(appName)
        # 加载s1.js脚本
        with open("./hook_rpc.js",encoding="utf-8") as f:
        # with open("./FridaLibs/hook_rpc.js") as f:
            script = pid.create_script(f.read())
        script.on('message', self.on_message)
        script.load()
        sys.stdin.read()
