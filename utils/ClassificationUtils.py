"""
主要是将弹框分为三类：
    1、询问、申请
    2、通知
    3、非正常弹框
以及对弹框进行问题判定
    1、诱导行为
    2、后退阻拦
    3、默认开启设置
    4、用户意图不一致
    5、正常弹框
"""



import base64
import os
import shutil
import json
import requests
# import get_ocr_text
from get_ocr_text import get_ocr_text
# import check_mislead
# import openai
from check_mislead import check_is_mislead_text
# import sys
# sys.path.append("C:/Users/17180/pythonProject/detectPopup")
from detectPopup.detect_popup import detect_pic

# 配置代理
# os.environ["HTTP_PROXY"] = '127.0.0.1:7890'
# os.environ['HTTPS_PROXY'] = '127.0.0.1:7890'
proxies = {
    'http':'127.0.0.1:7890',
    'https':'127.0.0.1:7890'
}

# 设置openai的认证
# api_key = 'Your Key'
api_key = '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'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}
# client = openai.OpenAI(api_key=api_key)
# def check_is_mislead_text(text: str) -> bool:
#     """
#     Check if the input text is misleading text
#     :param text: The input text to be checked
#     :return: True if the text is misleading, False otherwise
#     """
#     api_url = 'http://172.16.108.178:5192/check_misleading'  # Replace with the actual URL where the API is hosted
#     data = {'text': text}
#     response = requests.post(api_url, json=data)
#
#     if response.status_code == 200:
#         result = response.json()
#         return result['is_misleading']
#     else:
#         print("Failed to call the API:", response.status_code, response.text)
#         return False  # Return False if there was an error calling the API
#
# mislead_text = "去领取红包"
# res = check_is_mislead_text(mislead_text)
# print(res)

# 定义一个全局列表来维护表示同意的选项：
Allow_list = ["确定","确认","开启","同意","允许","设置","好评","保存","退出","喜欢","留下","安装","已读","登录","授予","更新"]  #,'是',"立即"
# 定义一个全局列表来维护表示拒绝的选项：
Delay_list= ["取消","不同意","否","拒绝","关闭","暂不","离开","再说","再想想","禁止","不用"]  #,"不","再","修改"
# 定义一个全局列表来表示通知的选项:
Info_list= ["知道","好的","提示",'我记住了']   #,"下一步"

# def get_ocr_text(file_path:str)->str:
#     """
#     Identify all text information in the given path's images.
#     :param file_path: The path of the image to be recognized.
#     :return: Image text extraction result
#     """
#     img1 = open(file_path, 'rb')
#     file_resq = {
#         "file": img1
#     }
#     res = requests.post("http://172.16.108.178:5185/ocr", files=file_resq)
#     print(res)
#     return res.text

