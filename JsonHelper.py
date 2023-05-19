from ScreenNode import *
import json

def dump_screen_map_to_json(file_name, screen_map:dict[str, ScreenNode]):
    res_list = get_res_list_from_screenmap(screen_map)
    dump_to_json(file_name, res_list)

def dump_to_json(file_name:str, res_list:list):
    file_name = file_name + ".json"
    fw = open(file_name, 'w', encoding='utf-8')
    json.dump(res_list, fw, ensure_ascii = False)
    fw.close()

def get_res_list_from_screenmap(screen_map:dict[str, ScreenNode]) -> list:
    res_list = []
    for screen_text, screen_node in screen_map.items():
        json_dict = {}
        json_dict["screen_text"] = screen_text
        json_dict["pkg_name"] = screen_node.pkg_name
        json_dict["class_name"] = screen_node.class_name
        json_dict["activity_name"] = screen_node.activity_name
        json_dict["already_clicked_cnt"] = screen_node.already_clicked_cnt
        json_dict["nextlist"] = get_nextlist(screen_node)
        json_dict["call_map"] = get_callmap_list(screen_node)
        res_list.append(json_dict)
    # print(res_list)
    return res_list

def get_callmap_list(screen_node: ScreenNode)-> list[str]:
    call_map_list = []
    for clickable_ele_uuid, call_screen_node in screen_node.call_map.items():
        call_map_list.append(call_screen_node.all_text)
    # print(call_map_list)
    return call_map_list

def get_nextlist(screen_node: ScreenNode) -> list[str]:
    nextlist = []
    for next in screen_node.children:
        nextlist.append(next.all_text)
    # print(nextlist)
    return nextlist

