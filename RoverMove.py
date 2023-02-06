import RoverGPS
import RoverLidar
import numpy as np

### Class that will handle the motion of the rover
class RoverMove:
	def __init__(self,gps:RoverGPS,lidar:RoverLidar) -> None:
		"""
		inputs:
			gps: instance of class RoverGPS
			lidar: instance of class RoverLidar
		"""
		#member variables here

		self.gps = gps
		self.lidar = lidar

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
		pass

	### Autonomous Mode ###
	def autonomous(self,LOI):
		"""
		autonomously move the rover to a LOI

		TODO: update function calls to match current classes
		"""
		#make the rover move autonomously to LOI
		while not atlocation:
			#Finding change in heading desired to point to LOI
			CurrCoordinate = get_gps()
			MagHeading = get_heading()
			DesHeading = bearing_to_target(CurrCoordinate,LOI)
			DeltaHeading = get_delta_heading(MagHeading,DesHeading)
			
			#Sending command to teensy
			self.sendRotation(DeltaHeading)

			#If fail, spit error
			while not success:
				success = check_motion_status() #ask teensy, teesny should know :)
			
			#Getting lidar map and finding what zone they are in
			#Priming for loop
			Map = get_lidar_map()
			[Status,Obstacles] = check_obstacles(Map)
			while Status is none:
				if check_desired_heading():
					self.sendTranslation(DISTANCE)
					while not success:
						success = check_motion_status()
					send_video(seconds=30)

					Map = get_lidar_map()
					[Status,Obstacles] = check_obstacles(Map)
				else:
					break
			while Status is "yellow":
				here
			while Status is "red":
				here
		
	def check_desired_heading(MagHeading,DesHeading)
		# checks if rover is pointing at LOI
		BufferAngle = 5
		if MagHeading > DesHeading - BufferAngle AND MagHeading < DesHeading + BufferAngle:
			pass
		else
			fail
	
	def get_delta_rotation(Obstacles):
		# priming variables
		Flag = 0
		RightValueX = 0
		RightValueY = 0
		LeftValueX = 0
		LeftValueY = 0
		# determines angle to rotate to avoid obstacles
		for Iteration in Obstacles:
			if Iteration.X < 0
			# takes most negative x value (left-most)
				if Flag is 0:
					LeftValueX = Iteration.X
					LeftValueY = Iteration.Y
					Flag = 1
			else:
			# takes most positive x value (right-most)
				RightValueX = Iteration.X
				RightValueY = Iteration.Y
		if (-1*LeftValue)>RightValue:
			# turns right
			# trig to find angle to turn
			AngleToTurn = np.arctan2(RightValueX,RightValueY)
		else:
			# turns left
			AngleToTurn = np.arctan2(LeftValueX,LeftValueY)
		# returns degrees
		AngleToTurn = np.rad2deg(AngleToTurn)
		# adds buffer to account for rover size
		BufferAngle = 10
		AngleToTurn = AngleToTurn + BufferAngle
		return AngleToTurn

	def get_delta_distance(Obstacles):
		# determines distance to move rover to avoid obstacles
		Flag = 0
		Iteration_prev = 0
		ValueY = 0
		for Iteration in Obstacles:
			if Iteration.Y > Iteration_prev
				ValueY = Iteration.Y
			Iteration_prev = Iteration.Y
		BufferDistance = 1
		DistanceToMove = ValueY + BufferDistance
		return DistanceToMove

	def manual(self,command):
		# make the rover execute a single command
		pass

	def sendRotation(self,angle:float) -> bool:
		"""
		sends a rotation to the teesny/controls to be executed

		input:
			angle: angle (deg) to rotate in NED frame about vertical axis (CW is positive)
		output:
			True if sent to teensy
			False if something went wrong
		"""

	def sendTranslation(self,distance:float) -> bool:
		"""
		sends a translation to the teesny/controls to be executed

		input:
			distance: distance [meters] to translate in body frame. Can only be along rover's foward and backward axis.
		output:
			True if sent to teensy
			False if something went wrong
		"""
