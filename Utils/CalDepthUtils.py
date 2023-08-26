import json
from collections import deque

class CalDepthUtils:
    @staticmethod
    def calDepth(screen_map):
        pass

    @staticmethod
    def bfs(adj_list, start_uid):
        """
        使用BFS算法遍历邻接表，并计算每个节点的层数
        """
        # 创建一个队列，并将起始节点加入队列中
        queue = deque([(start_uid, 0)])

        # 创建一个集合，用于记录已经访问过的节点
        visited = set()

        while queue:
            # 从队列中取出一个节点
            uid, level = queue.popleft()

            # 如果这个节点已经被访问过了，则跳过
            if uid in visited:
                continue

            # 将这个节点标记为已访问
            visited.add(uid)

            # 输出这个节点的层数
            print(f"Node {uid} is at level {level}")

            # 遍历这个节点的所有邻居，并将它们加入队列中
            target_screen = CalDepthUtils.indexScreen(adj_list, uid)
            for neighbor in target_screen['call_map'].values():
                queue.append((neighbor, level + 1))

    @staticmethod
    def indexScreen(adj_list, target_uid):
        for screen in adj_list:
            if screen["ck_eles_text"] == target_uid:
                return screen

if __name__ == "__main__":
    print(1)
    json_name = "/Users/feymanpaper/codeSpace/pyWorkSpace/privacy_policy/dumpjson/app.podcast.cosmos_restart0activity41&screen248&time2844.76s.json"

    with open(json_name, 'r') as f:
        data = json.load(f)
        print(data)


    start_screen_text = "&设置 540 1648&个人主页 540 599&HD445166t还 540 373&创作中心录制、管理你 540 736&我的通知 540 918&收听历史 540 1055&我的收藏 540 1192&付费账户 540 1329&问题反馈 540 1511& 540 2135& 849 2135& 990 2136&发现 180 2240&订阅 540 2240"
    # 计算'screen1'节点的层数
    CalDepthUtils.bfs(data, start_screen_text)