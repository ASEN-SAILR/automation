import RoverMove
import RoverComms
import RoverGPS
import RoverLidar
import RoverVideo
import RoverUART
from multiprocessing import Process

DISTANCE = 1 #distance to move in a straight line

if __name__ == "__main__":
	# start video recording (class)
	camPort = r"/dev/tty/0"
	videoPath = r"~/videos/" #example path
	video = RoverVideo(camPort,videoPath,vidLength=5)
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

	while True:
		command = None
		while command == None:
			command = comms.readCommand()
			#once a command is recieved, we need a way to monitor motion


		if command["type"] == "autonomous":
			# multiprodcessing process for this???  
			# can we make autonomous only perform one action at a time? below is what a multiprocessing process would look like
			auton_process = Process(target=move.autonomous,args=command["LOI"])
			auton_process.start() 
			

			# monitor process
			# tbc
			
		elif command["type"] == "manual":
			# multiprodcessing process for this???  
			move.manual(command) #just send the whole dictionary?
			#tbc

		elif command["type"] == "photo":
			#todo
			pass

		elif command["type"] == "stop":
			uart.sendStopCmd
			# skip over rest of loop and wait for command
			continue
