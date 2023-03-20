# https://www.turing.com/kb/python-multiprocessing-vs-multithreading
# suphakan
from multiprocessing import Process
import cv2
import numpy as np
import time
import RoverComms
import threading


# class camThread(threading.Thread):
#     def __init__(self, previewName, camID):
#         threading.Thread.__init__(self)
#         self.previewName = previewName
#         self.camID = camID

#     def run(self):
#         print("Starting " + self.previewName)
#         self.camPreview(self.previewName, self.camID)

#     def camPreview(previewName, camID):
#         cv2.namedWindow(previewName)
#         cam = cv2.VideoCapture(camID,cv2.CAP_DSHOW)
#         cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#         cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

#         if cam.isOpened():  # try to get the first frame
#             rval, frame = cam.read()
#             cv2.imwrite('frame'+str(camID)+'.jpg',frame)
#         else:
#             rval = False

#         while rval:
#             cv2.imshow(previewName, frame)
#             rval, frame = cam.read()
#             key = cv2.waitKey(20)
            
#             if key == 27:  # exit on ESC
#                 break
#         cv2.destroyWindow(previewName)

class RoverCamera:
    #def __init__(self, port, storage_path, vid_length) -> None:
    #    """inputs:
    #        port: usb port where main camera is located
    #        storage_path: path to where to store video
    #        vid_length: how long of video segments to store in seconds (is this how we #want to do it???)    
    #    """
    #    # member vars
    #    self.recordingProcess = []
        # initialize stuff
    #    pass

    def __init__(self,comms,port:list,vid_length:int,photoPath:str,photoResolution:tuple,videoPath:str,fps:int,videoResolution:tuple):
        self.port = port #camera 1 2 3
        self.comms = comms
    #for photo
        self.vid_length = vid_length #second
        self.photoPath = photoPath
        self.photoCounter = 0 #this will be on name of new photo
        self.photoResolution = photoResolution
    #for video
        self.videoPath = videoPath
        print(videoPath)
        self.fps = fps
        self.videoResolution = videoResolution
        self.videoCounter = 0 #this will be on name of new video

    def record(self):
        """
        The process that will actually be recording video. 
        Record in self.vidLength length chunks.
        """
        
        cap=cv2.VideoCapture(self.port[0]) #port
        cap.set(cv2.CAP_PROP_FPS,self.fps)
        #"desktop/:C/test" + "0" + ".avi"
        out = cv2.VideoWriter("/home/sailr/SeniorProjects/automation/videos/video.avi",cv2.VideoWriter_fourcc(*'MJPG'),self.fps,self.videoResolution)
        self.videoCounter+=self.videoCounter

        start = time.time()
        while(time.time()-start<self.vid_length):#break to stop recording after videoLength second
            ret,frame = cap.read()
            frame = cv2.resize(frame,self.videoResolution)
            if ret:
                out.write(frame)
                print('video capturing')
            else:
                print('video capture not working')
            #cv2.imshow('frame',frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):  

        print(str(time.time()-start))
        #cap.release() #stop recording and write video file into path
        #out.release() #turn off camera
        self.comms.syncVideo()

        # stroy all the windows
        #cv2.destroyAllWindows()

    def startRecording(self):
        """
        begin a process for recording video
        """
        self.recordingProcess = Process(target=self.record,args=None)     #   self.recordingProcess.start()
        #tbc

    
    def stopRecording(self):
        """
        stop the recordingProcess
        """
        self.recordingProcess.terminate()
        #tbc

    # uneeded? Should we send at certain cadence?
    #def sendVideo(self): # -> bool:
        """
        write some amount of video to a path that will be sent back to ground station
        """
        #todo
        #pass

    #def send360(self,port):
        #pano = self.take360(port)

        #send command

    def take360(self):

        capture0=cv2.VideoCapture(self.port[0])
        capture0.set(cv2.CAP_PROP_AUTOFOCUS,1)
        result,frame0=capture0.read()
        #cv2.imwrite('frame'+str(self.port[0])+'.jpg',frame0)
        capture0.release()

        capture1 = cv2.VideoCapture(self.port[1])
        capture1.set(cv2.CAP_PROP_AUTOFOCUS,1)
        result,frame1=capture1.read()
        #cv2.imwrite('frame'+str(self.port[1])+'.jpg',frame1)
        capture1.release()
        

        capture2 = cv2.VideoCapture(self.port[2])
        capture2.set(cv2.CAP_PROP_AUTOFOCUS,1)
        result,frame2=capture2.read()
        #cv2.imwrite('frame'+str(self.port[2])+'.jpg',frame2)
        capture2.release()
        
        #frame0=cv2.imread('frame'+str(self.port[0])+'.jpg')
        #frame1=cv2.imread('frame'+str(self.port[1])+'.jpg')
        #frame2=cv2.imread('frame'+str(self.port[2])+'.jpg')

        # initialized a list of images
        imgs = [frame2,frame1,frame0]
        
        #for i in range(len(image_paths)):
         #   imgs.append(image_paths[i])
            # this is optional if your input images isn't too large
            ## you don't need to scale down the image
            # in my case the input images are of dimensions 3000x1200
            # and due to this the resultant image won't fit the screen
            # scaling down the images
        # showing the original pictures
        #cv2.imshow('1',imgs[0])
        #cv2.imshow('2',imgs[1])
        #cv2.imshow('3',imgs[2])
        
        #stitchy=cv2.Stitcher.create()

        #(dummy,output)=stitchy.stitch(imgs)
        
        #if dummy != cv2.STITCHER_OK:
        # checking if the stitching procedure is successful
        # .stitch() function returns a true value if stitching is
        # done successfully
         #   print("Stitching was not successful")
        #else:
         #   print('Your Panorama is ready!!!')
        
        # final output
        pano = cv2.hconcat(imgs)
        cv2.imwrite("/home/sailr/SeniorProjects/automation/images/pano.jpg",pano)
        self.photoCounter += 1
        # save output as .jpg
        self.comms.syncImage()

#######

