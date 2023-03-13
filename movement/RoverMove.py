# Trevor
import sys
sys.path.append("../")
import time
from RoverGPS import RoverGPS
from RoverLidar import RoverLidar 
from RoverMagnet import RoverMagnet
import numpy as np
import pdb
from multiprocessing import Process
### Class that will handle the motion of the rover
class RoverMove:
        def __init__(self,lidar:RoverLidar) -> None:
                """
                inputs:
                        gps: instance of class RoverGPS
                        lidar: instance of class RoverLidar
                """
                #member variables here

                #self.gps = gps
                #self.magnet = magnet
                self.lidar = lidar
                self.process = None

        #Testing: Not complete
        def motionInProgress(self) :
                """
                checks if the rover is executing a manual or autnonomous command

                TODO: we need a variable that tracks if a motion is in progress, may not be possible with multiprocessing...
                
                inputs:
                        none
                returns:
                        True if executing motion
                        False if not executin motion
                """
                success = 0
                while not success:
                        success = check_motion_status
                return

        def startMove(self,command:dict):
                """
                Begins multiprocessing process for manual or autonomous process for rover. 

                input:
                        command dictionary
                returns:
                        bool
                """
                if self.process.is_alive():
                        #TODO Throw error
                        return

                # start self.process for these

                if command["type"]=="autonomous":
                        self.process = Process(target=self.autonomous, args=(command['LOI']))
                        self.process.start()

                elif command["type"]=="manual":
                        self.process = Process(target=self.manual, args=(command["type"],command["dist"],command["angle"]))
                        self.process.start()

                else:
                        # throw error?
                        return

        #Possibly not needed
        def stopMove(self) -> bool:
                """
                stop the rover after next action is complete
                Maybe unneeded depending on how we want to stop the rover 
                
                input:
                        none
                return:
                        bool
                """

        
        def emergencyStopRover(self) -> bool:
                """
                stop rover immediately. Terminate self.process ASAP. 

                return:
                        bool
                """
                return

        ### Autonomous Mode ###
        def autonomous(self,LOI):
                """
                autonomously move the rover to a LOI

                TODO: update function calls to match current classes
                """
                atlocation = 0
                #make the rover move autonomously to LOI
                LOI = [0,0]
                while not atlocation:
                        '''#Finding change in heading desired to point to LOI
                        MagHeading = magnet.get_heading()
                        DeltaHeading = self.gps.angleToTarget(LOI,MagHeading)
                        print(DeltaHeading)
                        #Sending command to teensy
                        #self.sendRotation(DeltaHeading)

                        #Will wait until motion is complete
                        #motionInProgress()

                        #Getting lidar map and finding what zone they are in
                        #Priming for loop
                        '''
                        time_to_scan = 2 #seconds
                        #Gets current lidar obstacles and status
                        [Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                        time.sleep(2)
                        #pdb.set_trace()
                        
                        #Just for testing Lidar
                        DeltaHeading = 0
                        while Status is None:
                                if self.check_desired_heading(DeltaHeading):
                                        #Commenting out movement to test lidar
                                        #self.sendTranslation(1) #Moves 1 meter
                                        #Waits until motion is complete
                                        #self.motionInProgress()
                                        [Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                                        time.sleep(2)
                                        #DeltaHeading = self.gps.angleToTarget(LOI,MagHeading)
                                        print("Nothing in the way")
                                else:
                                        break
                                        
                        while Status is "yellow":
                                #Needs testing
                                Distance = self.get_delta_distance(Obstacles) #Gets the distance to clear clearance zone
                                #Might need to check for distance more than a meter to make sure rover does not go further than it can see
                                #self.sendTranslation(Distance)
                                #Waits for motion to complete
                                #self.motionInProgress()
                                print("Move",Distance,"meters")
                                [Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                                time.sleep(2)
                        while Status is "red":
                                #Needs testing
                                Angle = self.get_delta_rotation(Obstacles) #Gets angle to rotate to set object in clearance zone
                                #self.sendRotation(Angle)
                                #Waits for motion to complete
                                #self.motionInProgress()
                                print("Rotate",Angle,"degrees")
                                [Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                                time.sleep(2)

        def check_desired_heading(self,DeltaHeading):
                if abs(DeltaHeading) < 2:# checks if rover is pointing at LOI
                        return 1
                else:
                        return 0
        
        #Tested: Yes, working as intended       
        #Input: Array of values of X,Y
        def get_delta_rotation(self,Obstacles):
                if len(Obstacles) == 0:
                        return 0
                # priming variables
                Flag = 0
                RightValueY = 0
                RightValueX = 0
                LeftValueY = 0
                LeftValueX = 0
                # determines angle to rotate to avoid obstacles
                # finds the furthest right and the furthest left obstacles
                for Iteration in Obstacles:
                        #pdb.set_trace()
                        if Iteration[1] < LeftValueY:
                                LeftValueY = Iteration[1]
                                LeftValueX = Iteration[0]
                        if Iteration[1] > RightValueY:
                                RightValueY = Iteration[1]
                                RightValueX = Iteration[0]
                # trig to find angle to turn
                AngleToTurnRight = np.rad2deg(np.arctan2(RightValueY,RightValueX))
                AngleToTurnLeft = np.rad2deg(np.arctan2(LeftValueY,LeftValueX))
                # chooses the shorter angle
                # adds buffer to account for rover size
                BufferAngle = 10
                if abs(AngleToTurnLeft) > AngleToTurnRight:
                        AngleToTurn = AngleToTurnRight
                else:
                        AngleToTurn = AngleToTurnLeft
                        BufferAngle = -BufferAngle
                #pdb.set_trace()
                AngleToTurn = AngleToTurn + BufferAngle
                return AngleToTurn
        
        #Tested: Yes, working as intended
        #Input: Array of values of X,Y
        def get_delta_distance(self,Obstacles):
                # determines distance to move rover to avoid obstacles
                Flag = 0
                Iteration_prev = 0
                ValueX = 0
                for Iteration in Obstacles:
                        if Iteration[0] > Iteration_prev:
                                ValueX = Iteration[0]
                        Iteration_prev = Iteration[0]
                BufferDistance = 1
                DistanceToMove = ValueX + BufferDistance
                return DistanceToMove

        #Possibly not needed
        def manual(self,type:str,dist:float,angle:float) -> bool:
                """
                passes on  a single command to teensy to be executed

                input:
                        type: "rotation" or "translation"
                        dist: distance to translate
                        angle: angle to rotate
                                *only one of dist and angle will be used with each call to manual()
                returns:
                        True if executed
                        False if error

                """

                return

        #Possibly not needed
        def sendRotation(self,angle:float) -> bool:
                """
                sends a rotation to the teesny/controls to be executed

                input:
                        angle: angle (deg) to rotate in NED frame about vertical axis (CW is positive)
                output:
                        True if sent to teensy
                        False if something went wrong
                """
                return

        #Possibly not needed
        def sendTranslation(self,distance:float) -> bool:
                """
                sends a translation to the teesny/controls to be executed

                input:
                        distance: distance [meters] to translate in body frame. Can only be along rover's foward and backward axis.
                output:
                        True if sent to teensy
                        False if something went wrong
                """
                return
