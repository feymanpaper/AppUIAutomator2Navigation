import cv2
import os


class Redraw:
    def __init__(self, input_image, xywh: [], conf):
        self.input_image = input_image
        self.xywh = xywh
        self.conf = conf
        self.pic_name = os.path.basename(input_image)

        # 解析输入路径
        path_parts = self.input_image.split("/")
        symbol = "/"
        folder_path = symbol.join(path_parts[:-2])

        # 构建输出路径
        output_folder = "ProcessedScreenshotPicture"
        output_dir = folder_path + "/" + output_folder
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.output_dir = output_dir

        # 标签路径
        pic_name_without_extension = os.path.splitext(self.pic_name)[0]
        self.label_path = folder_path + '/ProcessedScreenshotPicture/labels/' + pic_name_without_extension + '.txt'

    def redraw(self):

        output_folder = self.output_dir

        image_path = self.input_image
        label_path = self.label_path

        image = cv2.imread(image_path)

        if self.conf > 0:
            # 解析YOLO格式位置信息
            cx = self.xywh[0]
            cy = self.xywh[1]
            w = self.xywh[2]
            h = self.xywh[3]
            confidence = self.conf
            image_height, image_width, _ = image.shape
            left = int((cx - w / 2) * image_width)
            top = int((cy - h / 2) * image_height)
            right = int((cx + w / 2) * image_width)
            bottom = int((cy + h / 2) * image_height)
            # 绘制矩形框
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 10)
            # 绘制置信度
            text = f"Confidence: {confidence:.2f}"
            font_scale = 2
            font_thickness = 2
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            text_width, text_height = text_size
            cv2.putText(image, text, (left, top - 10 - text_height), cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                        (0, 0, 255), font_thickness)

        output_image_path = os.path.join(output_folder, self.pic_name)
        cv2.imwrite(output_image_path, image)