# 将图片转为base64编码
def encode_image(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except:
        print("图片路径错误")

# 判断是否默认开启app有利的隐私设置
def check_violate_privacy_preserving_by_default(path:str):
    """
    将指定路径下的图片交给LLM判断是否是默认开启选项，然后判断其是否侵犯了用户的隐私
    """
    # picture = encode_image(path)
    # chat_completion = client.chat.completions.create(
    #     model='gpt-4-vision-preview',
    #     messages=[{'role':'system',
    #             'content':[
    #                {'type': 'text',
    #                'text': 'Please analyze the content of the pop-up box in the provided image. If it includes any default'
    #                        ' selected options, return True otherwise return False, labeling as "default_setting:". In case'
    #                        ' of default settings being True, evaluate if these options are privacy settings beneficial to '
    #                        'the app but harmful to the user\'s privacy. Return True if they are beneficial to the app, '
    #                        'otherwise return False, labeling as "privacy_harmful_to_user:".'}
    #             ]},
    #             {'role': 'user',
    #             'content': [
    #                 {'type': 'image_url',
    #                  'image_url': {
    #                      'url': f'data:image/png;base64,{picture}'
    #                  }}
    #             ]}
    #     ]
    # )
    # chat_completion = client.chat.completions.create(
    #     model='gpt-4-vision-preview',
    #     messages=[{'role': 'user','content':  '能讲一个笑话吗'}]
    # )
    pop_up_scope = detect_pic(path)
    if pop_up_scope == None:
        print(path+" don't contains any pop-up")
        return -1
    bounds = pop_up_scope[0]['bounds']
    x=bounds[0]
    y=bounds[1]
    w=bounds[2]
    h=bounds[3]
    picture = encode_image(path)
    good_default_setting = encode_image("../res/good_default_setting.png")
    no_default_setting = encode_image('../res/no_default_setting.png')
    violate_default_setting = encode_image('../res/violate_default_setting.png')
    one_default_setting = encode_image('../res/one_default_setting.png')
    payload = {
        "model": 'gpt-4-vision-preview',
        # "model": 'gpt-3.5-turbo-instruct',
        "messages": [
            {'role':'system',
             'content':[
                 # {'type':'text','text':'Use the following step-by-step instructions to respond user inputs with the result in this format:step1:...,step2:...'},
                 # {'type':'text','text':'First - The user will provide you with an image containing a pop-up box. Please analyze the '
                 #                       'content of the pop-up box and determine if it includes any default selected options.'
                 #                       'If there is a default selected option, store the result with True otherwise with False, with the prefix "step1:".'},
                 # {'type':'text','text':'Then - IF the result of the Step 1 is False,return False with the prefix that says "step2:",'
                 #                       'If the result of the step 1 is True, then continue to evaluate whether these default enabled options'
                 #                       ' are privacy settings beneficial to the app. If they are beneficial to the app, return True;'
                 #                       ' otherwise return False, with the prefix "step2:".'}
                 # {'type': 'text',
                 #  'text': 'Use the following step-by-step instructions to respond user inputs with the result in this format:step1:...,step2:...'},
                 # {'type': 'text',
                 #  'text': 'Step1: The user will provide you with an image containing a pop-up box. Please analyze the '
                 #          'content of the pop-up box and determine if it includes any default selected options.'
                 #          'If there is a default selected option, store the result with True otherwise with False, with the prefix "step1:".'},
                 # {'type': 'text',
                 #  'text': 'Finally, based on the result of Step 1, please describe what will be the result in Step 2 and why?'
                 #          'Step 2: If the result of the step 1 is True, then evaluate whether these default enabled options'
                 #          ' are related to users privacy and beneficial to the app. If they are beneficial to the app itself and related to users privacy, return True;'
                 #          ' otherwise return False, with the prefix "step2:".'}
                {'type': 'text',
                # 'text':'The user will provide you one picture. This picture may contains some default selected settings(the setting which is highlight or more Conspicuous) or not.'
                #         'You are required to analysis the content of the pop-up box and ignore the contents of other areas that are not pop-ups, then get all the options and icons in the pop-up box(if it has).If the pop-up box contains any option which is selected by default,return True otherwise return False, labeling as "privacy_harmful_to_user:".'
                #         'If you return True, you should tell the user which option is selected.' # 21:55 0119
                # 'text':'The user will provide you one picture. This picture include a pop-up box and user will give you the pop-up\'s scope(x,y,w,h)'
                #        'and x and y is the start point\'s location,w and h is the pop-up\'s size. '
                #        'With the top left corner of the image as the origin, the positive direction of the x-axis is downwards, '
                #        'while the positive direction of the y-axis is right. The unit used is pixels.'
                #        'You should analysis the content within the pop-up and ignore other information that is out of the scope.'
                #        'This pop-up may contain some buttons or options or not. If the buttons'
                #        ' or options in this pop-up meet the following conditions, we consider that the option is selected by default: '
                #        'First, we only take the selectable options(eg:checkbox, radio button,and so on) into consideration. If there are '
                #        'selectable options within the pop-up that are directly selected(eg: radio button, checkbox,and so on). '
                #        'You need to extract all the options from the pop-up and ignore other information origion from the background, and then determine whether the options meet the above conditions.'
                #        'If the pop-up box contains any option which is selected by default,return True otherwise return False, labeling as "privacy_harmful_to_user:".'
                #        'If you return True, you should tell the user which option is selected. If you return False, you need to give the reason, too' # 19:39 0122

                 # 'text': 'The user will provide you with an image which includes a popup window. The user will tell you the range of the popup '
                 #         'box: (x,y,w,h) where x, y is a coordinate with the origin in the upper left corner of the image, the positive direction '
                 #         'of the x-axis is to the right, and the positive direction of the y-axis is to the downward; w,h represent the size of the popup '
                 #         'box and w is width, h is height; this range is in pixels. You need to ignore the entire content outside '
                 #         'the popup box and merely analyze the content within the range of the popup box. If this popup contains some optional items '
                 #         '(eg:checkbox, radio button,toggle switch, etc.), if there are any optional item are checked or selected or in the on position, return True otherwise return False, '
                 #         'labeling as "privacy_harmful_to_user:".'
                 #         'If you return True, you should tell the user which option is selected and where the option is. If you return False, you need to give the reason, too'  # 0124
                 'text': 'The user will provide you with an image which includes a popup window. You need to first identify the pop-up window and ignore the entire content outside '
                         'the popup box. If this popup contains some optional items '
                         '(eg:checkbox, radio button,toggle switch, etc.) are checked or selected or in the on position, return True otherwise return False, '
                         'labeling as "privacy_harmful_to_user:".'
                         'If you return True, you should tell the user which option is selected and where the option is. If you return False, you need to give the reason, too' # 0125 1513

                 # 'text':'The user will provide you one picture. This picture may contains some default selected settings or not.'
                 #        'You are required to analysis the content of the pop-up box and ignore the contents of other areas that are not pop-ups, then get all the options(if it has).If the pop-up box contains any option which is selected by default,return True otherwise return False, labeling as "privacy_harmful_to_user:".'
                 #        'If you return True, you should tell the user which option is selected.' # 21:21 0119
                # 'text': '"Privacy-preserving by default" is a principle adopted in the design and \            s '
                #         'and services, emphasizing the protection of user privacy without user intervention. This means that '
                #         'default settings and the fundamental behavior of systems prioritize respecting and safeguarding the'
                #         ' security of users\' personal information and data, rather than requiring users to take additional '
                #         'steps to protect their privacy.'
                #         'In a Pop-up box, if the box contains more than one option, none of the option should be selected by default'
                #         '. If there are more than one item in a pop-up box and some items were selected by default, we consider this pop-up box'
                #         'has violated the principle.'
                #         'If a popup requires user interaction to determine an option, then all the suboptions of the popup should not be selected by default, otherwise it is a violation of the principle. You should analysis the content of the Pop-up box and judge the box is violate the principle or not. If the popup design violates the principle, you need to return True, otherwise return False,labeling as "privacy_harmful_to_user:".'
                        # 'Under this approach, software, applications, or services automatically apply the strongest privacy '
                        # 'settings during initial configuration. This is contrary to practices that require users to manually'
                        # ' adjust settings for enhanced privacy protection. Privacy-preserving features may include data encryption,'
                        # ' anonymization techniques, data minimization, and confidential collection of user behavior.'
                        # 'Please analyze '
                        # 'the content of the pop-up box in the provided image. If it includes any default'
                        # ' selected options, return True otherwise return False, labeling as "default_setting:". In case'
                        # ' of default settings being True, then you should analysis the text and icon of the pop-up box to judge if the default selected options violate the "Privacy-preserving by default" principle. Return True if they violate the "Privacy-preserving by default" principle '     #are privacy settings beneficial to '
                        # # 'the app but harmful to the user\'s privacy or 
                        # 'otherwise return False, labeling as "privacy_harmful_to_user:".'
                        # 'According to the content of the pop-up window in the image, I want you to tell me if the pop-uo box violate the "Privacy-preserving by defaul" principle or not.'
                        # ' you should analysis the pop-up box and determine if it contains any default selected options.'
                        # 'If the pop-up box contains additional items and some have be selected, we consider it has violate the principle. You should retun True'
                        # ' if it hasn\'t violated the principle, you should return False, labeling as "privacy_harmful_to_user:".'
                        # '"default_setting:". '
                        # 'If the pop-up window contains '
                        # 'default settings and the default setting is selected or chosen,return True otherwise return False,labeling as "".'
                        # 'default options, continue analyzing its content to determine if the default enabled option violates the '
                        # '"Privacy-preserving by default" principle. If it does, return True otherwise return False, labeling as "privacy_harmful_to_user:".'
                        # ' If the pop-up window does not contain any default enabled options, return False, labeling as "privacy_harmful_to_user:".'
                        # 'You should note that you should respond according to the content of the pop-up window and try to avoid creating fictional scenarios as much as possible.'
                 }
             ]},
            # {'role':'user',
            #  'content':[
            #      {'type':'image_url',
            #       'image_url':
            #           {'url':f'data:image/png;base64,{good_default_setting}'}
            #       }
            #  ]},
            # {'role':'assistant',
            #  'content':[
            #      {'type':'text',
            #       'text':'default_setting: True\nThis image contains two options: "Do not close for now" and "Confirm closure". Among them, the option "Confirm closure" is highlighted, implying that users should choose this option. "\nprivacy_harmful_to_user": True\n Considering the text in the pop-up window, confirming closure will not bring any additional benefits to the app itself nor pose any privacy risks to the user.'}
            #  ]},
            # {'role': 'user',
            #  'content': [
            #      {'type': 'image_url',
            #       'image_url':
            #           {'url': f'data:image/png;base64,{one_default_setting}'}
            #       }
            #  ]},
            # {'role': 'assistant',
            #  'content': [
            #      {'type': 'text',
            #       'text': 'default_setting: True\nThis image contains one options: "找裹酱功能". And this option is selected by default, implying that users should choose this option. "\nprivacy_harmful_to_user": True\n Considering the text in the pop-up window, the chosen options may bring additional benefits to the app itself and it is not a essential option for user.'}
            #  ]},
            # {'role': 'user',
            #  'content': [
            #      {'type': 'image_url',
            #       'image_url':
            #           {'url': f'data:image/png;base64,{no_default_setting}'}
            #       }
            #  ]},
            # {'role': 'assistant',
            #  'content': [
            #      {'type': 'text',
            #       'text': 'default_setting: False\nThis image contains two options: Cancel and Allow, but neither of these options is highlighted or directly selected.Therefore this pop-up box has no default settings.\nprivacy_harmful_to_user": False\n According to the text information of this pop-up window, we cannot find any default selected options, and we cannot determine if it will compromise user privacy. Therefore, this pop-up window does not violate "privacy-preserving by-default".'}
            #  ]},
            # {'role': 'user',
            #  'content': [
            #      {'type': 'image_url',
            #       'image_url':
            #           {'url': f'data:image/png;base64,{violate_default_setting}'}
            #       }
            #  ]},
            # {'role': 'assistant',
            #  'content': [
            #      {'type': 'text',
            #       'text': 'default_setting: True\nThis pop-up window contains two main options: "暂时不用" and "立即开启", with the latter option highlighted. Additionally, there are two sub-options to determine the scope of notifications received: "全部（包含交易提醒、朋友消息提醒等）"  and "仅朋友消息提醒", with the former option selected by default. \nprivacy_harmful_to_user": True\n Based on the text of this pop-up window, we can see that it is an inquiry prompt asking for notification permissions from the user. However, the default selection leans towards granting greater permissions to the app itself, which may compromise user privac'}
            #  ]},
            {'role': 'user',
             'content': [
                 {'type': 'image_url',
                  'image_url': {
                      'url': f'data:image/png;base64,{picture}'
                  }},
                 # {'type':'text',
                 #  'text':f'pop-up scope:({x},{y},{w},{h})'}
             ]}
        ],
        "max_tokens": 300,
        'temperature': 0
    }
    responce = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,proxies=proxies,
                             json=payload)
    responce = responce.json()
    # if 'step2:True' in responce['choices'][0]['message']['content']:
    #     print(1)
    # elif 'step2:False' in responce['choices'][0]['message']['content']:
    #     print(2)
    # else:
    #     print(3)
    # result = json.loads(responce)
    # responce = chat_completion
    print(responce)
    if 'privacy_harmful_to_user: True' in responce['choices'][0]['message']['content']:
        responce['result']=True
    else:
        responce['result']=False
    return responce

