import cv2
import threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID,cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
        cv2.imwrite('frame'+str(camID)+'.jpg',frame)
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread3 = camThread("Camera 3", 2)
thread1.start()
thread2.start()
thread3.start()

image_paths=['frame0.jpg','frame1.jpg','frame3.jpg']
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

