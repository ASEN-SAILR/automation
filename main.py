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
import os
import serial.tools.list_ports

DISTANCE = 1 #distance to move in a straight line

def find_device_port(deviceID):
	ports = serial.tools.list_ports.comports()
	for port in ports:
		if deviceID in port.hwid:
			return port.device
	return None
def search_all_hwid():
	ports = serial.tools.list_ports.comports()
	for port in ports:
		print(port.hwid,port.device)

#'VID:PID=16C0:0483' for teensy
#'VID:PID=10C4:EA60' for lidar
#'VID:PID=1546:01A8' for gps

def main():
	search_all_hwid()
	#initialize logging
	logging.basicConfig(
		filename='rover_log.log',
		format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s %(funcName)10s-   %(message)s',
		level=logging.INFO,
		datefmt='%Y-%m-%d %H:%M:%S')
	
	logging.getLogger("numpy").setLevel(logging.WARNING)
	logging.getLogger("multiprocessing").setLevel(logging.WARNING)

	# file housekeeping
	os.system("> commands.txt")

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
	# gs_ip = '128.138.65.188'
	gs_home_path = "/home/ground-station/comms-gs/"
	gs_telem_path = gs_home_path+"telemetry.txt"
	gs_video_path = gs_home_path
	gs_image_path = gs_home_path

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
	teensy_port = find_device_port('VID:PID=16C0:0483')
	#teensy_port = r"/dev/ttyACM0"
	uart = RoverUART(teensy_port) 
	# print(teensy_port)
	uart.readLine() #clear the serial buffer 
	print('serial buffer cleared')
	# start lidar
	lidar_port = find_device_port('VID:PID=10C4:EA60')
	# lidar_port = r"/dev/ttyUSB0"
	lidar = RoverLidar(port_name=lidar_port)
	x_lim=np.array((0,2)) 
	y_lim=np.array((-1,1))
	threshold=8
	red_lim=np.array((-0.25,0.25))
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
	gps_port = find_device_port('VID:PID=1546:01A8')
	#gps_port = r"/dev/ttyACM1"
	
	gps = RoverGPS(gps_port,comms) # more params?
	os.system('> telemetry.txt')   
	gps.startTele()
	time.sleep(4)
	#LOI = [40.0093664,-105.2439658]
	gsLOI = gps.getGPS()
	
	# start move
	translation_res = 1
	move = RoverMove(lidar,gps,uart,comms,buffer_dist,red_width,translation_res)

	# Variable that contains the active process: manual or autonomous
	# need to instantiate a process then terminate for logic in while loop to work
	def foo(): pass
	process_flag = Value('b',True)
	current_process = Process(target=foo, args=(process_flag,))
	current_process.daemon = True
	current_process.start()

	if current_process.is_alive():current_process.terminate()

	# tracks current command
	active_command = {"commandType":None}
	# LOI = None
	command = None #{"commandType":"autonomous", "LOI":[40.0091687,-105.243807]}
	lost_connection = False
	logging.info("main loop begining")
	cam.startLiveVideo() # live_video_process = Process(comms.liveVideoServer)
					  # live_video_process.start()
	# time.sleep(1)
	# gps.stopTele()
	# cam.take360()
	# return

	while True:
		# time.sleep(1)
		logging.info("waiting for command")
		print("Waiting for Command...")

		while True: # loop waiting for new command
			time.sleep(1)
			#print("================ Waiting for Command ======================")
			
			if not comms.checkConnection(): #lost connection
    			lost_connection = True
				print('Lost connection, returning to ground station to regain connection')
				logging.info(f"Lost connection, returning to ground station")
    			process_flag.value = False
    			command = {"commandType":"autonomous","LOI":gsLOI}
			elif lost_connection: #regained connection, stop the rover
    			lost_connection = False
				process_flag.value = False
				print('Reconnected!')
				if active_command["commandType"]=='autonomous': #this means we lost connection when we're on auto
					print('Continuing automation toward to LOI')
					command = active_command
			elif active_command["commandType"]=="autonomous" and not current_process.is_alive(): #connection fine, auto done
				if gps.atloi(active_command["LOI"]): #at LOI
					if active_command["LOI"] == gsLOI: #LOI is ground station
						logging.info("rover at ground station")
						active_command = {"commandType":None}
						print("Mission done. Rover is now back at ground station. Waiting for a new command...")
					else: #LOI is not ground station
						logging.info("rover at LOI")
						print('At LOI, now taking pano.')
						cam.take360()
						print('Pano took. Now wait 30s before going back to ground station.')
						time.sleep(30)
						print('Waiting done. Setting command to autonomous and LOI to ground station.')
						command = {"commandType":"autonomous","LOI":gsLOI}
				else: #if autonomous exits before we're at LOI(by error), reset command to autonomous toward LOI
    					command = active_command
			
			if command:
    			logging.info(f"command ({command}) set by algorithm ")
				print('received new command: command=',command)
				break

			#to this point, connection is fine so comms shouldn't throw error
			command = comms.readCommand()

			if command:
    			logging.info(f"command ({command}) read in from RoverComms ")
				print('received new command: command=',command)
				break
			

		#to this point, command is set, either by algorithm or user
		if command["commandType"] == "startStop": #good practice to send stop command before switching modes
			logging.info("stop command received")
			print('Stop command received.')
			# termiate child processes immediately and stop motion ASAP
			process_flag.value = False
			if current_process.is_alive(): current_process.terminate()
			#tell the teensy to stop motion
			uart.sendStopCmd()
		elif command["commandType"]=="autonomous":
    		logging.info("autonomous command received")
			print('autonomous command received.')
			process_flag.value = False #stop and wait process to exit properly
			while current_process.is_alive():
    				print('Exiting the current process')
    				time.sleep(1)
			current_process = Process(target=move.autonomous, args=(command["LOI"],red_width,resolution/2,translation_res,process_flag))
			current_process.start()
		elif command["commandType"]=="manual":
    		logging.info(f"manual command received: {command}")
			print('manual command received.')
			process_flag = False #stop and wait process to exit properly
			while current_process.is_alive():
    				print('Exiting the current process')
    				time.sleep(1)
			current_process = Process(target=move.manual, args=(command["manualType"],command["command"])) #no need to pass in process_flag because once manual command is sent, there's nothing to do about it on Pi side. Just need to wait for confirmation from teensy. If want to stop immediately, send 'stop' command.
			current_process.start()
		# elif command["commandType"] == "photo":
		# 	process_flag = False
		# 	while current_process.is_alive():
    	# 			print('Exiting the current process')
    	# 			time.sleep(1)
		# 	# active_command = "photo"
		# 	# STOP recording 
		# 	# take pano photo
		# 	# begin recording 
		# 	#todo
		# 	cam.take360()

		active_command = command #keep track of the last command in case of connection lost
		command = {} #clear command and wait for new command
	
		#return to top of loop
			


if __name__ == "__main__":
	main()
