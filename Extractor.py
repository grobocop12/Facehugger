#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import os.path
import pickle
import face_recognition

def print_help():
    print('Face Extractor')
    print(f'Usage:')
    print(f'Extractor.py <video file name> <output .pkl file name>')

def main_loop(src_file, output):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    capture = cv2.VideoCapture(src_file)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    file = open(output,'ab')
    i = 0
    while(capture.isOpened()):
        ret, frame = capture.read()
        print(f'{i}/{length}',end='\r')
        i+=1
        if ret:
            faces = face_recognition.face_locations(frame)
            for (top, right, bottom, left) in faces:
                save_face(frame[ top:bottom, left:right ], file)
                
        else:
            break
    capture.release()
    file.close()
    print()

def save_face(face, file):
    pickle.dump(face, file)

def main():
    if len(sys.argv)<3:
        print_help()
        sys.exit()
    output = sys.argv[2]
    
    if not output.endswith('.pkl'):
        output = output + '.pkl'
    if(os.path.isfile(sys.argv[1])):
        main_loop(sys.argv[1],output)
    else:
        print('No such file!')
        print_help()


main()
