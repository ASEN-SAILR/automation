# https://www.turing.com/kb/python-multiprocessing-vs-multithreading
# suphakan
from multiprocessing import Process
import cv2
import numpy as np
import time
import RoverComms

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

    def __init__(self,comms:RoverComms,port:list,vid_length:int,photoPath:str,photoResolution:tuple,videoPath:str,fps:int,videoResolution:tuple):
        self.port = port #camera 1 2 3
        self.comms = comms
    #for photo
        self.vid_length = vid_length #second
        self.photoPath = photoPath
        self.photoCounter = 0 #this will be on name of new photo
        self.photoResolution = photoResolution
    #for video
        self.videoPath = videoPath
        self.fps = fps
        self.videoResolution = videoResolution
        self.videoCounter = 0 #this will be on name of new video

    def _record(self):
        """
        The process that will actually be recording video. 
        Record in self.vidLength length chunks.
        """
        
        cap=cv2.VideoCapture(self.port[0]) #port one
        #"desktop/:C/test" + "0" + ".avi"
        out = cv2.VideoWriter(self.videoPath+num2str(self.videoCounter)+".avi",cv2.VideoWriter_fourcc('M','J','P','G'),self.fps, self.videoResolution)
        videoCounter+=videoCounter

        start = time.time()

        while(time.time()-start<self.vid_length):#break to stop recording after videoLength second
            ret,frame = cap.read()
            out.write(frame)
            #cv2.imshow('frame',frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):  

        out.release() #stop recording and write video file into path
        cap.release() #turn off camera
        comms.syncVideo()

        # Destroy all the windows
        #cv2.destroyAllWindows()

    def startRecording(self):
        """
        begin a process for recording video
        """
        self.recordingProcess = Process(target=self._record,args=None)
        self.recordingProcess.start()
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

        cam_port0=self.port[0]
        cam_port1=self.port[1]
        cam_port2=self.port[2]
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
        #cv2.imshow('1',imgs[0])
        #cv2.imshow('2',imgs[1])
        #cv2.imshow('3',imgs[2])
        
        stitchy=cv2.Stitcher.create()
        (dummy,output)=stitchy.stitch(imgs)
        
        if dummy != cv2.STITCHER_OK:
        # checking if the stitching procedure is successful
        # .stitch() function returns a true value if stitching is
        # done successfully
            print("Stitching was not successful")
        else:
            print('Your Panorama is ready!')
        
        # final output
        cv2.imwrite(self.photoPath+num2str(self.photoCounter)+".avi",output)
        self.photoCounter += 1
        # save output as .jpg
        comms.syncImage()

        #cv2.imshow('final result',output)
        #cv2.waitKey(0)

