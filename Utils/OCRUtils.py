from PIL import Image
import pytesseract

def cal_privacy_ele_loc(img_path: str):
    image = Image.open(img_path)
    data = pytesseract.image_to_data(image, output_type='dict', lang='chi_sim')
    loc_list = __get_privacy_loc_list(data)
    assert (len(loc_list) >= 5)
    print(loc_list)
    st_index = __select_privacy_loc(loc_list)
    assert (st_index != -1)
    mid_index = __get_mid_index(st_index)
    x, y = loc_list[mid_index][1], loc_list[mid_index][2]
    return x, y

def __is_privacy_related(content: str):
    if content == '隐':
        return True
    elif content == '私':
        return True
    elif content == '权':
        return True
    elif content == '政':
        return True
    elif content == '策':
        return True
    return False


def __get_privacy_loc_list(data):
    boxes = len(data['level'])
    loc_list = []
    for i in range(boxes):
        if data['text'][i] != '' and __is_privacy_related(data['text'][i]):
            print(data['left'][i], data['top'][i], data['width'][i], data['height'][i], data['text'][i])
            x1 = data['left'][i]
            y1 = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            x = x1 + width / 2
            y = y1 + height / 2
            loc_list.append((data['text'][i], x, y))
    return loc_list


def __select_privacy_loc(loc_list):
    index = -1
    for i in range(len(loc_list) - 5 + 1):
        if loc_list[i][0] == "隐" and loc_list[i + 1][0] == "私" and loc_list[i + 2][0] == "权" and loc_list[i + 3][
            0] == "政" and loc_list[i + 4][0] == "策":
            index = i
            break
    return index


def __get_mid_index(st_index):
    return st_index + 2


