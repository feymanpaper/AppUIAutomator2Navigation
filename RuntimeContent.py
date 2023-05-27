from ScreenNode import *
class RuntimeContent(object):
    def __init__(self):
        # 存储运行时遍历过的screen序列
        self.screen_list = []
        # 存储运行时的state序列
        self.state_list = []
        # 存储因为错误导致重启的screen序列
        self.error_screen_list = []
        # 存储因为错误导致重启的clickable_ele
        self.error_clickable_ele_uid_list = []
        # 存储着整个app所有screen(ScrennNode) {key:screen_sig, val:screen_node}
        self.screen_map = {}
        # 全局记录每个组件的uid {key:cur_clickable_ele_uid, val:clickable_ele}
        self.ele_uid_map = {}



    def __new__(cls, *args, **kwargs):
        if not hasattr(RuntimeContent, "_instance"):
            RuntimeContent._instance = object.__new__(cls)
        return RuntimeContent._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not hasattr(RuntimeContent, '_instance'):
            RuntimeContent._instance = RuntimeContent(*args, **kwargs)
        return RuntimeContent._instance

    def append_screen_list(self, screen_text):
        self.screen_list.append(screen_text)

    def get_screen_list(self):
        return self.screen_list

    def clear_screen_list(self):
        self.screen_list.clear()

    def append_state_list(self, state):
        self.state_list.append(state)

    def get_state_list(self):
        return self.state_list

    def clear_state_list(self):
        self.state_list.clear()

    def append_error_screen_list(self, screen_text:str):
        self.error_screen_list.append(screen_text)

    def get_error_screen_list(self):
        return self.error_screen_list

    def append_error_clickable_ele_uid_list(self, ele_uid:str):
        self.error_clickable_ele_uid_list.append(ele_uid)

    def get_error_clickable_ele_uid_list(self):
        return self.error_clickable_ele_uid_list

    def put_screen_map(self, screen_text:str, screen_node:ScreenNode):
        self.screen_map[screen_text] = screen_node

    def get_screen_map(self):
        return self.screen_map

    def put_ele_uid_map(self, ele_uid, ele_dict):
        self.ele_uid_map[ele_uid] = ele_dict

    def get_ele_uid_map_by_uid(self, uid):
        return self.ele_uid_map[uid]

