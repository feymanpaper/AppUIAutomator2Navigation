import json

import requests



def get_ocr_text(file_path:str):
    img1 = open(file_path, 'rb')
    file_resq = {
        "file": img1
    }
    res = requests.post("http://172.16.108.178:3333/ocr", files=file_resq)
    # print(res.text)
    return res
if __name__ == '__main__':
    file_path = './_KXdr4VcB3my3_7S5ZJBq-7mDATExc9Qzchy_25uRqw=.png'

    img1 = open(file_path, 'rb')
    file_resq = {
        "file": img1
    }
    res = requests.post("http://172.16.108.178:3333/ocr", files=file_resq)
    print(type(res.json()))
    print(res.json())