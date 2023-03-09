# Luke
# https://github.com/adafruit/Adafruit_CircuitPython_RPLIDAR
import numpy as np
import time
import logging
from adafruit_rplidar import RPLidar 

def radialToCart(ang, dist:np.ndarray, type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]

    x = np.cos(ang)*dist
    y = np.sin(ang)*dist
    return x, y

class RoverLidar:
    def __init__(self,port_name) -> None:

        self._lidar = RPLidar(None, port_name, timeout=3)

        self.x_lim = None
        self.y_lim = None
        self.threshold = None
        self.red_lim = None
        self.resolution = None

        logging.info("RoverLidar __init__: RoverLidar initialized")


    def setMapParams(self, x_lim:tuple, y_lim:tuple, threshold:int, 
            red_lim:tuple, resolution:float):
        """
        Sets paramaters for getting the object map.
        Assumed body X axis points forward, Y out the right side, Z down
        inputs:
            x_lim [m]: limits of object reporting along x axis
            y_lim [m]: limits of object reporting along y axis
            threshold [number]: number of points needed in a bin to register as an obstacle
            red_lim [m]: the limits of the "red zone" along the x axis (no y axis limit needed)
            resolution [m]: defines the side length of the bins in the 2D array. Will round up
                to get a value that evenly fits each dimension depcified by x_lim and y_lim
        returns: 
            none
        """
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.threshold = threshold
        self.red_lim = red_lim
        self.resolution = resolution
        self._map_params_set = True

        if ((x_lim[1]-x_lim[0])/resolution != int((x_lim[1]-x_lim[0])/resolution)):
            logging.warning(f"The limits defined by x_lim ({x_lim}) are not evenly dividable by the resoltion ({resolution}). Not the end of the world but bins will have a slightly different spacing.")

        if ((y_lim[1]-y_lim[0])/resolution != int((y_lim[1]-y_lim[0])/resolution)):
            logging.warning(f"The limits defined by y_lim ({y_lim}) are not evenly dividable by the resoltion ({resolution}). Not the end of the world but bins will have a slightly different spacing.")

        logging.debug("RoverLidar setMapParams: map paramaters set")

    def startMotor(self):
        val = self._lidar.start_motor()
        logging.debug(f"motor started with return value of {val}")

    def stopMotor(self):
        val = self._lidar.stop_motor()
        logging.debug(f"motor stopped with return value of {val}")

    def startSensing(self):
        val = self._lidar.start()
        logging.debug(f"sensing started with raturn value of {val}")

    def stopSensing(self):
        val = self._lidar.stop()
        logging.debug(f"sensing stopped with return value of {val}")

    def getSingleScan(self) -> list:
        """
        Gets measurements from a single call to _lidar.iter_scans()
        kinda sucks don't use.
        TODO: how many rotations does this correspond to?
        """
        scan = []
        for temp_scan in self._lidar.iter_scans():           
            
            #I don't think the following for loop is needed 
            for (_, angle, distance) in temp_scan:
                pass
            scan = temp_scan
            break
        scan = np.ndarray(scan)
        logging.warning("This method kinda sucks. Use RoverLidar.getTimedScan instead.")
        logging.debug(f"`measurements` has dimensions of {scan.shape}")
        return scan
    
    def getTimedScan(self, scan_time):
        """
        scans for a certian amount of time. Actually isn't 
        going to be super accurate in terms of how long it 
        scans for beacuse self._lidar.iter_scans() takes a 
        variable amount of time.
        """
        start_time = time.time()
        scan = []
        for temp_scan in self._lidar.iter_scans():
            if(start_time+scan_time<time.time()):
                break
            # print(temp_scan)
        
            for (_, angle, distance) in temp_scan:
                pass
            scan.extend(temp_scan)
        
        return np.array(scan)

    def splitScan(self, scan):
        qualitites = scan[:,0]
        angles = scan[:,1]
        distances = scan[:,2]
        logging.debug(f"splitScan ran. `distances` has length {len(distances)}")
        return qualitites,angles,distances

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
        return xx,yy,object_map,x_binned,y_binned


    def getMap(self):
        """
        inputs:
            uses parameters from self.setMapParams() 
        returns:
            m x n 2D bool array with side lengths defined by x_lim and y_lim. True where 
            obstacles are deteceted, false otherwise.
        """
        if not self._map_params_set: 
            logging.critical("RoverLidar getMap: Map paramaters not set. Use RoverLidar.setMapParams() to set map paramters.")
            raise Exception("RoverLidar getMap: Map paramaters not set. Use RoverLidar.setMapParams() to set map paramters.")

        # if self._lidar.motor_running == False:   
        #     self.startMotor()

        # start LiDAR laser and collection of data
        #self.startSensing()

        # collect data from lidar
        scan = self.getTimedScan(2) #scans for 1 second 

        # stop the LiDAR sensing, keep motor running
        # TODO: ensure the LiDAR stops
        #self.stopSensing()

        #TODO: turn scans into map
        xx,yy,grid,x_binned,y_binned = self.scanToMap(scan=scan)
        
        return xx,yy,grid





    def getObstacles(self,scan_time=None,scan=None):
        """
        Inputs 
            map: 2d bool array, (0 -> empty, 1 -> object)
        returns
            color: color of zone where there are obstacles
            obstacles: coordiantes of obstacles located in map[(x1,y1),(x2,y2),...,(xn,yn)]  
        """

        #if a scan is not specifid, take a scan for time specified by `scan_time`
        if scan_time is None and scan is None:
            raise Exception("One of scan_time and scan must be defined")
        
        if scan is None:
            scan = self.getTimedScan(scan_time)

        _, angles, distances = self.splitScan(scan)
        distances /= 1000 # mm to m

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
        objects = objects*self.resolution

        if objects.size == 0:
            color = None
        else:
            color = "yellow"
            for object in objects:
                #print(f"comparing {abs(object[1])} with {abs(self.red_lim[0])}")
    

                if abs(object[1]) < abs(self.red_lim[0]):
                    color = "red" 

        return color,objects,coords*self.resolution