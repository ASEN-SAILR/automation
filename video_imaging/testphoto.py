import numpy
import cv2
import time

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS,30)
out = cv2.VideoWriter("testVid.avi",cv2.VideoWriter_fourcc(*'XVID'),30,(640,480))
start = time.time()
while time.time()-start<5:
    ret,frame = cap.read()
    out.write(frame)

cap.release()
out.release()





