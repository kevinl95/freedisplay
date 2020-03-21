import numpy as np
import os
import pathlib
import qrcode
import socket
from multiprocess import Process, Value
from flask import Flask, render_template, jsonify

IMAGE_FOLDER = os.path.join("static", "screenimgs")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = IMAGE_FOLDER


@app.route("/")
@app.route("/index")
def show_index():
    return render_template("index.html")


def capture(app):
    from mss import mss
    from PIL import Image
    import tempfile
    import shutil
    import os

    sct = mss()
    mon = sct.monitors[1]
    full_filename = os.path.join(app.config["UPLOAD_FOLDER"], "current.png")
    redundant_filename = os.path.join(app.config["UPLOAD_FOLDER"], "redundant.png")
    while 1:
        sct_img = sct.grab(mon)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        tp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tp.name)
        try:
            shutil.copy(tp.name, os.path.join(os.getcwd(), full_filename))
            shutil.copy(tp.name, os.path.join(os.getcwd(), redundant_filename))
        except OSError:
            pass
        tp.close()


def open_code():
    import cv2

    cv2.startWindowThread()
    cv2.namedWindow("Scan this code to access your display")
    cv2.imshow("Scan this code to access your display", cv2.imread("displaycode.png"))
    cv2.waitKey(0)


if __name__ == "__main__":
    pathlib.Path(IMAGE_FOLDER).mkdir(parents=True, exist_ok=True)
    screenshot = os.path.join(IMAGE_FOLDER, "current.png")
    if os.path.isfile(screenshot):
        os.remove(screenshot)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localip = s.getsockname()[0]
    s.close()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    qr.add_data("http://" + localip + ":5000")
    qr.make(fit=True)
    qrimg = qr.make_image(fill_color="black", back_color="white")
    qrimg.save("displaycode.png")
    cvprocess = Process(target=open_code)
    captureprocess = Process(target=capture, args=(app,))
    captureprocess.start()
    cvprocess.start()
    app.run(host=localip, use_reloader=False, debug=True)
    cvprocess.join()
    captureprocess.join()
