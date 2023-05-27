class StateHandler(object):
    state_map = {
        1: "不是当前要测试的app,即app跳出了测试的app",
        2: "发现当前界面有文本输入法框",
        3: "当前Screen已经存在",
        4: "当前Screen已经点完",
        5: "当前Screen不存在,新建Screen",
        6: "出现了不可回退的框, 启用随机点",
        7: "出现了不可回退的框, 需要重启?",
        8: "出现了不可回退的框, 启用double_press_back",
        9: "出现了系统权限页面",
        10: "出现了系统外不可回退的框",
        11: "当前Screen为WebView",
    }

    @classmethod
    def print_state(cls, state):
        print(f"状态为{state} {cls.state_map[state]}")

