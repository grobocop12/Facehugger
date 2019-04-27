import cv2
import numpy as np
import sys
import os.path
import PyQt5
from PyQt5 import QtGui, QtCore, QtWidgets




def print_help():
    print(f'Usage:')
    print(f'{sys.argv[0]} <video file name>')

def main_loop(file_name):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    capture = cv2.VideoCapture(file_name)

    while(capture.isOpened()):
        ret, frame = capture.read()

        if(frame is not None):
            faces = face_cascade.detectMultiScale(frame,scaleFactor= 1.2, minNeighbors=3)#,minSize= (20,20))
            #print('Detected faces:', len(faces))
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    capture.release()
    cv2.destroyAllWindows()

def main():
    if len(sys.argv)<2:
        print_help()
        sys.exit()

    if(os.path.isfile(sys.argv[1])):
        main_loop(sys.argv[1])
    else:
        print('No such file!')
        print_help()


main()