def typePopUp(path:str,picture_name:str):
    """
    只进行弹窗分类
    Args:
        path:
        picture_name:

    Returns:

    """
    # picture_text = get_ocr_text(path)
    picture_text = getPopUpText(path)
    if picture_text == -1:
        print(path+"is None Pop-up")
        return
    # print("识别图片文本为：" + picture_text)
    classified = -1;
    # 判断是否是第二类弹窗
    for info in Info_list:
        if info in picture_text:
            classified = 1
            break
    for tags in Allow_list:
        if tags in picture_text:
            for delay in Delay_list:
                if delay in picture_text:
                    classified = 0
                    break
    # 判断是否是第一类弹窗
    if classified == -1:
        # for info in Info_list:
        #     if info in picture_text:
        #         classified = 1
        #         break
        for tags in Allow_list:
            if tags in picture_text:
                for delay in Delay_list:
                    if delay in picture_text:
                        classified = 0
                        break
    # 根据结果将图片保存到指定目录下
    content = ""
    if classified == 0:
        content = "allowOrQuery"
    elif classified == 1:
        content = "info"
    else:
        content = "abnormal"

    # 将图片放入指定路径下
    # destination_path = "../ClassificationResult/" + content + "/" + picture_name + '/' + picture_name + '.png'
    destination_path = "../ClassificationResult/" + content + "/" + picture_name + '.png'
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(path, 'rb') as picture:
        with open(destination_path, 'wb') as destination_file:
            shutil.copyfileobj(picture, destination_file)

