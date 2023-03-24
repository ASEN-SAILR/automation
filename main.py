# Trevor Reed, Luke Roberson, Suphakan Sukwong 


from RoverMove import RoverMove
from RoverComms import RoverComms
from RoverGPS import RoverGPS
from RoverLidar import RoverLidar
from RoverCamera import RoverCamera
from RoverUART import RoverUART
import logging
import numpy as np
import time
from multiprocessing import Process

DISTANCE = 1 #distance to move in a straight line

if __name__ == "__main__":
	#initialize logging
	logging.basicConfig(
		filename='rover_log.log',
		format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s %(funcName)10s-   %(message)s',
		level=logging.INFO,
		datefmt='%Y-%m-%d %H:%M:%S')
	
	logging.getLogger("numpy").setLevel(logging.WARNING)
	logging.getLogger("multiprocessing").setLevel(logging.WARNING)

	# start reading commands from commands log
	# leaving these in for testing on automation end but should be taken out
	commands_path = r"commands.txt"
	telemetry_path = r"telemetry.txt"
	# onboard computer comms vars
	obcCommandPath = commands_path
	obcTelemPath = telemetry_path
	obcVideoPath = "video"
	obcImagePath = "images"
	#currCmdNum = 0 #not needed, automatically defined in RoverComms
	# ground station comms vars
	gs_ssh_password = "asen-sailr"
	gs_ip = "192.168.1.3"
	gs_home_path = "/home/ground-station/comms-gs/"
	gs_telem_path = gs_home_path+"telemetry.txt"
	gs_video_path = gs_home_path+"videos"
	gs_image_path = gs_home_path+"images"
	#start comms
	comms = RoverComms(obcCommandPath,obcTelemPath,obcVideoPath,obcImagePath,gs_ssh_password,gs_ip,gs_telem_path,gs_video_path,gs_image_path)
	

	# start video recording (class)
	# camPort = r"/dev/tty/0"
	# videoPath = r"~/videos/" #example path
	# vid_length = 5 #unit is second
	# photoPath = obcImagePath
	# photoResolution = (640,360) #format: tuple (480,480)
	# videoPath = obcVideoPath
	# fps = 30 
	# videoResolution = (640,360) #format: tuple (480,480)
	# video = RoverCamera(comms,camPort,videoPath,vidLength=5) #need comms so that we can send video after recording
	# comms,port,vid_length,photoPath,photoResolution,videoPath,fps,videoResolution
	# video.startRecording()

	# start uart comms with Teensy
	teensy_port = r"/dev/ttyACM1"
	uart = RoverUART(teensy_port) 
	uart.readLine() #clear the serial buffer 

	# start lidar
	lidar_port = r"/dev/ttyUSB0"
	lidar = RoverLidar(port_name=lidar_port)
	x_lim=np.array((0,1)) 
	y_lim=np.array((-.5,.5))
	threshold=0
	red_lim=np.array((0.25,0.25))
	red_width = .5
	resolution=0.1
	lidar.setMapParams(
			x_lim=x_lim, 
			y_lim=y_lim, 
			threshold=threshold, 
			red_lim=red_lim, 
			resolution=resolution
			)
	buffer_dist = resolution/2

	# start gps 
	gps_port = r"/dev/ttyACM0"
	gps = RoverGPS(gps_port) # more params?

	LOI = [40.0093664,-105.2439658]
	gs_coords = gps.getGPS()

	gps.startTele()

	# start move
	translation_res = 1
	move = RoverMove(lidar,gps,uart,buffer_dist,red_width,translation_res)

	#start record process that will be run on background - keep recording and sending videos
	#gps.startTele()

	# Variable that contains the active process: manual or autonomous
	# need to instantiate a process then terminate for logic in while loop to work
	def foo(): pass
	current_process = Process(target=foo, args=())
	current_process.start()
	if current_process.is_alive():current_process.terminate()

	# tracks current command
	active_command = "stop"
	
	command = {"commandType":"autonomous", "LOI":[40.0091687,-105.243807]}
	logging.info("main loop begining")
	while True:
		logging.info("waiting for command")
		while True: # and uart.read() == "nominal" <---- do we need to check Teensy comms for errors. Mayeb something like uart.heartbeat()
			
			# command = comms.readCommand()
			
			
			if command:
				logging.info(f"command ({command}) read in from RoverComms ")
			
				missionDone = False
				break


			#if no new command, at LOI, and autonomous done
			if active_command == "autonomous" and ~current_process.is_alive(): #we need to check if LOI not none because that means we were in autonomous mode so we should take a photo and return to gs. If LOI is none, that means we were in manual or other mode and should not take a photo and return to gs until user sets mode to autonomous. We also check if the process is done because that means we are at LOI.
				if LOI == gs_coords: #the rover reached LOI and now back at gsLOI
					logging.info("rover at LOI")
					if ~missionDone:
						missionDone = True
						print("Mission done. Rover is now back at ground station. Waiting for a new command...")
			else:#TODO:the rover is at the LOI
				pass
				# video.stopRecording()
				# video.take360()
				# video.startRecording()
				# #TODO what does the command looks like
				# command = {"type"="autonomous","LOI"=gsLOI}
				#once a command is recieved, we need a way to monitor motion		
				# check for emergecy stop conidition first

		if command["commandType"] == "stop":
			active_command = "stop"
			logging.info("stop command recieved")
			# termiate child processes immediately and stop motion ASAP
			LOI = None
			move.emergencyStop()

			if current_process.is_alive(): current_process.terminate()
			# current_process.close() #may need this???

			#tell the teensy to stop motion
			uart.sendStopCmd()
		
			# skip over rest of loop and wait for command
			continue


		# if we are here, there has been a new command specified and 
		# we need to stop manual or autonomous motion
		if current_process.is_alive(): current_process.terminate() #we probably want a more elegent way of stopping, this may cause memory leaks
		#move.stopMove()

		#if command["mode"] == "autonomous" or command["mode"] == "manual":
			#current_process = Process(target=move.startMove, args=(command,))
		if command["commandType"]=="autonomous":
			active_command = "autonomous"
			logging.info("autonomous command recieved")
			LOI = command["LOI"]
			current_process = Process(target=move.autonomous, args=(LOI,red_width,resolution/2,translation_res))
			current_process.start()
		elif command["commandType"]=="manual":
			active_command = "manual"
			logging.info(f"manual command recieved: {command}")
			LOI = None
			# current_process = Process(target=move.manual, args=(command["type"],command["dist"],command["angle"]))
			current_process = Process(target=move.manual, args=("rotation",0,0))
			current_process.start()		

		#TODO take photo when at LOI
		elif command["commandType"] == "photo":
			active_command = "photo"
			# STOP recording 
			# take pano photo
			# begin recording 
			#todo
			LOI = None
			# video.stopRecording()
			# video.take360()
			# video.startRecording()


		command = {} #TODO REMOVE WHEN DONE WITH NO COMMS testing
	
		#return to top of loop
			

