import sys
 
# setting path
sys.path.append('../.')

import RoverLidar
import logging

if __name__ == "__main__":
    logging.basicConfig(
        filename='lidar_log.log',
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s %(funcName)10s-   %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    lidar_port = "/dev/tty/USB0"
    lidar = RoverLidar(port = lidar_port)
    lidar.setMapParams(
                    x_lim=(0,3), 
                    y_lim=(-1,1), 
                    threshold=0, 
                    red_lim=(0.5,0.5), 
                    resolution=0.1
                    )

    xx,yy,map = lidar.getMap()

    


