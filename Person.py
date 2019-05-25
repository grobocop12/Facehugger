from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy


class Person:
    imgpathlist=[]
    imglist=[]
    label =0
    name =''
    facelist = []
    def __init__(self,imgpaths,name,label):
        self.name=name
        self.label = label
        self.imgpathlist=imgpaths
        for image_path in imgpaths:
            image = cv2.imread(image_path)
            self.imglist.append(image)
            face, rect = self.detect_face(image)
            if face is not None:
                self.facelist.append(face)


    def detect_face(self,img):
        # convert the test image to gray image as opencv face detector expects gray images
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # load OpenCV face detector, I am using LBP which is fast
        # there is also a more accurate but slow Haar classifier
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

        # let's detect multiscale (some images may be closer to camera than others) images
        # result is a list of faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

        # if no faces are detected then return original img
        if (len(faces) == 0):
            return None, None

        # under the assumption that there will be only one face,
        # extract the face area
        (x, y, w, h) = faces[0]

        # return only the face part of the image
        return gray[y:y + w, x:x + h], faces[0]

    def GetFaces(self):
        return self.facelist

    def GetRecData(self):
        labelist = []
        for f in self.facelist:
            labelist.append(self.label)
        return self.facelist,labelist

