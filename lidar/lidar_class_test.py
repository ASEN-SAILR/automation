import os
from math import floor
from adafruit_rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
import time
import logging
#https://github.com/SkoltechRobotics/rplidar

NAME = "TRR_scan_20230221_trash_"

def radialToCart(ang,dist,type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    x = np.multiply(np.cos(ang),dist)
    y = np.multiply(np.sin(ang),dist)
    return x, y

class LidarTest:
    # Setup the RPLidar
    def __init__(self) -> None:
        self.x_lim = None
        self.y_lim = None
        self.threshold = None
        self.red_lim = None
        self.resolution = None

    def splitScan(self, scan):
        qualitites = scan[:,0]
        angles = scan[:,1]
        distances = scan[:,2]
        logging.debug(f"splitScan ran. `distances` has length {len(distances)}")
        return qualitites,angles,distances

    def setMapParams(self, x_lim:tuple, y_lim:tuple, threshold:int, 
            red_lim:tuple, resolution:float):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.threshold = threshold
        self.red_lim = red_lim
        self.resolution = resolution

    
    def scanToMap(self,scan):
        _, angles, distances = self.splitScan(scan)
        distances /= 1000

        x_points,y_points = radialToCart(ang=angles, dist=distances, type='deg')
        x_mag = self.x_lim[1]-self.x_lim[0]
        y_mag = self.y_lim[1]-self.y_lim[0]
    
        # the following array is a 1D array of bools. True means associated point is within x_lim and y_lim.
        truth_vals = np.all(np.vstack((x_points>self.x_lim[0], x_points<self.x_lim[1], y_points>self.y_lim[0], y_points<self.y_lim[1])),0)
        
        # removes points outside of x_lim and y_lim
        x_chopped = x_points[truth_vals]
        y_chopped = y_points[truth_vals]
        

        # puts hit counts into integer coordnitates 
        # ex: x,y = (0.1,0.2) would be binned into (1,2) if the resolution was 0.1
        x_binned = [val//self.resolution for val in x_chopped]
        y_binned = [val//self.resolution for val in y_chopped]

        # this returns unique points (defined by coords in x_binned and y_binned) and their counts
        coords,counts = np.unique(list(zip(x_binned,y_binned)),return_counts=True,axis=0)

        # objects are points where there are more hits than the threshold 
        objects = np.array(coords[counts>self.threshold], dtype=np.int_)
        logging.info(f"there were {len(objects)} objects detected with a threshold of {self.threshold} and resoluton of {self.resolution}")
    
        # create 2d array for objects 
        x_bins = int(x_mag//self.resolution)
        y_bins = int(y_mag//self.resolution)
        object_map = np.zeros([x_bins,y_bins])

        # fills the grid with ones where there is an "object". 
        # Looks complicated because `objects` contains negative numbers which cannot be indices
        object_map[objects[:,0]-(int(self.x_lim[0]/self.resolution)+1),objects[:,1]-(int(self.y_lim[0]/self.resolution)+1)] = 1

        #get coordiantes of bins in final array
        x = np.arange(start=self.x_lim[0], stop=self.x_lim[1], step=x_mag/x_bins)
        y = np.arange(start=self.y_lim[0], stop=self.y_lim[1], step=y_mag/y_bins)
        xx,yy = np.meshgrid(y,x)

        logging.info("finished object map")
        return xx,yy,object_map,x_chopped,y_chopped

    def getMap(self):
        PORT_NAME = 'COM9'

        lidar = RPLidar(None, PORT_NAME, timeout=3)
        # lidar.reset()
        time.sleep(1)

        scan_time = 1


        all_scans = list([])
        try:
        #    print(lidar.get_info())
            count = 0
            while count<2:
                count+=1
                start_time = time.time()
                scan = []
                for temp_scan in lidar.iter_scans():
                    if(start_time+scan_time<time.time()):
                        break
                    # print(temp_scan)
                
                    for (_, angle, distance) in temp_scan:
                        pass
                    scan.extend(temp_scan)
                
                return np.array(scan)
                    
                # print(f"scan {count}")
                # np.save(os.path.join(r"C:\\Users\\luker\\Documents\\repos\\SAILR\\automation\\lidar\\data",f"{NAME}{count}.npy"),np.array(scan))
                # all_scans.append(scan)


        except KeyboardInterrupt:
            print("Didn't get data, maybe LiDar is disconnected")
            
            pass

        # print('scan',all_scans)

        # convert to x,y
        for i,scan in enumerate(all_scans):
            degs = [i for i in range(360)]
            qual,ang,dist = zip(*scan)

            x,y = radialToCart(ang,dist,type='deg')

            # print('x',x)
            # print('y',y)
            #plot
            fig, ax = plt.subplots(figsize=(8,8))
            plt.scatter(x,y);
            ax.set_title(f"{NAME}{i}", fontsize=18)
            ax.set_xlabel('x', fontsize=14)
            ax.set_ylabel('y', fontsize=14)
            ax.grid()
            ax.set_aspect('equal')
            plt.savefig(os.path.join(r"C:\\Users\\luker\Documents\\repos\\SAILR\\automation\\lidar\\images",f"{NAME}{i}.jpg"),dpi=200)
            # plt.close(fig)


        #stop (disconnects, but doesn't turn it off, idk why)
        # lidar.stop_motor()
        lidar.stop()
        lidar.disconnect()
        print('Stopping.')

if __name__ == "__main__":
    logging.basicConfig(
        filename='lidar_class_test.log',
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-3s %(funcName)10s-   %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')
    lidar = LidarTest()
    lidar.setMapParams(
                x_lim=(0,3), 
                y_lim=(-1,1), 
                threshold=0, 
                red_lim=(0.5,0.5), 
                resolution=0.1
                )
    scan = lidar.getMap()
    xx,yy,map,x_points,y_points = lidar.scanToMap(scan)

    fig,ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.plot_surface(xx,yy,map)

    fig,ax = plt.subplots()
    ax.scatter(x_points,y_points)

    plt.show()
