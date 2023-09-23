from PIL import Image
import pytesseract
from PIL import ImageEnhance

def cal_privacy_ele_loc(img_path: str, privacy_text:str) -> tuple():
    """
    :param img_path: 截图的路径
    :return: "隐私权政策"文本的坐标
    """
    img = Image.open(img_path)
    # 二值化
    img = img.convert('L')  # 这里也可以尝试使用L
    # 修改图片的灰度
    # img = img.convert('RGB')  # 这里也可以尝试使用L
    # enhancer = ImageEnhance.Color(img)
    # enhancer = enhancer.enhance(0)
    # enhancer = ImageEnhance.Brightness(enhancer)
    # enhancer = enhancer.enhance(2)
    # enhancer = ImageEnhance.Contrast(enhancer)
    # enhancer = enhancer.enhance(8)
    # enhancer = ImageEnhance.Sharpness(enhancer)
    # img = enhancer.enhance(20)

    # config = '--psm 1 -c tessedit_char_whitelist=隐私权政策,'
    # text = pytesseract.image_to_string(img, lang='chi_sim')
    # print(text)

    data = pytesseract.image_to_data(img, output_type='dict', lang='chi_sim')
    loc_list = __get_privacy_loc_list(data, privacy_text)

    if len(loc_list) < len(privacy_text):
        return None

    st_index = __get_first_privacy_loc(loc_list, privacy_text)
    if st_index == -1:
        return None
    mid_index = __get_mid_index(st_index)
    # 此处的变换是为了迎合ele_dict
    x, y, w, h = int(2*loc_list[mid_index][1]), int(2*loc_list[mid_index][2]), int(0), int(0)
    return x, y, w, h


def __is_privacy_related(content: str, pp_text:str):
    for c in pp_text:
        if content == c:
            return True
    return False


def __get_privacy_loc_list(data, pp_text):
    boxes = len(data['level'])
    loc_list = []
    for i in range(boxes):
        if data['text'][i] != '' and __is_privacy_related(data['text'][i], pp_text):
            x1 = data['left'][i]
            y1 = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            x = x1 + width / 2
            y = y1 + height / 2
            loc_list.append((data['text'][i], x, y))
    return loc_list


def __get_first_privacy_loc(loc_list, privacy_text:str):
    index = -1
    for i in range(len(loc_list) - len(privacy_text) + 1):
        flag = True
        for j in range(len(privacy_text)):
            if loc_list[i+j][0] != privacy_text[j]:
                flag = False
                break
        if flag:
            index = i
            break
    return index


def __get_mid_index(st_index):
    return st_index + 2
