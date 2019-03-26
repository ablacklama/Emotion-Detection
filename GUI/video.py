from PyQt5.QtCore import QThread, Qt, pyqtSignal
import cv2
from PyQt5.QtGui import QImage
import os
import numpy as np
import csv
from collections import Counter
class SharedData:
    def __init__(self):
        self.hasphoto = False
        self.photo = None

class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, PhotoShare, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.PhotoShare = PhotoShare
    def run(self):
        cap = cv2.VideoCapture(0)
        while self.isRunning:
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convert_to_qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


    def display(self, img, faces, numImages, lastlabel, saving):
        disp_img = np.copy(img)
        if len(faces) == 1:
            x, y, w, h = faces[0]
            savestr = ""
            if saving:
                savestr = "SAVED"
            cv2.rectangle(disp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(disp_img, lastlabel + "  {}".format(str(numImages)) + savestr,
                        (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 0))

        return disp_img
