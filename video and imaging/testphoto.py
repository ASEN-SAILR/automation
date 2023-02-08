import numpy as np
import cv2

capture = cv2.VideoCapture(0)
result,frame=capture.read()

cv2.imwrite('testphoto.jpg',frame)

cv2.imshow('1',frame)




