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

# Create three threads as follows
thread1 = camThread("Camera 1", 0)
thread2 = camThread("Camera 2", 1)
thread3 = camThread("Camera 3", 2)
thread1.start()
thread2.start()
thread3.start()
imgs=['frame0.jpg','frame1.jpg','frame2.jpg']
pano = cv2.hconcat(imgs)
cv2.imshow(pano)