def check_is_mislead(path,picture_name):
    picture_text = getPopUpText(path)
    if picture_text == -1:
        print(path + "is None Pop-up")
        return
    ans=False
    for text in picture_text:
        ans = check_is_mislead_text(text)
        if ans==True:
            break
    if ans ==True:
        content = "Mislead"
        print(ans)
    else:
        print(ans)
        content ="Not_mislead"
    destination_path = "../ClassificationResult/" + content+"/" + picture_name + '.png'
    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
    with open(path, 'rb') as picture:
        with open(destination_path, 'wb') as destination_file:
            shutil.copyfileobj(picture, destination_file)
    return ans
def getPopUpText(path:str):
    picture_text = get_ocr_text(path)
    # picture_text = picture_text.json()
    scope = detect_pic(path)
    # print(scope[0],scope[1],scope[2],scope[3])
    if scope != None:
        bounds = scope[0]['bounds']
        # print(bounds)
        x = bounds[0]
        y = bounds[1]
        # print(type(x))
        w = bounds[2]
        h = bounds[3]
    else:
        return -1
    picture_text = picture_text.json()
    text_list = picture_text['res']
    ans = []
    for text in text_list:
        text_x = text['xywh'][0]
        text_y = text['xywh'][1]
        text_w = text['xywh'][2]
        text_h = text['xywh'][3]
        if x<=text_x and y<=text_y and x+w>= text_h+text_x and y+h>=text_y+text_w:
            ans.append(text['text'])
            # print(text)
            # ans+=" || \n"

    # print("识别图片文本为：" + picture_text.text)
    return ans
    # return picture_text.text

