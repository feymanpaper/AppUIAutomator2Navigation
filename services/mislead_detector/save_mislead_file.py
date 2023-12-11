import os
import shutil
from datetime import datetime
import random

def get_random_str():
    str = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 10))
    return str

def save_mislead_file(abs_path: str, from_img: str, to_img: str, click_xy: tuple) -> str:
    # 创建文件夹名,获取包名
    # package_name = abs_path.split("\\")[-1].split("-")[0]
    parts = abs_path.split("\\")
    package_name = parts[1].split("-")[0]
    # 加上时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f"{package_name}_{timestamp}"

    # 创建文件夹,在某个路径下，这里写的绝对路径
    base_directory = "C:/Codelife/ui/collectData/mislead_data"
    directory = os.path.join(base_directory, folder_name)
    os.makedirs(directory)

    # 保存图片
    from_name=get_random_str()
    to_name=get_random_str()
    from_img_path = os.path.join(directory, f"{from_name}.png")
    to_img_path = os.path.join(directory, f"{to_name}.png")
    # 复制图片到新路径,使用绝对路径
    abs_path = "collectData\com.alibaba.aliyun-20231202-003938\Screenshot\ScreenshotPicture"
    abs_path = abs_path.replace("\\", "/")
    abs_path = "C:/Codelife/ui/" + abs_path
    from_img_full_path = os.path.join(abs_path, from_img)
    to_img_full_path = os.path.join(abs_path, to_img)
    shutil.copy(from_img_full_path, from_img_path)
    shutil.copy(to_img_full_path, to_img_path)

    # 保存点击坐标到txt文件
    with open(os.path.join(directory, "ui_relation.txt"), "w") as file:
        file.write(f"{to_name} {from_name} {click_xy[0]} {click_xy[1]}")


    return directory
