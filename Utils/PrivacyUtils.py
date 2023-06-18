import json


def parse_privacy_txt():
    res = []
    f = open("../PrivacyData/privacy_items.txt")
    lines = f.readlines()
    for line in lines:
        item = line.split(" ")[0]
        res.append(item)
    return res


def parse_dumpjson(file_name):
    f = open(file_name)
    content = f.read()
    a = json.loads(content)
    b = str(a)
    return b


def look_up(item_list, str):
    res = []
    for item in item_list:
        if item in str:
            res.append(item)
    return res


def non_look_up(item_list, str):
    res = []
    for item in item_list:
        if item not in str:
            res.append(item)
    return res


def get_missing_data_item(screen_text_file_name, pricacy_policy_file_name):
    item_list = parse_privacy_txt()
    screen_text_file_name = "../dumpjson/com.alibaba.android.rimet_screen444time8000s.json"
    screen_text = parse_dumpjson(screen_text_file_name)
    match_privacy_item = look_up(item_list, screen_text)
    privacy_policy_file_name = "../PrivacyData/PrivacyPolicySaveDir/钉钉.json"
    privacy_policy_text = parse_dumpjson(privacy_policy_file_name)
    exist_item = look_up(match_privacy_item, privacy_policy_text)
    non_exist_item = non_look_up(match_privacy_item, privacy_policy_text)
    return non_exist_item
