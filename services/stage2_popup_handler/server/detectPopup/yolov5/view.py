import io

import numpy as np
from PIL import Image
from django.http import HttpResponse,JsonResponse
import os
import cv2
from detectPopup.yolov5 import check_popup

def detect(request):
    if request.method == 'POST':
        img_bytes = request.FILES.get('file').read()
        img_buffer_numpy = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_buffer_numpy, cv2.IMREAD_UNCHANGED)
        res = []
        if img is not None:
            buttons = check_popup.detect_pic(img)
            if buttons is not None:
                res.extend(buttons)
        return JsonResponse({'data': res},safe=False)
    else:
        return HttpResponse("no file")
    return HttpResponse("not POST")