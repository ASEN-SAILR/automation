import RoverMove
import sys
sys.path.append("../")
import RoverGPS
import RoverLidar
import numpy as np
import pdb

# start lidar
lidar_port = r"/dev/tty/2"
lidar = RoverLidar(lidar_port) # more params?

# start gps 
gps_port = r"/dev/tty/2"
gps = RoverGPS(comms,gps_port) # more params?

# start move
move = RoverMove(gps,lidar)
#Testing check_desired_heading function
#Should return true
Value1 = move.check_desired_heading(50,51)
#Should return false
Value2 = move.check_desired_heading(50,53)
if Value1 == 1 and Value2 == 0:
	print('check_desired_heading passed')
else:
	print('check_desired_heading failed')

#Testing get_delta_rotation function
Obstacles_grid = [[.3,-1.5],[.6,1.5]]
Value1 = move.get_delta_rotation(Obstacles_grid)
if abs(Value1) > 0:
	print('get_delta_rotation passed')
else:
	print('get_delta_rotation failed')

#Testing get_delta_distance function
Value1 = move.get_delta_distance(Obstacles_grid)
if Value1 == 1.6:
	print('get_delta_distance passed')
else:
	print('get_delta_distance failed')



#Testing autonomous function
move.autonomous(1)
pdb.set_trace()
