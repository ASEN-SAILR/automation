import numpy
import cv2
import time

cap=cv2.VideoCapture(0)
ret,frame = cap.read()
cv2.imwrite('img.jpg',frame)
cap.release()
cap1=cv2.VideoCapture(4)
ret1,frame1 = cap1.read()
cv2.imwrite('img1.jpg',frame1)
cap1.release()
cap2=cv2.VideoCapture(8)
ret2,frame2 = cap2.read()
cv2.imwrite('img2.jpg',frame2)

cap2.release()
imgs_paths= ['img.jpg','img1.jpg','img2.jpg']
imgs=[]
output=cv2.hconcat(imgs_paths)
#cv2.imwrite('panoReal.jpg',output)
cv2.imwrite('panoReal.jpg',output)




