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
Obstacles_np = np.load('ObstacleGrid.npy') 
pdb.set_trace()

