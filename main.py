import numpy as np
import cv2
from mss import mss
from PIL import Image

sct = mss()

mon = sct.monitors[1]

while 1:
    sct_img = sct.grab(mon)
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    cv2.imshow('test', np.array(img))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
