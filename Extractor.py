#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import os.path
import pickle

def print_help():
    print('Face Extractor')
    print(f'Usage:')
    print(f'Extractor.py <video file name> <output file name>')

def main_loop(src_file, output):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    capture = cv2.VideoCapture(src_file)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    file = open(output+'.pkl','ab')
    i = 0
    while(capture.isOpened()):
        ret, frame = capture.read()
        print(f'{i}/{length}',end='\r')
        i+=1
        if ret:
            faces = face_cascade.detectMultiScale(frame,scaleFactor= 1.4, minNeighbors=3)
            for (x,y,w,h) in faces:
                save_face(frame[y:(y+h),x:(x+w)],file)
        else:
            break
    capture.release()
    file.close()
    print()

def save_face(face, file):
    pickle.dump(face,file)

def main():
    if len(sys.argv)<3:
        print_help()
        sys.exit()

    if(os.path.isfile(sys.argv[1])):
        main_loop(sys.argv[1],sys.argv[2])
    else:
        print('No such file!')
        print_help()


main()
