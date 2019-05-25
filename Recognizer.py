from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy
import Person

def makerecognizer(osoby):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    facelist = []
    labelist = []
    dict ={}

    for i in osoby:
        faces,labels = i.GetRecData()
        facelist.extend(faces)
        labelist.extend(labels)
        dict[labels[0]]=i.name

    face_recognizer.train(facelist,numpy.array(labelist))
    return face_recognizer, dict

def predict(face,face_recognizer):
    label, confidence = face_recognizer.predict(face)
    if confidence>90:
        return  label
    else:
        return None

def make_tracker():
    (major, minor) = cv2.__version__.split(".")[:2]
    if int(major) == 3 and int(minor) < 3:
        tracker = cv2.Tracker_create(args["tracker"].upper())

    # otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
    # approrpiate object tracker constructor:
    else:
        # initialize a dictionary that maps strings to their corresponding
        # OpenCV object tracker implementations
        OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
        }

        # grab the appropriate object tracker using our dictionary of
        # OpenCV object tracker objects
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

    return tracker





mojezdjcia = ['training-data/s3/1.jpg','training-data/s3/2.jpg','training-data/s3/3.jpg','training-data/s3/4.jpg']
imie = 'Kamil Szkaradnik'
id =1
osoba = Person.Person(mojezdjcia,imie,id)
Persons = [osoba]

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
        help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
        help="OpenCV object tracker type")
args = vars(ap.parse_args())
track_list = []
name_list = []
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

face_recognizer,dict = makerecognizer(Persons)

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(0.01)

while True:
    frame = vs.read()
    if frame is None:
        break

    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]
    if(Persons.__len__()>track_list.__len__()):



        face_locations = face_cascade.detectMultiScale(frame, 1.3, 5)
        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in face_locations:
            face = gray[y:y + w, x:x + h]
            personid = predict(face,face_recognizer)
            if(personid != None):
                initBB = (x, y, w, h)
                tracker = make_tracker()
                print(type(tracker))
                tracker.init(frame, initBB)
                track_list.append(tracker)
                name_list.append(dict.get(personid))
                # grab the new bounding box coordinates of the object
    i=0
    for one_tracker in track_list:
            (success, box) = one_tracker.update(frame)
            tag = name_list[i]
                # check to see if the tracking was a success
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
                cv2.putText(frame, tag, (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            i += 1
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

