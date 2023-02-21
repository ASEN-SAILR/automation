# import sys
import matplotlib.pyplot as plt
 
# setting path
# sys.path.append('../.')

from RoverLidar import RoverLidar
import logging

if __name__ == "__main__":
    logging.info("begin main")
    logging.basicConfig(
        filename='lidar_log.log',
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s %(funcName)10s-   %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    # lidar_port = "/dev/tty/USB0"a
    lidar_port = "COM9"
    lidar = RoverLidar(port_name=lidar_port)
    logging.info("about to set mapParams")
    lidar.setMapParams(
                    x_lim=(0,3), 
                    y_lim=(-1,1), 
                    threshold=5, 
                    red_lim=(0.5,0.5), 
                    resolution=0.05
                    )

    x,y,x_chopped,y_chopped = lidar.getObstacles()
    
    fig,ax = plt.subplots()
    ax.scatter(x,y)

    fig,ax = plt.subplots()
    ax.scatter(x_chopped,y_chopped)
    plt.show()

    


