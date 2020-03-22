import cv2
import numpy as np
import os
import pathlib
import qrcode
import shutil
import socket
import tempfile
import threading
from flask import Flask, render_template, jsonify
from mss import mss
from PIL import Image


def capture(upload_folder):
    sct = mss()
    mon = sct.monitors[1]
    full_filename = os.path.join(upload_folder, "current.png")
    redundant_filename = os.path.join(upload_folder, "redundant.png")
    while 1:  # Take a screenshot, then immediately take another
        sct_img = sct.grab(mon)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        tp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tp.name)  # Save to a temporary file
        try:
            # Once it's ready begin copying to the displayed image location in
            # static.
            shutil.copy(tp.name, os.path.join(os.getcwd(), full_filename))
            # This redundant image fills in if the UI makes a request for an
            # image and it isn't ready yet, filling in the gap with the
            # previously seen image.
            shutil.copy(tp.name, os.path.join(os.getcwd(), redundant_filename))
        except OSError:
            pass
        tp.close()


def open_code():
    cv2.startWindowThread()
    cv2.namedWindow("Scan this code to access your display")
    im = cv2.imread("displaycode.png")
    imS = cv2.resize(im, (540, 540))
    cv2.imshow("Scan this code to access your display", imS)
    cv2.waitKey(0)


IMAGE_FOLDER = os.path.join("static", "screenimgs")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = IMAGE_FOLDER


@app.route("/")
@app.route("/index")
def show_index():
    return render_template("index.html")


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
    # Serve at a local public IP
    qr.add_data("http://" + localip + ":5000")
    qr.make(fit=True)
    qrimg = qr.make_image(fill_color="black", back_color="white")
    qrimg.save("displaycode.png")
    # Capture and the CV window run in seperate threads so that the server
    # is ready for the user
    cyprocess = threading.Thread(target=open_code, args=())
    cyprocess.daemon = True
    cyprocess.start()  # Start the execution
    captureprocess = threading.Thread(
        target=capture, args=(app.config["UPLOAD_FOLDER"],)
    )
    captureprocess.daemon = True
    captureprocess.start()
    app.run(host=localip, use_reloader=False, debug=True)
