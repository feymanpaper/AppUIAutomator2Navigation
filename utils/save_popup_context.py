import os
import shutil
from datetime import datetime
import random
import json

def get_random_str():
    str = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 10))
    return str
# def copy_image_as_byte_stream(from_img_source_path, from_img_save_path, to_img_source_path, to_img_save_path):
#     # Copy from_img_full_path to from_img_path
#     with open(from_img_source_path, 'rb') as f:
#         byte_stream = f.read()
#         with open(from_img_save_path, 'wb') as f_out:
#             f_out.write(byte_stream)
#
#     # Copy to_img_full_path to to_img_path
#     with open(to_img_source_path, 'rb') as f:
#         byte_stream = f.read()
#         with open(to_img_save_path, 'wb') as f_out:
#             f_out.write(byte_stream)

def copy_image_as_byte_stream(source, target):
    # Copy from_img_full_path to from_img_path
    with open(source, 'rb') as f:
        byte_stream = f.read()
        with open(target, 'wb') as f_out:
            f_out.write(byte_stream)

def save_popup_context(abs_path: str, from_img: str, to_img: str, click_xy: tuple, click_text:str, from_text:str, to_text:str):
    # 创建文件夹名,获取包名
    # package_name = abs_path.split("\\")[-1].split("-")[0]

    # 加上时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    time_path = f"{timestamp}"
    abs_dir = os.getcwd()
    #获取当前文件所在目录
    base_directory = abs_path
    screenshot_dir = os.path.join(abs_dir, base_directory, "Screenshot", "ScreenshotPicture")

    from_img = os.path.split(from_img)[-1]
    to_img = os.path.split(to_img)[-1]

    # 保存图片
    from_img_path = os.path.join(screenshot_dir, f"{from_img}")
    to_img_path = os.path.join(screenshot_dir, f"{to_img}")

    popup_dir = os.path.join(abs_dir, base_directory, "PopupContext", time_path)
    os.makedirs(popup_dir)
    from_img_save_path = os.path.join(popup_dir, from_img)
    to_img_save_path = os.path.join(popup_dir, to_img)

    if "root" not in from_img_path:
        copy_image_as_byte_stream(from_img_path, from_img_save_path)
    if "root" not in to_img_path:
        copy_image_as_byte_stream(to_img_path, to_img_save_path)

    json_full_path = os.path.join(popup_dir, "ui_relations.txt")

    # 保存到json文件

    res_dict = {}
    res_dict["from_img"] = from_img
    res_dict["to_img"] = to_img
    res_dict["click_text"] = click_text
    res_dict["click_xy"] = click_xy
    res_dict["from_text"] = from_text
    res_dict["to_text"] = to_text
    with open(json_full_path, "w") as file:
        json.dump(res_dict, file, ensure_ascii=False)
