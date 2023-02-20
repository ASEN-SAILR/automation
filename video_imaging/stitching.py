
import cv2
import numpy as np

cam_port0=0
cam_port1=1
cam_port2=2
result0, frame0 = cv2.VideoCapture(cam_port0)
result1, frame1 = cv2.VideoCapture(cam_port1)
result2, frame2 = cv2.VideoCapture(cam_port2)

image_paths=[frame0,frame1,frame2]

# initialized a list of images
imgs = []
 
for i in range(len(image_paths)):
    imgs.append(cv2.imread(image_paths[i]))
    imgs[i]=cv2.resize(imgs[i],(0,0),fx=0.2,fy=0.2)
    # this is optional if your input images isn't too large
    # you don't need to scale down the image
    # in my case the input images are of dimensions 3000x1200
    # and due to this the resultant image won't fit the screen
    # scaling down the images
# showing the original pictures
cv2.imshow('1',imgs[0])
cv2.imshow('2',imgs[1])
cv2.imshow('3',imgs[2])
 
stitchy=cv2.Stitcher.create()
(dummy,output)=stitchy.stitch(imgs)
 
if dummy != cv2.STITCHER_OK:
  # checking if the stitching procedure is successful
  # .stitch() function returns a true value if stitching is
  # done successfully
    print("Stitching was not successful")
else:
    print('Your Panorama is ready!!!')
 
# final output
cv2.imwrite('Pano.jpg',output)
# save output as .jpg
cv2.imshow('final result',output)

cv2.waitKey(0)