def classification(path:str,picture_name:str):
    """
    Args:
        path: 需要进行解析的图片路径
        picture_name:需要解析的图片名称
    Returns:
        无返回值，会根据不同的弹框类型将图片放入不同的文件夹下
    """
    # picture_text = get_ocr_text(path)
    # picture_text = picture_text.json()
    # scope = detect_pic(path)
    # if scope!=None:
    #     bounds = scope[0]['bounds']
    #     x = bounds[0]
    #     y = bounds[1]
    #     w = bounds[2]
    #     h = bounds[3]
    # print("识别图片文本为："+picture_text)

    picture_text = getPopUpText(path)
    if picture_text==-1:
        return

    classified = -1;
    # 判断是否是第一类弹窗
    for tags in Allow_list:
        if tags in picture_text:
            for delay in Delay_list:
                if delay in picture_text:
                    classified = 0
                    break
    # 判断是否是第二类弹窗
    if classified == -1:
        for info in Info_list:
            if info in picture_text:
                classified = 1
                break
    # 根据结果将图片保存到指定目录下
    content = ""
    if classified==0:
        content= "allowOrQuery"
    elif classified ==1:
        content="info"
    else:
        content="abnormal"

    # 将图片放入指定路径下
    # destination_path ="../ClassificationResult/"+content+"/"+picture_name+'/'+picture_name+'.png'
    destination_path = "../ClassificationResult/" + content + "/" + picture_name + '.png'
    os.makedirs(os.path.dirname(destination_path),exist_ok=True)

    with open(path,'rb') as picture:
        with open(destination_path,'wb') as destination_file:
            shutil.copyfileobj(picture,destination_file)
    # return None

    # 判断弹框是否存在问题：
    mislead = check_is_mislead_text(picture_text)
    privacy_harmful_to_user = check_violate_privacy_preserving_by_default(path)
    result={"mislead":mislead,"privacy_harmful_to_user":privacy_harmful_to_user['result'],"LLM judge result":privacy_harmful_to_user['choices'][0]['message']['content']}
    json_path ="../ClassificationResult/"+content+"/"+picture_name+'/result.json'
    # os.makedirs(json_path)
    with open(json_path,'w') as file:
        json.dump(result,file)

