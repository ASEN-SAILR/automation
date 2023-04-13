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
from multiprocessing import Process, Value

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
	camPort = [0,4,8]
	videoPath = "~/SeniorProjects/automation/videos/" #example path
	videoLength = 5 #unit is second
	photoPath = "~/SeniorProjects/automation/images/"
	photoResolution = (640,360) #format: tuple (480,480)
	# videoPath = obcVideoPath
	fps = 30 
	videoResolution = (640,360) #format: tuple (480,480)
	cam = RoverCamera(comms,camPort,videoLength,photoPath,photoResolution,videoPath,fps,videoResolution) #need comms so that we can send video after recording

	# start uart comms with Teensy
	teensy_port = r"/dev/ttyACM0"
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
	gps_port = r"/dev/ttyACM1"
	gps = RoverGPS(gps_port,comms) # more params?

	#LOI = [40.0093664,-105.2439658]
	gs_coords = gps.getGPS()

	gps.startTele()

	# start move
	translation_res = 1
	move = RoverMove(lidar,gps,uart,comms,buffer_dist,red_width,translation_res)

	#start record process that will be run on background - keep recording and sending videos
	#gps.startTele()

	# Variable that contains the active process: manual or autonomous
	# need to instantiate a process then terminate for logic in while loop to work
	def foo(): pass
	process_flag = Value('b',True)
	current_process = Process(target=foo, args=(process_flag))
	current_process.start()

	if current_process.is_alive():current_process.terminate()

	# tracks current command
	# active_command = "stop"
	LOI = None	
	command = None#{"commandType":"autonomous", "LOI":[40.0091687,-105.243807]}
	logging.info("main loop begining")
	comms.startLive() # live_video_process = Process(comms.liveVideoServer)
					  # live_video_process.start()
	while True:

		logging.info("waiting for command")
		while True: # and uart.read() == "nominal" <---- do we need to check Teensy comms for errors. Mayeb something like uart.heartbeat()
			
			#print("================ Waiting for Command ======================")
			command = comms.readCommand()
			
			if command:
				logging.info(f"command ({command}) read in from RoverComms ")
				print('received new command: command=',command)
				missionDone = False
				break


			#if no new command, at LOI, and autonomous done
			if LOI is not None and ~current_process.is_alive(): #we need to check if LOI not none because that means we were in autonomous mode so we should take a photo and return to gs. If LOI is none, that means we were in manual or other mode and should not take a photo and return to gs until user sets mode to autonomous. We also check if the process is done because that means we are at LOI.
				if gps.atloi(LOI): 
					if LOI == gs_coords: #the rover reached LOI and now back at gsLOI
						logging.info("rover at LOI")
						if ~missionDone:
							comms.isStreaming = False
							missionDone = True
							print("Mission done. Rover is now back at ground station. Waiting for a new command...")
					else:#TODO:the rover is at the LOI
						#pass
						# video.stopRecording()

						# live_video_process.terminate()
						print('At LOI, now taking pano.')
						cam.take360()
						print('Pano took. Now wait 30s before going back to ground station.')
						time.sleep(30)
						print('Waiting done. Setting command to auto and LOI to ground station.')
						# video.take360()
						# video.startRecording()
						# live_video_process.start()
						# #TODO what does the command looks like
						command = {"commandType"="autonomous","LOI"=gsLOI}

						#once a command is recieved, we need a way to monitor motion		
						# check for emergecy stop conidition first
				else: #if autonomous exits before we're at LOI(by error), reset command to autonomous toward LOI
    					command = {"commandType"="autonomous","LOI"=LOI}

		if command["commandType"] == "stop":
			active_command = "stop"
			logging.info("stop command recieved")
			print('Stop command received.')
			# termiate child processes immediately and stop motion ASAP
			LOI = None
			# move.emergencyStop()
			process_flag.value = False
			if current_process.is_alive(): current_process.terminate()
			# current_process.close() #may need this???

			#tell the teensy to stop motion
			uart.sendStopCmd()
		
			# skip over rest of loop and wait for command
			continue


		# if we are here, there has been a new command specified and 
		# we need to stop manual or autonomous motion
		#if current_process.is_alive(): current_process.terminate() #we probably want a more elegent way of stopping, this may cause memory leaks
		#move.stopMove()

		#if command["mode"] == "autonomous" or command["mode"] == "manual":
			#current_process = Process(target=move.startMove, args=(command,))
		if command["commandType"]=="autonomous":
    		process_flag.value = False
			while current_process.is_alive():
    				print('Exiting the current process')
    				time.sleep(1)
			active_command = "autonomous"
			logging.info("autonomous command recieved")
			print('autonomous command received.')
			LOI = command["LOI"]
			current_process = Process(target=move.autonomous, args=(LOI,red_width,resolution/2,translation_res,process_flag))
			current_process.start()
		elif command["commandType"]=="manual":
			process_flag = False
			while current_process.is_alive():
    				print('Exiting the current process')
    				time.sleep(1)
			print("====================+++++++++++== Sending manual command ============+++")
			active_command = "manual"
			logging.info(f"manual command recieved: {command}")
			print('manual command received.')
			LOI = None
			current_process = Process(target=move.manual, args=(command["manualType"],command["command"]))
			current_process.start()

		#TODO take photo when at LOI
		elif command["commandType"] == "photo":
			active_command = "photo"
			# STOP recording 
			# take pano photo
			# begin recording 
			#todo
			print('stop command received.')
			LOI = None
			cam.take360()
			# video.stopRecording()
			# video.take360()
			# video.startRecording()


		command = {} #TODO REMOVE WHEN DONE WITH NO COMMS testing
	
		#return to top of loop
			

