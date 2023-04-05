# cur_activity
# for....所有能点击的组件:
#   click()
# 否则当前没东西可点了，back ，不写成dfs
from utils import *
from Screen import *


def dfs_screen(last_screen_sig, last_clickable_ele):
    # 获取当前screen
    cur_screen_info = get_screen_info(d)
    cur_screen_sig = get_signature(cur_screen_info)

    #EditText点击之后会有输入框，此时无法点击其他组件
    #因此需要back消除输入框，然后return
    if last_clickable_ele is not None:
        if("EditText" in last_clickable_ele.get("class")):
            d.press("back")
            return
        
    

    # screen没有变化说明该组件不会造成页面跳转
    if cur_screen_sig == last_screen_sig:
        return
    print(cur_screen_info)
    print("*"*100)
    
    # 建Screen跳转图
    cur_screen_node = None
    if screen_map.get(cur_screen_sig, False) == False:
        # 初始化cur_screen_node信息
        cur_screen_node = ScreenNode()
        cur_screen_node.info = cur_screen_info
        cur_screen_node.sig = cur_screen_sig
        clickable_eles = get_clickable_elements(d, umap)
        cur_screen_node.clickable_elements = clickable_eles
        # 将cur_screen加入到全局记录的screen_map
        screen_map[cur_screen_sig] = cur_screen_node
        # 将cur_screen加入到last_screen的子节点
        last_screen_node = screen_map.get(last_screen_sig)
        last_screen_node.add_child(cur_screen_node)
    else:
        cur_screen_node = screen_map.get(cur_screen_sig)

    #如果触发了新的界面，这个时候要判断是否存在回边，存在环就不加call_map
    #表示虽然该组件能触发新界面，但是会产生回边，因此不能将screen加入call_map
    if last_screen_sig != "root":
        last_screen_node = screen_map.get(last_screen_sig)
        if last_screen_node.find_ancestor(cur_screen_sig):
            #产生了回边
            pass
        else:
            last_clickale_ele_uuid = get_uuid(last_clickable_ele, d, umap)
            last_screen_node.call_map[last_clickale_ele_uuid] = cur_screen_sig
    
    # 遍历cur_screen的所有可点击组件
    cur_screen_node_clickable_eles = cur_screen_node.clickable_elements
    for cur_clickable_ele in cur_screen_node_clickable_eles:
        #--------------------------------------
        #判断当前组件是否需要访问
        #1.如果没访问过，即vis_map[uuid]=False，就直接访问
        #2.如果访问过了，即vis_map[uuid]=True,还得判断该组件是否是
        #当前callmap的，如果是还需要递归判断该组件对应的call_map里面的节点(screen)
        #的所有组件是否访问完毕
        uuid = get_uuid(cur_clickable_ele, d, umap)
        if ele_vis_map.get(uuid, False) == False:
            # 拿到该组件的坐标x, y
            loc_x, loc_y = get_location(cur_clickable_ele)
            ele_vis_map[uuid] = True
            #点击该组件
            cur_screen_node.already_clicked_cnt = get_uuid_cnt(uuid)
            print(f"点击组件: {uuid}")
            d.click(loc_x, loc_y)
            time.sleep(2)
            dfs_screen(cur_screen_sig, cur_clickable_ele)

        else:
            if cur_screen_node.call_map.get(uuid, None) is not None:
                target_screen_sig = cur_screen_node.call_map.get(uuid)
                if not cur_screen_node.is_all_children_finish(target_screen_sig):
                    # click_map指示存在部分没完成
                    loc_x, loc_y = get_location(cur_clickable_ele)
                    # 点击该组件
                    cur_screen_node.already_clicked_cnt = get_uuid_cnt(uuid)
                    print(f"点击组件: {uuid}")
                    d.click(loc_x, loc_y)
                    time.sleep(2)
                    dfs_screen(cur_screen_sig, cur_clickable_ele)
    # for循环遍历结束back返回上一层界面
    d.press("back")
    time.sleep(2)



# 存储着整个app所有screen(ScrennNode) {key:screen_sig, val:screen_node}
screen_map = {}
# umap: {key:uid, value:cnt}
umap = {}
# 全局记录组件是否有被点击过 {key:uuid, val:true/false}
ele_vis_map = {}


# 启动app开始执行
d = Device()
curr_pkg_name = "com.example.myapplication"
# curr_pkg_name = "com.alibaba.android.rimet"
d.app_start(curr_pkg_name)
time.sleep(3)
root_sig = "root"
root = ScreenNode()
root.sig = root_sig
screen_map["root"] = root
dfs_screen(root_sig, None)