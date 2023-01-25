LOI = argv[0]
while not atlocation
	#Finding change in heading desired to point to LOI
	CurrCoordinate = get_gps()
	MagHeading = get_heading()
	DesHeading = bearing_to_target(CurrCoordinate,LOI)
	DeltaHeading = get_delta_heading(MagHeading,DesHeading)
	#Sending command to teensy
	send_uart_cmd('angle',DeltaHeading)
	#If fail, spit error
	wait for success
		loop here
	end
	#Getting lidar map and finding what zone they are in
	#Priming for loop
	Map = get_lidar_map()
	[Status,Obstacles] = check_obstacles(Map)
	while Status is none
		if check_desired_heading()
			send_uart_cmd('translation',DISTANCE)
			wait for success
				loop here
			end
			Map = get_lidar_map()
			[Status,Obstacles] = check_obstacles(Map)
		else
			break
	while Status is yellow
		here
	while Status is red
		here



	
