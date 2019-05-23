# USAGE
# python opencv_object_tracking.py
# python opencv_object_tracking.py --video dashcam_boston.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy
import face_recognition



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
        help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
        help="OpenCV object tracker type")
args = vars(ap.parse_args())
track_list = []
name_list = []
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


def make_name():
        name = ''
        while(True):

                key = cv2.waitKeyEx() & 0xFF

                if(key==13):
                        break
                z = chr(key)
                name = name + z
        return name

# extract the OpenCV version info
def make_tracker():
        (major, minor) = cv2.__version__.split(".")[:2]

# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
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
# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)

# otherwise, grab a reference to the video file
else:
        vs = cv2.VideoCapture(args["video"])

# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        frame = vs.read()
        frame = frame[1] if args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
                break

        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]

        if len(track_list) <1:
                face_locations = face_cascade.detectMultiScale(frame, 1.3, 5)
                # start OpenCV object tracker using the supplied bounding box
                # coordinates, then start the FPS throughput estimator as well
                for (x,y,w,h) in face_locations:
                        initBB = (x,y,w,h)
                        tracker  = make_tracker()
                        print(type(tracker))
                        tracker.init(frame, initBB)
                        track_list.append(tracker)
                        name_list.append('twarz')
                

        # check to see if we are currently tracking an object
        if True:
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
                # update the FPS counter
                        i +=1
                        



        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF


        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        '''
        if key == ord("s"):
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                        showCrosshair=True)

                # start OpenCV object tracker using the supplied bounding box
                # coordinates, then start the FPS throughput estimator as well
                tracker  =make_tracker()
                tracker.init(frame, initBB)
                track_list.append(tracker)
                name_list.append(make_name())
                fps = FPS().start()
        '''
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

# if we are using a webcam, release the pointer
if not args.get("video", False):
        vs.stop()

# otherwise, release the file pointer
else:
        vs.release()

# close all windows
cv2.destroyAllWindows()
