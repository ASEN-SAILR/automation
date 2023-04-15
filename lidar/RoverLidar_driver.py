import sys
import matplotlib.pyplot as plt
import numpy as np
import time

# setting path
sys.path.append('../.')
sys.path.append('.')

from RoverLidar import RoverLidar
import logging

DATA_NAME = "lidar_test_20200222_"

if __name__ == "__main__":
    logging.info("begin main")
    logging.basicConfig(
        filename='lidar_log.log',
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s %(funcName)10s-   %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    lidar_port = "/dev/ttyUSB0"
    #lidar_port = "COM9"
    lidar = RoverLidar(port_name=lidar_port)
    logging.info("about to set mapParams")
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
    # path = r"C:\Users\luker\OneDrive - UCB-O365\Classes\2023_spring\ASEN 4028\Teams Shortcuts\General\JPL Senior Projects\Testing\LiDAR Testing Material\data\TRR_scan_15_spray_paint.npy"
    # scan = np.load(path)
    while True:
        color,objects,points = lidar.getObstacles(2)
        print(objects)

        fig,ax = plt.subplots()
        ax.scatter(points[:,0],points[:,1])
        ax.set_title(DATA_NAME+"hits")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_xlim(x_lim*1.1)
        ax.set_ylim(y_lim*1.1)
        ax.set_aspect("equal")
        ax.grid()

        fig,ax = plt.subplots()
        ax.scatter(objects[:,0],objects[:,1])
        ax.set_title(DATA_NAME+"Obstacles")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_xlim(x_lim*1.1)
        ax.set_ylim(y_lim*1.1)
        ax.set_aspect("equal")
        ax.grid()

       # plt.show()
        #time.sleep(5)
        #plt.close('all')
    