def testClassification(path:str):
    """
    读取文件路径下的图片，然后分类
    Args:
        path:
        picture_name:

    Returns:

    """
    current_path = path+"/ui_relations.txt"
    picture_path = ""
    with open(current_path,'r') as file:
        info_dict = json.load(file)
        # print(type(info_dict))
        picture_name = info_dict["to_img"]
        picture_text = info_dict["to_text"]
        picture_path = path+"/"+picture_name
        print(picture_path)
        picture_name = picture_name[:-4]
        # isMislead = check_is_mislead_text(picture_text)
        classified = -1;
        # 判断是否是第一类弹窗
        for tags in Allow_list:
            if tags in picture_text:
                for delay in Delay_list:
                    if delay in picture_text:
                        classified = 0
                        break
        # 判断是否是第二类弹窗
        if classified == -1:
            for info in Info_list:
                if info in picture_text:
                    classified = 1
                    break
        # 根据结果将图片保存到指定目录下
        content = ""
        if classified == 0:
            content = "allowOrQuery"
        elif classified == 1:
            content = "info"
        else:
            content = "abnormal"

        # 将图片放入指定路径下
        destination_path = "../ClassificationResult/" + content + "/" + picture_name + '/' + picture_name + '.png'
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        # path =
        with open(picture_path, 'rb') as picture:
            with open(destination_path, 'wb') as destination_file:
                shutil.copyfileobj(picture, destination_file)
        # return None

        # 判断弹框是否存在问题：
        mislead = check_is_mislead_text(picture_text)
        privacy_harmful_to_user = check_violate_privacy_preserving_by_default(picture_path)
        result = {"mislead": mislead, "privacy_harmful_to_user": privacy_harmful_to_user['result'],
                  "LLM judge result": privacy_harmful_to_user['choices'][0]['message']['content']}
        json_path = "../ClassificationResult/" + content + "/" + picture_name + '/result.json'
        # os.makedirs(json_path)
        with open(json_path, 'w') as file:
            json.dump(result, file)

def start_test(file_path:str):
    files = os.listdir(file_path)
    for file in files:
        current_dictory = file_path+'/'+file
        testClassification(current_dictory)

