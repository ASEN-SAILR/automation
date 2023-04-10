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
imgs= ['img.jpg','img1.jpg','img2.jpg']
for i in  range(len(imgs)):
    imgs.append(cv2.imread(imgs[i]))
    imgs[i] = cv2.resize(imgs[i],(0,0),fx=0.4,fy=0.4)



stitchy = cv2.Stitcher.create()
(d, output) = stitchy.stitch([frame1,frame,frame2])


print(d)
#cv2.imwrite('panoReal.jpg',output)
cv2.imshow('Final',output)




