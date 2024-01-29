# import requests
#
#
# def get_img_scope(image_path):
#     url = r"http://127.0.0.1:45678/detect"
#     # f = open(image_path,'rb')
#     files = {'file': open(image_path, 'rb')}
#     responce = requests.post(url,files=files)
#     return responce.json().get("data")
#
# if __name__=="__main__":
#     ans = get_img_scope("../data_819/Images/3SlHCFFlMucd_UdD4AN_HbLeAUAqQW9-35D3A6Jq1lI=.png")
#     print(ans)
# from detect_popup import detect_pic
# ans = detect_pic("../data_819/Images/3SlHCFFlMucd_UdD4AN_HbLeAUAqQW9-35D3A6Jq1lI=.png")
# print(ans)