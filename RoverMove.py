# Written by Trevor Reed
import sys, time, numpy as np, pdb, logging
from RoverGPS import RoverGPS
from RoverLidar import RoverLidar 
from RoverUART import RoverUART
from RoverComms import RoverComms
from multiprocessing import Process

### Class that will handle the motion of the rover
class RoverMove:
	def __init__(self,lidar:RoverLidar,gps:RoverGPS,uart:RoverUART,comms:RoverComms,buffer_dist,red_width,translation_res) -> None:
		"""
		Initializes member variables
		"""
		self.gps = gps
		self.lidar = lidar
		self.uart = uart
		self.process = None
		self.buffer_dist = buffer_dist
		self.red_width = red_width
		self.translation_res = translation_res
		self.comms = comms
		logging.info("Rovermove initialized")

	def motionInProgress(self) :
		"""
		Loops until motion is complete
		"""
		success = 0
		while not success:
			#TODO: Call the correct function
			#success = self.uart.check_motion_status()
			success = 1
			time.sleep(.5)
		return

	### Autonomous Mode ###
	def autonomous(self,LOI,red_width,buffer_dist,translation_res):
		"""
		Autonomously move the rover to a LOI
		"""
		logging.info("Beginning autonomous movement.")
		
		#Initializes starting/desired LOI and connection flag to verify connection is still established
		start_LOI = LOI
		desired_LOI = LOI
		connection_flag = 1

		#Checking if Rover is at LOI
		atloi = self.gps.atloi(LOI)
		
		#Initializing LiDAR
		time_to_scan = 2 # seconds
		[status, obstacles, _] = self.lidar.getObstacles(time_to_scan)
		
		#Initializing commands
		command = None

		#Loops until LOI is reached
		while not atloi:

			#If ground station connection is lost, sets LOI to start point for rover to return to
			if not self.comms.checkConnection():
				#Sets the desired LOI to revert to when connection is regained
				if connection_flag == 1:
					desired_LOI = LOI
				LOI = start_LOI
				connection_flag = 0
			#If ground station connection is regained, sets LOI back to what it was before
			elif connection_flag == 0:
				LOI = desired_LOI
				connection_flag = 1

			#Checks if a switch to manual control is sent
			command = self.comms.readCommand()
			if command["commandType"] == "stop":
				print('Stopping autonomy..."')
				break;

			#Finding change in heading desired to point to LOI
			mag_heading = self.uart.getMagneticAzm()
			print(mag_heading)
			delta_heading = self.gps.angleToTarget(LOI,mag_heading)
			print('Delta heading required:',delta_heading,'degrees.')

			#Sending command to teensy and waiting for completion
			self.uart.sendRotateCmd(delta_heading)
			#Function waits for completion before moving on
			self.motionInProgress()

			#Checks if at LOI
			atloi = self.gps.atloi(LOI)
			logging.info('[lat,lon]='+str(self.gps.getGPS())+', dist='+str(self.gps.distanceToTarget(LOI))+' m, angle from N='+str(self.gps.bearingToTarget(LOI))+' deg, MagHeading='+str(mag_heading)+' deg, atloi='+str(atloi))
			
			#If no object is in the way and not yet at LOI, enters loop
			while status is None and atloi == 0:
				#Checks if Rover is pointing at LOI before movement
				if self.checkDesiredHeading(delta_heading):
					print("Nothing in the way")
					print("Moving",translation_res,"meters")

					#Sends translation command
					self.uart.sendTranslateCmd(translation_res)
					#Function waits for completion before moving on
					self.motionInProgress()

					#Checks if Rover is pointing at LOI
					mag_heading = self.uart.getMagneticAzm()
					print(mag_heading)
					delta_heading = self.gps.angleToTarget(LOI,mag_heading)
					atloi = self.gps.atloi(LOI)

					#Checks if any obstacle is in view
					[status,obstacles,_] = self.lidar.getObstacles(time_to_scan)
					delta_heading = self.gps.angleToTarget(LOI,mag_heading)
				#If Rover is not pointing at LOI, breaks and re-evaluates state
				else:
					break
					
			#If object is in clearance zone (yellow), enters loop
			while status == "yellow" and atloi == 0:
				#Finds the distance required to pass the object
				distance = self.getDeltaDistance(obstacles)
				#Sends translation command
				print("Moving",distance,"meters")
				self.uart.sendTranslateCmd(distance)
				#Function waits for completion before moving on
				self.motionInProgress()
				
				#Checks if any obstacle is in view
				[status,obstacles,_] = self.lidar.getObstacles(time_to_scan)
				
				#Checks if at LOI
				atloi = self.gps.atloi(LOI)

			#If object is in avoidance zone (red), enters loop
			while status == "red" and atloi == 0:

				#If obstacle is too close, Rover backs off (should not ever occur)
				if self.getDeltaDistance(obstacles)<red_width/2:
					#Sends command to backoff from Obstacle
					self.uart.sendTranslateCmd(-translation_res)
					#Function to wait for completion before moving on
					self.motionInProgress()

				#Continues
				else:
					#Finds the required angle to rotate to move obstacle into clearance zone
					des_angle = self.getDeltaRotation(obstacles,red_width,buffer_dist)
					
					#Sends rotation command
					print("Rotating",des_angle,"degrees")
					self.uart.sendRotateCmd(des_angle)
					#Function to wait for completion before moving on
					self.motionInProgress()

					#Checks if any obstacle is in view
					[status,obstacles,_] = self.lidar.getObstacles(time_to_scan)

					#Checks if at LOI
					atloi = self.gps.atloi(LOI)
		logging.info('[lat,lon]='+str(self.gps.getGPS())+', dist='+str(self.gps.distanceToTarget(LOI))+' m, angle from N='+str(self.gps.bearingToTarget(LOI))+' deg, MagHeading='+str(mag_heading)+' deg, atloi='+str(atloi))

	def checkDesiredHeading(self,delta_heading):
		'''
		Checks if the rover is pointing at the desired heading within 2 degrees
		'''
		if abs(delta_heading) < 2:
			return 1
		else:
			return 0
	
	def getDeltaRotation(self,obstacles,red_width,buffer_dist):
		'''
		Finds the rotation required to move obstacle out of avoidance zone
		'''
		#If there are no obstacles in view, return 0 degrees
		if len(obstacles) == 0:
			return 0

		#Priming variables
		flag = 0
		Rightvalue_y = obstacles[0][1]
		Rightvalue_x = obstacles[0][0]
		Leftvalue_y = obstacles[0][1]
		Leftvalue_x = obstacles[0][0]

		#Finds the furthest right X and Y and the furthest left X and Y values for obstacles
		for iteration in obstacles:
			if iteration[1] < Leftvalue_y:
				Leftvalue_y = iteration[1]
				Leftvalue_x = iteration[0]
			if iteration[1] > Rightvalue_y:
				Rightvalue_y = iteration[1]
				Rightvalue_x = iteration[0]
		
		#Adds the buffer distance produced by LiDAR grid to corresponding values
		Rightvalue_y = Rightvalue_y + buffer_dist
		Leftvalue_y = Leftvalue_y - buffer_dist
		#Adding .5 for rover length so rotation is at center of Rover
		rover_length = 1/2
		Rightvalue_x = Rightvalue_x + rover_length - buffer_dist
		Leftvalue_x = Leftvalue_x + rover_length - buffer_dist 
		
		#Finds the angles to turn right and left using trig
		DistRight = np.sqrt(Rightvalue_x**2+Rightvalue_y**2)
		AngleToTurnRight = np.rad2deg(np.arcsin((3*red_width/4)/DistRight))
		DistLeft = np.sqrt(Leftvalue_x**2+Leftvalue_y**2)
		AngleToTurnLeft = np.rad2deg(np.arcsin((-3*red_width/4)/DistLeft))
		
		#Adds opposite angle to correct calculation
		if not np.isnan(AngleToTurnRight):
			if Rightvalue_y > 0:
				AngleToTurnRight += np.rad2deg(np.arctan(Rightvalue_y/Rightvalue_x))
		#If arcsin returns nan, set angles to 90 degrees (turn square right/left). Arcsin returns nan if obstacle is too close (shouldnt happen)
		else:
			AngleToTurnRight = 90
		if not np.isnan(AngleToTurnLeft):
			if Leftvalue_y < 0:
				AngleToTurnLeft += np.rad2deg(np.arctan(Leftvalue_y/Leftvalue_x))
		else:
			AngleToTurnLeft = -90

		#Chooses the smaller angle to return
		if abs(AngleToTurnLeft) > abs(AngleToTurnRight):
			 AngleToTurn = AngleToTurnRight
		elif abs(AngleToTurnLeft) < abs(AngleToTurnRight):
			 AngleToTurn = AngleToTurnLeft

		#Last two checks are for if arcsin produced nan so it returns -90 or 90
		elif abs(Rightvalue_y) > abs(Leftvalue_y):
			AngleToTurn = AngleToTurnLeft
		else: 
			AngleToTurn = AngleToTurnRight

		return AngleToTurn
		
	def getDeltaDistance(self,obstacles):
		'''
		Determines the distance required to move past an obstacle in the clearance zone
		'''
		#Priming variables
		flag = 0
		iteration_prev = 0
		value_x = 0
		value_y = 0

		#Finds the point closest to the center (center is X == 0)
		for iteration in obstacles:
			if iteration[0] > iteration_prev:
				value_x = iteration[0]
				value_y = iteration[1]
			iteration_prev = iteration[0]

		#Adds buffer to move clearly past clearance zone
		buffer_distance = .5
		value_x = value_x + buffer_distance

		#Trig to find distance to the object
		distance_to_obj = np.sqrt(value_x**2+value_y**2)
		angle = np.arctan2(value_y,value_x)

		#Trig to find distance to move
		distance_to_move = distance_to_obj/np.cos(angle)
		return distance_to_move

	def manual(self,type:str,distOrAngle:float) -> bool:
		"""
		Passes on a single command to teensy to be executed
		"""
		if type == "rotate":
			self.uart.sendRotateCmd(distOrAngle)
		elif type == "translate":
			self.uart.sendTranslateCmd(distOrAngle)
		return
