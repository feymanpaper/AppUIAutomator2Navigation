from DeviceHelper import *
# 任务:
# 实现一个屏幕截图功能, 注: uiautomator2具有截图功能
# 要求实现截图, 并且将截图命名为encode_screen_uid(screen_uid),即编码当前界面信息的字符串,并且将文件保存在Screenshot目录下(目录不存在则程序自动创建)
# 并且encode_screen_uid(screen_uid)能够进行解码回screen_uid, 即decode_screen_uid(encode_screen_uid(screen_uid)) = screen_uid
# 编码解码格式可以自行选择
# 测试可以在test/ScreenshotUtils_test.py上进行测试, 不需要跑其他文件
class ScreenshotUtils:

    @staticmethod
    def get_screen_uid():
        '''
        Description: 该方法返回当前界面信息(可点击组件的文本和位置)
        '''
        cur_ck_eles = get_clickable_elements()
        cur_ck_eles = remove_dup(cur_ck_eles)
        cur_ck_eles = merged_clickable_elements(cur_ck_eles)
        ck_eles_text = to_string_ck_els(cur_ck_eles)
        return ck_eles_text

    @staticmethod
    def screen_shot(screen_uid:str):
        #TODO
        pass

    @staticmethod
    def encode_screen_uid(screen_uid:str)->str:
        #TODO
        pass

    @staticmethod
    def decode_screen_uid(encode_str:str)->str:
        #TODO
        pass