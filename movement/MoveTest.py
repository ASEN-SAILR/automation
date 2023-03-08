import MovementDev as move
import numpy as np
import pdb

#Testing check_desired_heading function
#Should return true
Value1 = move.RoverMove.check_desired_heading(50,54)
#Should return false
Value2 = move.RoverMove.check_desired_heading(50,56)
if Value1 == 1 and Value2 == 0:
	print('check_desired_heading passed')
else:
	print('check_desired_heading failed')

#Testing get_delta_rotation function
Obstacles_grid = [[.3,-1.5],[.6,1.5]]
Value1 = move.RoverMove.get_delta_rotation(Obstacles_grid)
if abs(Value1) > 0:
	print('get_delta_rotation passed')
else:
	print('get_delta_rotation failed')

#Testing get_delta_distance function
Value1 = move.RoverMove.get_delta_distance(Obstacles_grid)
if Value1 == 1.6:
	print('get_delta_distance passed')
else:
	print('get_delta_distance failed')


