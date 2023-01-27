DISTANCE = 1 #distance to move in a straight line

LOI = argv[0]

def send_translation(distance):
	send_uart_cmd("translation",distance)

def send_rotation(angle):
	send_uart_cmd("angle",angle)




### Autonomous Mode ###
def autonomous():
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
			else
				break
		while Status is "yellow":
			here
		while Status is "red"
			here

def manual():
	#insert code 
	return



	
