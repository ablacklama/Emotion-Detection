from PyQt5.QtCore import QThread, Qt, pyqtSignal
import cv2
import numpy as np


class FaceDetectionThread(QThread):

    #changePixmap = pyqtSignal(QImage)

    def __init__(self, PhotoData, parent=None):
        QThread.__init__(self, parent=parent)
        self.PhotoData = PhotoData
        self.haar_cascade = cv2.CascadeClassifier(
            'data/haarcascade_frontalface_alt.xml')

    def biggerFace(self,faces):
        faces = np.array(faces)
        if faces.shape[0] < 2:
            return faces
        else:
            biggestFace = None
            biggestSize = 0
            for face in faces:
                size = face[2] * face[3]
                if size > biggestSize:
                    biggestFace = face
                    biggestSize = size
            return [biggestFace]

    def getFaceImg(self):
        if self.PhotoData.hasphoto:
            img = self.PhotoData.get_photo()

            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            faces = self.haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            faces = self.biggerFace(faces)

            if len(faces) == 1:
                x, y, w, h = faces[0]
                faceimg = gray[y:y + h, x:x + w]
                return np.copy(faceimg)
            else:
                return None


    def run(self):
        while True:
            #print(str(self.PhotoData) + "\n\n")
            self.PhotoData.set_face_image(self.getFaceImg())