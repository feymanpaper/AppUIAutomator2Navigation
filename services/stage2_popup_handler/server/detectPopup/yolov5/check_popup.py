
import cv2
import argparse
import os
import shutil
import numpy as np
from skimage.metrics import structural_similarity as ssim
import time
import torch
from PIL import Image
from models.yolo import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized
import io

import numpy as np
from PIL import Image
from django.http import HttpResponse,JsonResponse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--weights', nargs='+', type=str, default='best.pt', help='model.pt path(s)')
parser.add_argument('--source', type=str, default='data/images', help='source')  # file/folder, 0 for webcam
parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
parser.add_argument('--conf-thres', type=float, default=0.05, help='object confidence threshold')
parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
parser.add_argument('--view-img', action='store_true', help='display results')
parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
parser.add_argument('--augment', action='store_true', help='augmented inference')
parser.add_argument('--update', action='store_true', help='update all models')
parser.add_argument('--project', default='runs/detect', help='save results to project/name')
parser.add_argument('--name', default='exp', help='save results to project/name')
parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
opt = parser.parse_args(args=[])

def has_edge(cnt,gray):
    x, y, w, h = cv2.boundingRect(cnt)
    border_intensity = []
    if y > 0:
        border_intensity.append(np.mean(gray[y-1, x:x+w]))
    if y+h+1 < gray.shape[0]:
        border_intensity.append(np.mean(gray[y+h+1, x:x+w]))
    if x > 0:
        border_intensity.append(np.mean(gray[y:y+h, x-1]))
    if x+w+1 < gray.shape[1]:
        border_intensity.append(np.mean(gray[y:y+h, x+w+1]))
    edge_intensity = np.mean(gray[y:y+h, x:x+w]) - np.mean(border_intensity)
    if edge_intensity > 5:  
        return True
    return False

def detect_color(cnt,img):
    x, y, w, h = cv2.boundingRect(cnt)
    xmin, ymin, xmax, ymax = x, y, x+w, y+h
    region = img[ymin:ymax, xmin:xmax]
    sobelx = cv2.Sobel(region, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(region, cv2.CV_64F, 0, 1, ksize=5)
    gradient = np.sqrt(sobelx**2.0 + sobely**2.0)
    region_variance = np.var(gradient)
    background = np.copy(img)
    background[ymin:ymax, xmin:xmax] = 0
    sobelx = cv2.Sobel(background, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(background, cv2.CV_64F, 0, 1, ksize=5)
    gradient = np.sqrt(sobelx**2.0 + sobely**2.0)
    background_variance = np.var(gradient)
    # 比较模糊度
    if region_variance - background_variance > 1/5 * background_variance:
        return True
    else:
        mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
        mask[y:y+h, x:x+w] = 1
        region_intensity = np.mean(cv2.mean(img, mask=mask))
        mask_inv = cv2.bitwise_not(mask) 
        outside_region_intensity = np.mean(cv2.mean(img, mask=mask_inv))
        # 比较颜色亮度
        if region_intensity - outside_region_intensity > 50:
            return True
        return False

def is_center(cnt,img):
    x, y, w, h = cv2.boundingRect(cnt)
    center_x, center_y = x + w//2, y + h//2
    if center_x > img.shape[1] * 0.4 and center_x < img.shape[1] * 0.6 and center_y > img.shape[0] * 0.35 and center_y < img.shape[0] * 0.6:
        return True
    return False

def is_pop(cnt,img,gray):
    x, y, w, h = cv2.boundingRect(cnt)
    # 对区域大小进行限制
    if w!=img.shape[1] and h!=img.shape[0] and w>img.shape[1] * 0.5 and h>img.shape[0] * 0.1 and h < img.shape[0] * 0.9:
        if is_center(cnt,img) and has_edge(cnt,gray) and detect_color(cnt,img):
            return True
    return False

def detect_popup_by_canny(img):
    if img is None:
        print("no img")
        return []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img, 100, 200)
    edges = cv2.dilate(edges, None)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    popup_boxes = []
    for cnt in contours:
        if is_pop(cnt,img,gray):
            x, y, w, h = cv2.boundingRect(cnt)
            popup_boxes.append((x, y, x+w, y+h))
    return popup_boxes


def detect_popup(img):
    print("detect_popup")
    popup_boxes = detect_popup_by_canny(img)
    if len(popup_boxes)>0:
        # 一个弹窗可能会得到多个轮廓，只取最外层的
        box = popup_boxes[0]
        return {"class":"pop_up","bounds": box}
    return None

# 指定使用的GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 加载模型
weights = '/code/detectPopup/detectPopup/yolov5/best.pt'  # 更新权重文件路径
model = attempt_load(weights, map_location=device)

# 将模型设置为评估模式
model.eval()
stride = int(model.stride.max())  # model stride
names = model.module.names if hasattr(model, 'module') else model.names


def detect_button(img):
    buttons = []
    im0s = img
    img = cv2.resize(img, (640, 640))
    img = torch.from_numpy(img).float().div(255.0).permute(2, 0, 1).unsqueeze(0).to(device)
    # img /= 255.0  # 0 - 255 to 0.0 - 1.0
    # if img.ndimension() == 3:
    #     img = img.unsqueeze(0)
    pred = model(img)[0]
    pred = non_max_suppression(pred, opt.conf_thres,agnostic=opt.agnostic_nms)
    for i, det in enumerate(pred):
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
            for *xyxy, conf, cls in reversed(det):
                box = (int(xyxy[0].item()), int(xyxy[1].item()), int(xyxy[2].item()), int(xyxy[3].item()))
                buttons.append({"class": names[int(cls)], "bounds": box})
    return buttons
        
def detect_pic(img):
    pop_up = detect_popup(img)
    if pop_up is None:
        return None
    else:
        buttons = detect_button(img)
        res = []
        res.append(pop_up)
        res.extend(buttons)
        return res



# if __name__ == '__main__':
#     source = '/code/yolov5_5_0/yolov5/check_btn'
#     for root, dirs, files in os.walk(source):
#         for apk in dirs:
#             apkPath = os.path.join(source,apk)
#             for subroot, subdirs, subfiles in os.walk(apkPath):                   
#                 for round in subdirs:
#                     roundPath = os.path.join(apkPath,round)
#                     for subsubroot, subsubdirs, subsubfiles in os.walk(roundPath): 
#                         img_list = os.listdir(subsubroot)
#                         for file in img_list:
#                             if not file.endswith(".png"):
#                                 continue
#                             img_path = os.path.join(subsubroot,file)
                        
#                             print(img_path)
#                             res = detect_popup(img_path)
#                             print(res)
#                             if res is not None:
#                                 detect_button(img_path)
           