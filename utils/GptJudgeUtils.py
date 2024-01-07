import os
import openai
import json
import base64
# import requests
import requests
# 根据实际情况，配置一下系统当前的代理
os.environ["HTTP_PROXY"] = '127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = '127.0.0.1:7890'


# proxies = {
#     'http': '127.0.0.1:7890',
#     'https': '127.0.0.1:7890'
# }

# 将图片转为base64编码
def encode_image(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        print("图片路径错误")


api_key = 'Your Key'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}


def isPictureRight():
    result = {}
    apps = os.listdir('../collectData')
    for dir in apps:
        flashs = os.listdir('../collectData/' + dir + "/PopupContext")
        file = '../collectData/' + dir + "/PopupContext/"
        result[dir] = [0, 0, 0]  # [true,false,others]
        for flash in flashs:
            try:
                with open(file + flash + '/ui_relations.txt', 'r') as fp:
                    relation = json.load(fp)
                    # fp.close()
                    click_txt = relation['click_text']
                    from_txt = relation['from_text']
                    to_text = relation['to_text']
                    click_pos = relation['click_xy']
                    from_image = relation['from_img']
                    to_image = relation['to_img']
                    ques = '一个ui界面的文本为：' + from_txt + ",我在这个界面上点击了文本为：" + click_txt + '的组件，现在它跳转到了另一个界面,界面文字为:' + to_text + ',你能回答一下本次点击的事件和跳转的事件之间是否是明显不关联的，如果是请返回true，否则返回false'
                    if click_txt == 'dummy_root_element':
                        q = '接下来请扮演一个软件安全专家来审查软件中出现弹窗是否合理，下面是一张屏幕截图，我在{}{}处执行了回退操作'.format(
                            click_pos[0], click_pos[1])
                    else:
                        q = '下面是一张屏幕截图，我在图片中的{} {}坐标处点击了文本显示为：{}的组件'.format(click_pos[0],
                                                                                                         click_pos[1],
                                                                                                         click_txt)

                    if from_image == 'root':
                        payload = {
                            "model": 'gpt-4-vision-preview',
                            "messages": [
                                {'role': 'user',
                                 'content': [
                                     {'type': 'text', 'text': '我点击了一个应用'},

                                     {'type': 'text', 'text': '然后这是跳转后的界面,里面包含一个弹窗'},
                                     {'type': 'image_url',
                                      'image_url': {
                                          'url': f'data:image/png;base64,{encode_image(file + flash + "/" + to_image)}'
                                      }},
                                     {'type': 'text',
                                      # 'text': '根据提供的界面截图信息，判断弹框内容是否与预期的核心功能相关，并评估弹框的性质但是不用告诉我评估结果。如果弹框内容与核心功能无关、是广告或有其他不良行为，请返回False；否则，返回True。'
                                      'text': '根据提供的界面截图信息，判断弹框内容是否与预期的核心功能相关、是否存在诱导和广告。如果弹框内容与核心功能无关、是广告或有其他不良行为，请返回False；否则，返回True。注意，你只需要回答True或者False，而不要其他的分析性语句'
                                      }
                                 ]
                                 # 'content':[
                                 #     {'type':'text','text':ques}
                                 # ]
                                 }
                            ],
                            "max_tokens": 20,
                            'temperature': 0.1
                        }
                    else:
                        payload = {
                            "model": 'gpt-4-vision-preview',
                            "messages": [
                                {'role': 'user',
                                 'content': [
                                     {'type': 'text', 'text': q},
                                     {'type': 'image_url',
                                      'image_url': {
                                          'url': f'data:image/png;base64,{encode_image(file + flash + "/" + from_image)}'
                                      }},
                                     {'type': 'text', 'text': '然后这是跳转后的界面,里面包含一个弹窗'},
                                     {'type': 'image_url',
                                      'image_url': {
                                          'url': f'data:image/png;base64,{encode_image(file + flash + "/" + to_image)}'
                                      }},
                                     {'type': 'text',
                                      'text': '根据提供的界面截图信息，判断弹框内容是否与预期的核心功能相关。如果弹框内容与核心功能无关、是广告或有其他不良行为，请返回False；否则，返回True。注意，你只需要回答True或者False，而不要其他的分析性语句'}
                                 ]
                                 # 'content':[
                                 #     {'type':'text','text':ques}
                                 # ]
                                 }
                            ],
                            "max_tokens": 20,
                            'temperature': 0.1
                        }
                    responce = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,
                                             json=payload)

                    responce = responce.json()
                    if 'True' in responce['choices'][0]['message']['content']:
                        result[dir][0] += 1
                        print(1)
                        print(result[dir][0])
                    elif 'False' in responce['choices'][0]['message']['content']:
                        result[dir][1] += 1
                        print(2)
                        print(result[dir][1])
                    else:
                        result[dir][2] += 1
                        print(3)
                        print(result[dir][2])
                    print(responce)
            except:
                print("打开文件失败")

    return result


if __name__ == "__main__":
    ans = isPictureRight()