from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy
import Person


def make_name():
    name = ''
    while (True):

        key = cv2.waitKeyEx() & 0xFF

        if (key == 13):
            break
        z = chr(key)
        name = name + z
    return name

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
    if confidence>50:
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


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
            help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
            help="OpenCV object tracker type")
args = vars(ap.parse_args())

def Start(Persons):




    track_list = []
    name_list = []
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')

    face_recognizer,dict = makerecognizer(Persons)

    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(0.01)
    cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
    while True:
        frame = vs.read()
        if frame is None:
            break

        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]
        if(True):

            i = 0
            tracpos=[]
            for one_tracker in track_list:
                (success, box) = one_tracker.update(frame)
                tag = name_list[i]
                # check to see if the tracking was a success
                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    tracpos.append((x, y, w, h))
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, tag, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                else:
                    name_list.remove(tag)
                    track_list.remove(one_tracker)
                i += 1

            face_locations = face_cascade.detectMultiScale(frame, 1.3, 5)
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for (x, y, w, h) in face_locations:
                face = gray[y:y + w, x:x + h]
                personId = predict(face, face_recognizer)

                istargeted =False
                k = 0
                for i in tracpos:

                    (x1, y1, w1, h1) = i
                    if((x1 < x+0.5*w < x1+w1)and (y1<y+0.5*h<y1+h1)and (x < x1+0.5*w1 < x+w)and (y<y1+0.5*h1<y+h) ):
                        istargeted =True
                        if(name_list.__len__()>0):
                            if(personId!=None and not(dict.get(personId)in name_list) and name_list[k]=="Unknow"):
                                name_list.remove(name_list[k])
                                track_list.remove(track_list[k])
                                print('podmiana')
                                print(personId)
                            else:
                                continue

                    k = k +1


                if((personId != None)and istargeted ==False ):
                    if not(dict.get(personId)in name_list):
                        initBB = (x, y, w, h)
                        tracker = make_tracker()
                        print(type(tracker))
                        tracker.init(frame, initBB)
                        track_list.append(tracker)
                        name_list.append(dict.get(personId))
                    else:
                        initBB = (x, y, w, h)
                        tracker = make_tracker()
                        print(type(tracker))
                        tracker.init(frame, initBB)
                        track_list.append(tracker)
                        name_list.append("Unknow")
                if(personId==None and istargeted ==False):
                    initBB = (x, y, w, h)
                    tracker = make_tracker()
                    print(type(tracker))
                    tracker.init(frame, initBB)
                    track_list.append(tracker)
                    name_list.append("Unknow")


                    # grab the new bounding box coordinates of the object

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if key == ord("s"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                                   showCrosshair=True)

            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            tracker = make_tracker()
            tracker.init(frame, initBB)
            track_list.append(tracker)
            name_list.append(make_name())
