#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import os.path
import pickle

def print_help():
    print(f'Usage:')
    print(f'{sys.argv[0]} <video file name>')

def main_loop(file_name):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    capture = cv2.VideoCapture(file_name)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print(length)
    i = 1
    while(capture.isOpened()):
        ret, frame = capture.read()
        print(f'{i}/{length}',end='\r')
        i+=1
        if ret:
            faces = face_cascade.detectMultiScale(frame,scaleFactor= 1.4, minNeighbors=3)#,minSize= (20,20))
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.imshow('frame',frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
            break
    capture.release()
    cv2.destroyAllWindows()
    print()

def save_faces(faces):
    print()

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
