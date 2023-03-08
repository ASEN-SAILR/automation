# Trevor Reed, Luke Roberson, Suphakan Sukwong 


import RoverMove
import RoverComms
import RoverGPS
import RoverLidar
import RoverCamera
import RoverUART
import logging
from multiprocessing import Process

DISTANCE = 1 #distance to move in a straight line

if __name__ == "__main__":
	#initialize logging
	logging.basicConfig(
        filename='rover_log.log',
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s -   %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

	# start reading commands from commands log
	# leaving these in for testing on automation end but should be taken out
	commands_path = r"~/commands.txt"
	telemetry_path = r"~/telemetry.txt"
	# onboard computer comms vars
	obcCommandPath = commands_path
	obcTelemPath = telemetry_path
	obcVideoPath = "~/video"
	obcImagePath = "~/images"
	#currCmdNum = 0 #not needed, automatically defined in RoverComms
	# ground station comms vars
	gs_ssh_password = "asen-sailr"
	gs_ip = "192.168.56.102"
	gs_home_path = "/home/ground-station/asen-sailr/"
	gs_telem_path = gs_home_path+"telemetry.txt"
	gs_video_path = gs_home_path+"videos"
	gs_image_path = gs_home_path+"images"
	#start comms
	comms = RoverComms(obcCommandPath,obcTelemPath,obcVideoPath,obcImagePath,gs_ssh_password,gs_ip,gs_telem_path,gs_video_path,gs_image_path)
	

	# start video recording (class)
	camPort = r"/dev/tty/0"
	videoPath = r"~/videos/" #example path
	vid_length = 5 #unit is second
	photoPath = obcImagePath
	photoResolution = (640,360) #format: tuple (480,480)
	videoPath = obcVideoPath
	fps = 30 
	videoResolution = (640,360) #format: tuple (480,480)
	video = RoverCamera(comms,camPort,videoPath,vidLength=5) #need comms so that we can send video after recording
	comms,port,vid_length,photoPath,photoResolution,videoPath,fps,videoResolution
	video.startRecording()

	# start uart comms with Teensy
	teensy_port = r"/dev/tty/1"
	uart = RoverUART(teensy_port,baud=115200) 

	# start lidar
	lidar_port = r"/dev/tty/2"
	lidar = RoverLidar(lidar_port) # more params?

	# start gps 
	gps_port = r"/dev/tty/2"
	gps = RoverGPS(comms,gps_port) # more params?

	# start move
	move = RoverMove(gps,lidar)

	#start record process that will be run on background - keep recording and sending videos
	gps.startTele()
	cam.startRecording()

	# Variable that contains the active process: manual or autonomous
	current_process = None

	# tracks current command
	active_command = "stop"

	command = None
	while True:
		while command == None: # and uart.read() == "nominal" <---- do we need to check Teensy comms for errors. Mayeb something like uart.heartbeat()
			command = comms.readCommand()
			#once a command is recieved, we need a way to monitor motion

		# check for emergecy stop conidition first
		if command["mode"] == "emergency_stop":
			# termiate child processes immediately and stop motion ASAP

			move.emergencyStop()

			if current_process == ~ None: current_process.terminate()
			# current_process.close() #may need this???

			#tell the teensy to stop motion
			uart.sendEmergencyStop()
		
			# skip over rest of loop and wait for command
			continue


		# if we are here, there has been a new command specified and 
		# we need to stop manual or autonomous motion
		current_process.terminate() #we probably want a more elegent way of stopping, this may cause memory leaks

		if command["mode"] == "autonomous" or command["mode"] == "manual":
			move.startMove(command)			

		elif command["mode"] == "photo":
			# STOP recording 
			# take pano photo
			# begin recording 
			#todo
			pass

		elif command["mode"] == "stop":
			# allow child processes to stop on their own time (will finish motion)
			uart.sendStop()
			
			# skip over rest of loop and wait for command
			continue

		command = comms.readCommand()
		while move.actionInProgress() and command["mode"] != 'emergency_stop':
			# will hold until a motion is complete or emergency stop command
			# comes through from the ground station
			command = comms.readCommand() #if user inputs command while moving, it will ignore
										  #should exit this loop with command being None(and rover done action) or emergency stop command

		#return to top of loop
			

