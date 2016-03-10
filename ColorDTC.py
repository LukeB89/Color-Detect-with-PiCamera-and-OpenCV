#!/usr/bin/python
from picamera.array import PiRGBArray
from matplotlib import pyplot as plt
from picamera import PiCamera
import DynamicObjectV2
import numpy as np
import os.path
import time
import cv2
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
Obj = DynamicObjectV2.Class

widths = 440
heigths = 280

resX = 6
resY = 6
count = 0
imc = 0

hue = 0
sat = 0
val = 0
camera = PiCamera()
camera.resolution = (widths, heigths)
camera.framerate = 32
camera.hflip = True
rawCapture = PiRGBArray(camera, size=(widths, heigths))

time.sleep(0.1)
def dec_conv(x):
    return format(x, '03d')

def init(self):
    # put your self.registerOutput here
    self.registerOutput("colourDTC", Obj("R", 0, "G", 0, "B", 0))

def run (self):
    # put your init and global variables here
    
    # main loop
    while 1:
            # capture frames from the camera
        for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                # This is used to store the index of the largest face found
                # This is considered in later code to be the face of interest
                #largestFaceIdx = -1
                
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                frame = image.array
                size = 20
                x = (widths/2)- size
                y = (heigths/2) - size
                w = (widths/2) + size
                h = (heigths/2) + size

                
                # This block grabs an image from the camera and prepares
                # a grey version to be used in the face detection.
                #(ret,frame) = cam.read()
                
    ##            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                blr = cv2.blur(frame,(10,10))
                cv2.rectangle(frame,(x,y),(w,h),(255,0,0),1)
                cv2.line(frame, (x,y),(w,h),(255,0,0),1)
                cv2.line(frame, (x,h),(w,y),(255,0,0),1)
                cv2.circle(frame, (220, 140),2,(0,255,0),2)

                maskd = np.zeros(blr.shape[:2], np.uint8)
                maskd[130:150, 210:230] = 255
                con = cv2.mean(blr,mask = maskd)
                Red = dec_conv(int(con[2]))
                Gre = dec_conv(int(con[1]))
                Blu = dec_conv(int(con[0]))
                self.output("colourDTC",Obj("R",Red,"G",Gre,"B",Blu))
##                print "B=%d, G=%d, R=%d" %(con[0],con[1],con[2])


                cv2.imshow('frame', frame)
                
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)

                
                # Check for keypresses
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    print "Q Pressed"
                    break
                

        print "Quitting..."
        '''cam.release()'''
        break
        cv2.destroyAllWindows()