def start(file_path:str)->str:
    """
    传入保存图片的根目录，然后进行分类
    Returns:

    """
    # 一个图片一个目录
    # picture_paths =  os.listdir(file_path)
    # for picture in picture_paths:
    #     current_path = file_path+"/"+picture
    #     picture_name =picture[:-4]
    #     # print(current_path)
    #     print(picture_name)
    #     classification(current_path,picture_name)

    #所有图片在一个目录下
    picture_paths = os.listdir(file_path)
    empty_num = 0
    pop_up_num = 0
    for picture in picture_paths:
        if 'empty' in picture:
            empty_num+=1
            continue
        picture_name = picture[:-4]
        path = file_path+"/"+picture
        # 只进行弹框分类
        typePopUp(path,picture_name)
        # 只进行误导判断
        # ans = check_is_mislead(path,picture_name)
        print()

        pop_up_num+=1
    print("========================================")
    print(empty_num)
    print(pop_up_num)


if __name__=="__main__":
    # check_violate_privacy_preserving_by_default("../data_819/Images/3SlHCFFlMucd_UdD4AN_HbLeAUAqQW9-35D3A6Jq1lI=.png")
    # classification("../data_819/Images/3SlHCFFlMucd_UdD4AN_HbLeAUAqQW9-35D3A6Jq1lI=.png","3SlHCFFlMucd_UdD4AN_HbLeAUAqQW9-35D3A6Jq1lI=")
    # start("../data_819/Images")
    # start_test("../PopupContext")
    # start("../data_819/Images")

# LLM Test

    # pictures = os.listdir("../data_819/Images")
    pictures = os.listdir("../chosenPicture")
    for picture in pictures:
        path ="../data_819/Images/"+picture
        ans = check_violate_privacy_preserving_by_default(path)
        if ans==-1:
            continue
        picture_name = picture[:-4]
        result = {"privacy_harmful_to_user": ans['result'],
                  "LLM judge result": ans['choices'][0]['message']['content']}
        if ans['result'] == True:
            content = 'violate_defalut_setting'
        else:
            content='not_violate_default_setting'
        json_path = "../ClassificationResult/LLM/" + content + "/" + picture_name + '/result.json'
        destination_path = "../ClassificationResult/LLM/" + content + "/" + picture_name + '/' + picture
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        with open(path, 'rb') as picture:
            with open(destination_path, 'wb') as destination_file:
                shutil.copyfileobj(picture, destination_file)
        # os.makedirs(json_path)
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as file:
            json.dump(result, file)

# 弹框文本识别测试：
#     getPopUpText("../ClassificationResult/abnormal/IJ_98qXqlmIu4czlvm7m58DKNYGkyCybI0UfGcz005k=.png")

# 弹框分类


# payload = {
#          "model": 'gpt-4-vision-preview',
#          "messages": [
#              {'role': 'user',
#               'content': [
#                   {'type': 'text', 'text': '我点击了一个应'},
#                   {'type': 'text', 'text': '然后这是跳转后的界面,里面包含一个弹窗'},
#                   {'type': 'image_url',
#                    'image_url': {
#                        'url': f'data:image/png;base64,{encode_image(file + flash + "/" + to_image)}'
#                    }},
#                   {'type': 'text',
#                    # 'text': '根据提供的界面截图信息，判断弹框内容是否与预期的核心功能相关，并评估弹框的性质但是不用告诉我评估结果。如果弹框内容与核心功能无关、是广告或有其他不良行为，请返回False；否则，返回True。'
#                    'text': '根据提供的界面截图信息，判断弹框内容是否与预期的核心功能相关、是否存在诱导和广告。如果弹框内容与核心功能无关、是广告或有其他不良行为，请返回False；否则，返回True。注意，你只需要回答True或者False，而不要其他的分析性语句'
#                    }
#               ]
#               # 'content':[
#               #     {'type':'text','text':ques}
#               # ]
#               }
#          ],
#          "max_tokens": 20,
#          'temperature': 0.1
# }