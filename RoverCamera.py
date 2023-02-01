#https://www.turing.com/kb/python-multiprocessing-vs-multithreading
from multiprocessing import Process

class RoverCamera:
    def __init__(self, port, storage_path, vid_length) -> None:
        """
        inputs:
            port: usb port where main camera is located
            storage_path: path to where to store video
            vid_length: how long of video segments to store in seconds (is this how we want to do it???)    
        """
        # member vars
        self.recordingProcess = []

        # initialize stuff

        pass

    def setPhotoSetting(self,params):
        """
        setter for photo paramaters
        """
        pass

    def setVideoSetting(self,params):
        """
        setter for video paramters
        """
        pass

    def _record(self):
        """
        The process that will actually be recording video. 
        Record in self.vidLength length chunks.
        """
        pass

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
    def sendVideo(self) -> bool:
        """
        write some amount of video to a path that will be sent back to ground station
        """
        #todo
        pass

