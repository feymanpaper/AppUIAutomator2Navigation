# 介绍:
# 根据邻接表(图的数据结构表示)建立App界面之间的跳转图, 比如界面A点击了某个按钮跳转到了界面B, 则表示A->B
# privacy_policy/dumpjson 目录下的每个json文件表示一个App界面之间跳转的邻接表
# 以app.podcast.cosmos_restart0activity41&screen248&time2844.76s文件举例, 该文件表示的是App包名为app.podcast.cosmos(该App为小宇宙)的界面跳转图
# 观察其json结构, ck_eles_text表示的是该界面的screen_uid(可点击组件的文本和位置信息),即通过这个screen_uid我们可以唯一标识这个界面
# nextlist表示的是从某个界面出发, 能到达的其他界面(注意其他界面也以screen_uid表示)
# call_map同样表示从某个界面触发能到达的其他界面, 是一个map{key, value}, 表示通过点击某个按钮(key:clickable_ele_uid)到达的其他界面(value:screen_uid)
# call_map和nextlist还有不同的地方就是nextlist可能存在环, 比如A->B->C->A, call_map是无环图

# 此外, 另外一个同学在做的是将界面截图收集起来, 并且将界面的screen_uid进行encode, 界面截图的文件命名为encode(screen_uid)
# ScreenshotUtils.py还会提供函数进行decode, 使得decode(encode(screen_uid)) = screen_uid

# 任务:根据App界面截图和json邻接表, 建立一个App界面之间的跳转图, 并且可视化出来

import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from PIL import Image

# 点布局相关
x_root = 0
y_root = 0
x_space = 3000
y_space = 6000

# 截图比例相关
node_size = 1000
length_to_width_ratio = 1.5

class DrawGraphUtils:
    @staticmethod
    def draw_callgraph(jsonFilePath, screenShotFilePath, svgSaveFilePath):
        pass

    @staticmethod
    def load_data():
        pass

    @staticmethod
    def save_data():
        pass