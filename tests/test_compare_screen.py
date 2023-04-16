import sys 
sys.path.append("..")
import ScreenCompareStrategy

str1 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
str2 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
diff = ScreenCompareStrategy.minEditDistance(str1, str2)
ratio = diff/len(str1)
print(ratio*100, "%")