import sys
import matplotlib.pyplot as plt
import numpy as np
import time
 
# setting path
sys.path.append('../.')
sys.path.append('.')

from RoverLidar import RoverLidar
import logging

if __name__ == "__main__":
    port = "dev/ttyUSB0"
    lidar = RoverLidar()
    x_lim=np.array((0,3)) 
    y_lim=np.array((-2,2))
    threshold=0
    red_lim=np.array((0.5,0.5))
    resolution=0.1
    lidar.setMapParams(
                    x_lim=x_lim, 
                    y_lim=y_lim, 
                    threshold=threshold, 
                    red_lim=red_lim, 
                    resolution=resolution
                    )
    
    while True:
        color,objects,points = lidar.getObstacles(2)
        time.sleep(1)
