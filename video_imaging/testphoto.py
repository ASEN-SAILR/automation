import numpy
import cv2

cap0=cv2.VideoCapture(0)
re,frame0=cap0.read()
out=cv2.imwrite("/home/sailr/SeniorProjects/automation/images/testphoto.jpg",frame0)



