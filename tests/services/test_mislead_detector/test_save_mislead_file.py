import sys
sys.path.append('C:\\Codelife\\ui')
from services.mislead_detector import save_mislead_file

abs_path = "collectData\com.alibaba.aliyun-20231202-003938\Screenshot\ScreenshotPicture"
from_img = "0IfqneiOmh6xX4VulvUwX41EwIHFKt4C7TNY3BWX53o=.png"
to_img = "0UGIAyuB3G077ow6mMUnRMnQyYLdmz2ZHFhLjUi1prY=.png"
click_xy = (255, 255)
res = save_mislead_file.save_mislead_file(abs_path, from_img, to_img, click_xy)

assert res is not None