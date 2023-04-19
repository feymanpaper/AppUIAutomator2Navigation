import sys 
sys.path.append("..")
from ScreenCompareStrategy import *


str1 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
str2 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
ab = ScreenCompareStrategy(LCSComparator())
res, ratio = ab.compare_screen(str1, str2)
print(f"The result is {res} and {ratio}")

str3 = "   旧设备扫码验证发送短信验证人工申诉 联系客服 "
str4 = "   旧设备扫码验证发送短信验证人工申诉 联系客服 我知道了 "
res, ratio = ab.compare_screen(str3, str4)
print(f"The result is {res} and {ratio}")


str3 = "+8618033138368 请输入密码 登录忘记密码 我已阅读并同意服务协议, 隐私权政策 专属帐号 注册帐号 更多选项 加入会议"
str4 = "root"

str3 = '搜索 热门国家和地区中国+86日本+81中国台湾+886中国香港+852马来西亚+60印度尼西亚+62印度+91菲律宾+63泰国+66美国+1A阿尔巴尼亚+355阿尔及利亚+213'
str4 = '\ue899 \ue899  旧设备扫码验证发送短信验证人工申诉 联系客服 '

res, ratio = ab.compare_screen(str3, str4)
print(f"The result is {res} and {ratio}")