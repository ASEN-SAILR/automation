import RoverGPS
import RoverLidar

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

	def motionInProgress(self):
		"""
		checks if the rover is executing a manual or autnonomous command
		
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
		"""
		#make the rover move autonomously to LOI
		while not atlocation:
			#Finding change in heading desired to point to LOI
			CurrCoordinate = get_gps()
			MagHeading = get_heading()
			DesHeading = bearing_to_target(CurrCoordinate,LOI)
			DeltaHeading = get_delta_heading(MagHeading,DesHeading)
			
			#Sending command to teensy
			send_rotation(DeltaHeading)

			#If fail, spit error
			while not success:
				success = check_motion_status() #ask teensy, teesny should know :)
			
			#Getting lidar map and finding what zone they are in
			#Priming for loop
			Map = get_lidar_map()
			[Status,Obstacles] = check_obstacles(Map)
			while Status is none:
				if check_desired_heading():
					send_translation(DISTANCE)
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
