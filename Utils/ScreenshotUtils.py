import uiautomator2 as u2
import base64
import os
import hashlib
import json
from DeviceHelper import *

# 任务:
# 实现一个屏幕截图功能, 注: uiautomator2具有截图功能
# 要求实现截图, 并且将截图命名为encode_screen_uid(screen_uid),即编码当前界面信息的字符串,并且将文件保存在Screenshot目录下(目录不存在则程序自动创建)
# 并且encode_screen_uid(screen_uid)能够进行解码回screen_uid, 即decode_screen_uid(encode_screen_uid(screen_uid)) = screen_uid
# 编码解码格式可以自行选择
# 测试可以在test/ScreenshotUtils_test.py上进行测试, 不需要跑其他文件
class ScreenshotUtils:

    @staticmethod
    def get_screen_uid():
        # 该方法返回当前界面信息(可点击组件的文本和位置)
        cur_ck_eles = get_clickable_elements()
        cur_ck_eles = remove_dup(cur_ck_eles)
        cur_ck_eles = merged_clickable_elements(cur_ck_eles)
        ck_eles_text = to_string_ck_els(cur_ck_eles)
        return ck_eles_text

    @staticmethod
    def screen_shot(screen_uid:str):
        # 连接设备
        d = u2.connect()

        # 创建及写入映射json
        ScreenshotUtils.create_json_file('screenshot_map')
        ScreenshotUtils.write_mapping_to_json('screenshot_map', ScreenshotUtils.encode_screen_uid(screen_uid), screen_uid)

        # 获取屏幕截图
        screenshot = d.screenshot()

        # 创建保存截图和json的目录（如果不存在）
        screenshot_dir = 'Screenshot'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # 构造截图文件名，并保存截图
        filename = ScreenshotUtils.encode_screen_uid(screen_uid)
        screenshot_dir_picture = 'ScreenshotPicture'
        savepath = os.path.join(screenshot_dir, screenshot_dir_picture)
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        filepath = savepath + '/' + filename + '.png'
        screenshot.save(filepath)

    @staticmethod
    def encode_screen_uid(screen_uid: str) -> str:
        hashed_data = hashlib.sha256(screen_uid.encode('utf-8')).digest()
        encoded_bytes = base64.urlsafe_b64encode(hashed_data).decode('utf-8')
        return encoded_bytes

    @staticmethod
    def decode_screen_uid(encode_str: str) -> str:
        file_path = "Screenshot/" + "screenshot_map.json"

        with open(file_path, 'r') as file:
            data = json.load(file)

        value = data.get(encode_str)
        return value

    @staticmethod
    def create_json_file(name):
        # 创建保存 JSON 文件的目录（如果不存在）
        dir_path = 'Screenshot'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        dir_path_json = 'ScreenshotJson'
        dir_path = os.path.join(dir_path, dir_path_json)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 构建文件路径
        file_path = os.path.join(dir_path, f"{name}.json")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            # 创建空的 JSON 数据
            data = {}
            # 写入 JSON 文件
            with open(file_path, 'w') as file:
                json.dump(data, file)

    @staticmethod
    def write_mapping_to_json(name, key, value):
        file_path = f"{name}.json"
        file_path = 'Screenshot/ScreenshotJson/' + file_path

        # 读取 JSON 文件
        with open(file_path, 'r') as file:
            data = json.load(file)

        # 添加映射关系
        data[key] = value

        # 写入 JSON 文件
        with open(file_path, 'w') as file:
            json.dump(data, file)

