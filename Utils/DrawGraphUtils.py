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
from PIL import Image

# 点布局相关
x_root = 0
y_root = 0
x_space = 3000
y_space = 5000

# 截图比例相关
enlarge_ratio = 1600
node_size = 1000
length_to_width_ratio = 1.5

class DrawGraphUtils:
    @staticmethod
    def draw_callgraph(cls):
        #TODO
        # 获取json文件夹路径
        current_dir = os.getcwd()
        json_folder = os.path.join(current_dir, "dumpjson")

        # 遍历文件夹所有文件
        for filename in os.listdir(json_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(json_folder, filename)

                # 打开/读取JSON文件
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    graph = nx.DiGraph()
                    # 存放截图显示位置
                    pos = {}
                    root_flag = 1

                    for obj in data:
                        ck_eles_text = obj["ck_eles_text"]
                        nextlist = obj["nextlist"]
                        call_map = obj["call_map"]

                        if root_flag:
                            graph.add_node(ck_eles_text)
                            pos[ck_eles_text] = (x_root, y_root)
                            root_flag = 0

                        if graph.has_node(ck_eles_text):
                            x_parent, y_parent = pos[ck_eles_text]
                            num = len(nextlist)
                            x_first = x_parent - num * x_space / 2
                            order = 0

                            for nxt in nextlist:
                                if not graph.has_node(nxt):
                                    graph.add_node(nxt)
                                    x_child = x_first + order * x_space
                                    order += 1
                                    y_child = y_parent - y_space
                                    pos[nxt] = (x_child, y_child)

                                if nxt is not None and ck_eles_text != nxt:
                                    graph.add_edge(ck_eles_text, nxt)

                            for _, target in call_map.items():
                                if target is not None and ck_eles_text != target:
                                    graph.add_edge(ck_eles_text, target)
                        else:
                            break

                    # 测试点位置
                    node_size = 20
                    nx.draw_networkx_edges(graph, pos, arrowstyle='-', width=1)
                    nx.draw_networkx(graph, pos, with_labels=False, arrows=True, node_size=node_size)
                    plt.show()

                    # # 获取每个点对应截图
                    # image_files = {node: 'image1.png' for node in graph.nodes}
                    # nx.set_node_attributes(graph, image_files, 'image')
                    #
                    # fig, ax = plt.subplots(figsize=(100, 150))
                    #
                    # # 调整截图显示位置和比例
                    # for node in graph.nodes:
                    #     x, y = pos[node]
                    #     x *= enlarge_ratio
                    #     y *= enlarge_ratio
                    #     img_path = graph.nodes[node]['image']
                    #     img = Image.open(img_path)
                    #     resized_img = img.resize((node_size, int(node_size * length_to_width_ratio)))
                    #     img_width, img_height = img.size
                    #
                    #     x -= img_width / 2
                    #     y -= img_height / 2
                    #     ax.imshow(resized_img, extent=(x, x + img_width, y, y + img_height), zorder=1)
                    #
                    # # 画图
                    # nx.draw_networkx_edges(graph, pos, ax=ax, width=2, edge_color='black', alpha=0.7)
                    # ax.margins(0.2)
                    # plt.axis('off')
                    # # # 保存图片
                    # # picture_folder = os.path.join(current_dir, "graph_picture") + '\\'
                    # # picture_name = filename + '.png'
                    # # plt.savefig(picture_folder + picture_name)
                    # plt.show()
        