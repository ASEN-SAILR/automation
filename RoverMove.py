# Trevor 
import RoverGPS
import RoverLidar
from multiprocessing import Process

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
		self.process = None

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
		return self.process.is_alive()

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
			pass

		# start self.process for these

		if command["type"]=="autonomous":
			self.process = Process(target=self.autonomous, args=(command['LOI']))
			self.process.start()

		elif command["type"]=="manual":
			self.process = Process(target=self.manual, args=(command["type"],command["dist"],command["angle"]))
			self.process.start()

		else:
			# throw error?
			pass

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
		pass

	def sendTranslation(self,distance:float) -> bool:
		"""
		sends a translation to the teesny/controls to be executed

		input:
			distance: distance [meters] to translate in body frame. Can only be along rover's foward and backward axis.
		output:
			True if sent to teensy
			False if something went wrong
		"""
		pass
