# Trevor
import sys
sys.path.append("../")
import time
from RoverGPS import RoverGPS
from RoverLidar import RoverLidar 
#from RoverMagnet import RoverMagnet
#from RoverUART import RoverUART
import numpy as np
import pdb
from multiprocessing import Process
### Class that will handle the motion of the rover
class RoverMove:
        def __init__(self,lidar:RoverLidar,gps:RoverGPS,buffer_dist,red_width) -> None:
                """
                inputs:
                        gps: instance of class RoverGPS
                        lidar: instance of class RoverLidar
                """
                #member variables here

				#self.uart = uart
                self.gps = gps
                #self.magnet = magnet
                self.lidar = lidar
                self.process = None
                self.buffer_dist = buffer_dist
                self.red_width = red_width

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
        def autonomous(self,LOI,RedWidth):
                """
                autonomously move the rover to a LOI

                TODO: update function calls to match current classes
                """
                MagHeading = 0 # self.uart.getMagneticAzm()
                atlocation = 0 # self.gps.distanceToTarget(LOI) < 1.15 #precision radius(+/-1.15)
                #make the rover move autonomously to LOI
                time_to_scan = 2 # seconds
                [Status, Obstacles, _] = self.lidar.getObstacles(time_to_scan)
                while not atlocation:
                        #Finding change in heading desired to point to LOI
                        #MagHeading = magnet.get_heading()
                        
                        #DeltaHeading = self.gps.angleToTarget(LOI,MagHeading)
                        DeltaHeading = 0
                        print('Delta heading required:',DeltaHeading,'degrees.')
                        #Sending command to teensy
                        #self.sendRotation(DeltaHeading)

                        #Will wait until motion is complete
                        #motionInProgress()

                        #Getting lidar map and finding what zone they are in
                        #Priming for loop
                        
                        #time_to_scan = 2 #seconds
                        #Gets current lidar obstacles and status
                        #[Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                        #time.sleep(2)
                        #pdb.set_trace()
                        
                        while Status is None:
                                if self.check_desired_heading(DeltaHeading):
                                        #Commenting out movement to test lidar
                                        #self.sendTranslation(1) #Moves 1 meter
                                        #Waits until motion is complete
                                        #self.motionInProgress()
                                        print("Nothing in the way")
                                        pdb.set_trace()
                                        [Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                                        #time.sleep(2)
                                        DeltaHeading = self.gps.angleToTarget(LOI,MagHeading)
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
                                pdb.set_trace()
                                [Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                                #time.sleep(2)
                        while Status is "red":
                                #Needs testing
								if self.get_delta_distance(Obstacles)<RedWidth/2:
    								pass#back off
								else:
									Angle = self.get_delta_rotation(Obstacles,RedWidth) #Gets angle to rotate to set object in clearance zone
									#self.sendRotation(Angle)
									#Waits for motion to complete
									#self.motionInProgress()
									print("Rotate",Angle,"degrees")
									pdb.set_trace()
									[Status,Obstacles,_] = self.lidar.getObstacles(time_to_scan)
                                #time.sleep(2)

        def check_desired_heading(self,DeltaHeading):
                if abs(DeltaHeading) < 2:# checks if rover is pointing at LOI
                        return 1
                else:
                        return 0
        
        #Tested: Yes, working as intended       
        #Input: Array of values of X,Y
        def get_delta_rotation(self,Obstacles,RedWidth):
                if len(Obstacles) == 0:
                        return 0
                # priming variables
                Flag = 0
                RightValueY = Obstacles[0][1]
                RightValueX = Obstacles[0][0]
                LeftValueY = Obstacles[0][1]
                LeftValueX = Obstacles[0][0]
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
                '''if abs(LeftValueY) > abs(RightValueY):
                        ValueY = RightValueY
                        ValueX = RightValueX
                else:
                        ValueY = LeftValueY
                        ValueX = LeftValueX
                        RedWidth = -RedWidth
                '''
				#RightValueX += 0.5 #if we dont add this, we assume the rover turn in place of LiDar, which in fact we turn in place of the middle of the rover(0.5m behind LiDar)
				#LeftValueX += 0.5
                DistRight = np.sqrt(RightValueX**2+RightValueY**2)
                AngleToTurnRight = np.rad2deg(np.arcsin((RedWidth/2)/DistRight)) #add buffer to y?
                #print(AngleToTurn)
                DistLeft = np.sqrt(LeftValueX**2+LeftValueY**2)
                AngleToTurnLeft = np.rad2deg(np.arcsin((-RedWidth/2)/DistLeft)) #add buffer to y?
                #pdb.set_trace()
                if not np.isnan(AngleToTurnRight):
    					if RightValueY > 0:
                         	AngleToTurnRight += np.rad2deg(np.arctan(RightValueX/RightValueY))
                else:
                    	AngleToTurnRight = 90
                # if LeftValueY < 0:
                #          BufferAngle = np.rad2deg(np.arctan(LeftValueX/LeftValueY))
                #          if not np.isnan(AngleToTurnLeft):
                #                   AngleToTurnLeft = AngleToTurnLeft + BufferAngle
                #          else:
                #                   AngleToTurnLeft = -90
                # else:
                #          if np.isnan(AngleToTurnLeft):
                #                   AngleToTurnLeft = -90
				if not np.isnan(AngleToTurnLeft):
    					if LeftValueY < 0:
                        	AngleToTurnLeft += np.rad2deg(np.arctan(LeftValueX/LeftValueY))
                else:
                        AngleToTurnLeft = -90

                #pdb.set_trace()
                if abs(AngleToTurnLeft) > abs(AngleToTurnRight):
                         AngleToTurn = AngleToTurnRight
                elif abs(AngleToTurnLeft) < abs(AngleToTurnRight):
                         AngleToTurn = AngleToTurnLeft
                elif abs(RightValueY) > abs(LeftValueY): #abs(angleLeft) == abs(angleRight) and abs(rightY) > abs(leftY)
                        print(RightValueY,LeftValueY)
                        AngleToTurn = AngleToTurnLeft
                else: #abs(angleLeft) == abs(angleRight) and abs(rightY) <= abs(leftY)
                        AngleToTurn = AngleToTurnRight
                return AngleToTurn
                # trig to find angle to turn
                #AngleToTurnRight = np.rad2deg(np.arctan2(RightValueY+self.buffer_dist,RightValueX-self.buffer_dist))
                #AngleToTurnLeft = np.rad2deg(np.arctan2(LeftValueY-self.buffer_dist,LeftValueX-self.buffer_dist))
                #if LeftValueY == 0:
                 #       AngleToTurnLeft = 0
                #if RightValueY == 0:
                 #       AngleToTurnRight = 0
                # chooses the shorter angle
                # adds buffer to account for rover size
                #pdb.set_trace()
                ''' print(AngleToTurnRight,AngleToTurnLeft)
                if abs(AngleToTurnRight) > abs(AngleToTurnLeft):
                        AngleToTurn = AngleToTurnLeft
                else:
                        AngleToTurn = AngleToTurnRight
                return AngleToTurn
                '''
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
                BufferDistance = 0
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
