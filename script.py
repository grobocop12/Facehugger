import cv2
import numpy as np
import sys
import os.path

def print_help():
    print(f'Usage:')
    print(f'{sys.argv[0]} <video file name>')

def main_loop(file_name):

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    capture = cv2.VideoCapture(file_name)

    while(capture.isOpened()):
        ret, frame = capture.read()

        if(frame is not None):
            faces = face_cascade.detectMultiScale(frame,scaleFactor= 1.1, minNeighbors=2,minSize= (10,10))
            print('Detected faces:', len(faces))
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