import numpy as np
import cv2

capture = cv2.VideoCapture(-1)
result,frame=capture.read()
	
cv2.resize(frame, (1920,1080))

cv2.imwrite('testphoto.jpg',frame)

cv2.imshow('1',frame)




