import RoverMove
import RoverComms
import RoverGPS
import RoverLidar
import RoverCamera
import RoverUART
from multiprocessing import Process

DISTANCE = 1 #distance to move in a straight line

if __name__ == "__main__":
	# start video recording (class)
	camPort = r"/dev/tty/0"
	videoPath = r"~/videos/" #example path
	video = RoverCamera(camPort,videoPath,vidLength=5)
	video.startRecording()

	# start uart comms with Teensy
	teensyPort = r"/dev/tty/1"
	uart = RoverUART(teensyPort,baud=115200) 

	# start lidar
	lidarPort = r"/dev/tty/2"
	lidar = RoverLidar(lidarPort) # more params?

	# start gps 
	gpsPort = r"/dev/tty/2"
	gps = RoverGPS(gpsPort) # more params?

	# start reading commands from commands log
	commandsPath = r"~/commands.txt"
	telemetryPath = r"~/telemetry.txt"
	comms = RoverComms(commandsPath,telemetryPath)

	# start RoverMove 
	move = RoverMove(gps,lidar)
	
	# Variable that contains the active process: manual or autonomous
	current_process = None

	# tracks current command
	active_command = "stop"

	while True:
		command = None
		while command == None: # and uart.read() == "nominal" <---- do we need to check Teensy comms for errors. Mayeb something like uart.heartbeat()
			command = comms.readCommand()
			#once a command is recieved, we need a way to monitor motion

		# check for emergecy stop conidition first
		if command["type"] == "emergency_stop":
			# termiate child processes immediately and stop motion ASAP

			if current_process is not None: current_process.terminate()
			# current_process.close() #may need this???

			#tell the teensy to stop motion
			uart.sendEmergencyStop()
		
			# skip over rest of loop and wait for command
			continue


		# if we are here, there has been a new command specified and 
		# we need to stop manual or autonomous motion
		current_process.terminate() #we probably want a more elegent way of stopping, this may cause memory leaks

		if command["type"] == "autonomous":
			active_command = "autonomous"

			# multiprodcessing process for this???  
			# can we make autonomous only perform one action at a time? below is what a multiprocessing process would look like
			auton_process = Process(target=move.autonomous,args=(command["LOI"]))
			auton_process.start() 

			current_process = auton_process
			

			# monitor process
			# tbc
			
		elif command["type"] == "manual":
			# check for stop condition prior?

			# multiprodcessing process for this???  
			move.manual(command) #just send the whole dictionary?
			#tbc

		elif command["type"] == "photo":
			# STOP recording 
			# take pano photo
			# begin recording 
			#todo
			pass

		elif command["type"] == "stop":
			# allow cild processes to stop on their own time (will finish motion)
			uart.sendStop()
			
			# skip over rest of loop and wait for command
			continue


		while move.actionInProgress() and not comms.isNewCommand():
			# will hold until a motion is complete or a new command 
			# comes through from the ground station
			pass

		#return to top of loop
			


