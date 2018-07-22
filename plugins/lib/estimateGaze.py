#Import required modules
import cv2
import sys
import dlib
import numpy as np
import time, threading
from multiprocessing import Process, Queue
import thread
import os
import time

NOSE=30
RIGHT_EYE=36
LEFT_EYE=45
MOUTH_RIGHT=48
MOUTH_LEFT=54
MENTON=8

#Detect the facial feature in an image (processing done in a dedicated process)
def detect(detector,image,queue):
    detections = detector(image,1)
    #Put results in queue to be recovered in the main thread
    queue.put(detections)

class GetGaze():
    def __init__(self,controller = None):
        print('GAZE ESTIMATOR CREATED')
        #get path to look for the predictor
        dir_path = os.path.dirname(os.path.realpath(__file__))

        #Set up some required objects
        global detector
        detector = dlib.get_frontal_face_detector() #Face detector

        self.predictor = dlib.shape_predictor(dir_path + "/shape_predictor_68_face_landmarks.dat") #Landmark identifier. Set the filename to whatever you named the downloaded file

        #self.go_on = True
        self.video_capture = cv2.VideoCapture(0)
        #Get camera setings (resolution)
        ret, frame = self.video_capture.read()
        self.video_capture.release()
        size = frame.shape

        #Define constants for image processing
        focal_length = size[1]
        center = (size[1]/2, size[0]/2)

        self.camera_matrix = np.array(
                                 [[focal_length, 0, center[0]],
                                 [0, focal_length, center[1]],
                                 [0, 0, 1]], dtype = "double"
                                 )
        self.dist_coeffs = np.zeros((4,1))

        #Prototypic location of points used for orientation estimation
        self.model_points = np.array([
                        (0.0, 0.0, 0.0),             # Nose tip
                        (0.0, -330.0, -65.0),        # Chin
                        (-225.0, 170.0, -135.0),     # Left eye left corner
                        (225.0, 170.0, -135.0),      # Right eye right corne
                        (-150.0, -150.0, -125.0),    # Left Mouth corner
                        (150.0, -150.0, -125.0)      # Right mouth corner
                    ])

        #Stopping variable
        self.shouldStop = False

        #Controller to feed back the results of the head gaze
        self.controller = controller

    def start(self):
        #Queue to return the variable from the process
        print("GAZE ESTIMATOR CREATED")
        queue = Queue()

        #Open video
        video_capture = cv2.VideoCapture(0)
        look_away =None
        while True:

            print("ENTER WHILE GAZE ESTIMATOR")
            #Get an image
            ret, frame = video_capture.read()

            #Preparation of the image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            clahe_image = clahe.apply(gray)

            #Start detection of faces in a dedicated process
            process = Process(target = detect,args=(detector,clahe_image,queue))
            process.start()
            process.join()

            #Recover results from the detection
            detections = queue.get()

            for k,d in enumerate(detections): #For each detected face

                shape = self.predictor(clahe_image, d) #Get coordinates

                image_points = np.array([
                                    (shape.part(NOSE).x, shape.part(NOSE).y),     # Nose tip
                                    (shape.part(MENTON).x, shape.part(MENTON).y),     # Chin
                                    (shape.part(LEFT_EYE).x, shape.part(LEFT_EYE).y),     # Left eye left corner
                                    (shape.part(RIGHT_EYE).x, shape.part(RIGHT_EYE).y),     # Right eye right corne
                                    (shape.part(MOUTH_LEFT).x, shape.part(MOUTH_LEFT).y),     # Left Mouth corner
                                    (shape.part(MOUTH_RIGHT).x, shape.part(MOUTH_RIGHT).y)      # Right mouth corner
                                ], dtype="double")

                rvec = np.array([[1.2],[1.2],[-1.2]])
                tvec = np.array([[0],[0],[1000]])

                #Comparison between observed features and theoretical position to obtain rotation difference
                (success, rotation_vector, translation_vector)  = cv2.solvePnP(self.model_points, image_points, self.camera_matrix, None, None, None, False, cv2.SOLVEPNP_ITERATIVE)

                #print "Rotation Vector:\n {0}".format(rotation_vector[0])
                #print "Translation Vector:\n {0}".format(translation_vector)

                #Compare difference of angle on x to a threshold to estimate if the person if looking
                threshold = -.1
                look_away = rotation_vector[0]>threshold

            #Reaction to angle
            if self.controller == None:
                if look_away:
                    print "look straigth"
                else:
                    print "fine"
            else:
                print("CONTROLLER GAZE ESTIMATOR")
                if look_away:
                    print("HEAD GAZE")
                    self.controller.headGaze(look_away)
                else:
                    print('fine fine fine')

            #Check if loop should be stopped
            if (cv2.waitKey(1) & 0xFF == ord('q')) or self.shouldStop: #Exit program when the user presses 'q'
                break

    def stop(self):
        print "Stopping"
        self.shouldStop = True


def main():
    gg =  GetGaze()
    gg.start()

if __name__ == '__main__':
    main()
