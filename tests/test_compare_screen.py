import sys 
sys.path.append("..")
from ScreenCompareStrategy import *

str1 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
str2 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
ab = ScreenCompareStrategy(LCSComparator())
res, ratio = ab.compare_screen(str1, str2)
print(ratio*100, "%")


str1 = "   旧设备扫码验证发送短信验证人工申诉 联系客服 "
str2 = "   旧设备扫码验证发送短信验证人工申诉 联系客服 我知道了"
res, ratio = ab.compare_screen(str2, str1)
print(ratio*100, "%")

str1 = "+8118033138368 请输入密码 登录忘记密码 我已阅读并同意服务协议, 隐私权政策 专属帐号 注册帐号 更多选项 加入会议"
str2 = "+8618033138368 请输入密码 登录忘记密码 我已阅读并同意服务协议, 隐私权政策 专属帐号 注册帐号 更多选项 加入会议"
res, ratio = ab.compare_screen(str1, str2)
print(ratio*100, "%")