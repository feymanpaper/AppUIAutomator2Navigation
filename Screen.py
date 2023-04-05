class Screen:
    def __init__(self):
        # 包名 + 类名 + activity 
        self.pkg_name = ""
        self.class_name = ""
        self.activity_name = ""
        # call_map:{key:widget_uuid, value: next_screen}
        # call_map主要记录哪些组件能到达下一个Screen
        self.call_map = {}
        # 记录当前screen可点击的组件
        self.clickable_widget = []
        # 记录当前screen已经被点击过的组件个数
        self.already_clicked_cnt = 0
    


