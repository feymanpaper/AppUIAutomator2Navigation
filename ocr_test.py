from PIL import Image
import pytesseract
import uiautomator2 as u2
import xml.etree.ElementTree as ET

def get_location_from_xmlele(element):
    bounds = element.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2
    return x, y

def get_screen_all_clickable_text_and_loc(d):
    text = ""
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    for element in root.findall('.//node'):
        temp_text = element.get("text")
        loc_x, loc_y = get_location_from_xmlele(element)
        if temp_text and "隐私权政策" in temp_text:
            print(f"{temp_text}: {loc_x},{loc_y}")
            text += "&" + temp_text + " " + str(loc_x) + " " + str(loc_y)

def is_privacy_related(content:str):
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

if __name__ == '__main__':
    d = u2.connect()
    get_screen_all_clickable_text_and_loc(d)


    # 加载图像
    image = Image.open('/Users/feymanpaper/codeSpace/pyWorkSpace/privacy_policy/collectData/com.alibaba.android.rimet-20230905-210223/Screenshot/ScreenshotPicture/IrDptbPzQJxgydSXEPMYDsPaqJ4cTCd-wkhfJKb_4cY=.png')

    # 将图像转换为文本
    # text = pytesseract.image_to_string(image, lang='chi_sim')
    # print(text)

    data = pytesseract.image_to_data(image, output_type='dict', lang='chi_sim')
    boxes = len(data['level'])
    for i in range(boxes):
        if data['text'][i] != '' and is_privacy_related(data['text'][i]):
            print(data['left'][i], data['top'][i], data['width'][i], data['height'][i], data['text'][i])
            x1 = data['left'][i]
            y1 = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]
            x = x1+width/2
            y = y1+height/2
            print(f"{x} {y}")

    target_x = 617.5
    target_y = 1194.0
    d.click(target_x, target_y)
    # # 搜索目标文本
    # target_text = '目标文本'
    # if target_text in text:
    #     # 获取目标文本的位置
    #     coordinates = pytesseract.image_to_boxes(image)
    #     print(coordinates)
    # else:
    #     print('未找到目标文本')