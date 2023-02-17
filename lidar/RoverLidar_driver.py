import sys
 
# setting path
sys.path.append('../.')

import RoverLidar

if __name__ == "__main__":
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

    


