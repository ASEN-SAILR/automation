
import cv2
import numpy as np

#port = list of camera ID from /dev

cam0 = cv2.VideoCapture()
cam0.open(0)

cam1 = cv2.VideoCapture()
cam1.open(1)

cam2 = cv2.VideoCapture()
cam2.open(1)

# result2, frame2 = cv2.VideoCapture("USB\VID_0C45&PID_6366&MI_00"
result0,frame0 = cam0.read()
result1,frame1 = cam1.read()
result2,frame2 = cam2.read()

image_paths=[frame0,frame1,frame2]
print(type(frame0))
# initialized a list of images
imgs = []
 
for i in range(len(image_paths)):
    imgs.append(image_paths[i])
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