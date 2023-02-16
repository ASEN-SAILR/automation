# Luke
# https://github.com/adafruit/Adafruit_CircuitPython_RPLIDAR
import numpy as np
from adafruit_rplidar import RPLidar 

def radialToCart(ang:np.ndarray, dist:np.ndarray, type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]

    x = np.cos(ang)*dist
    y = np.sin(ang)*dist
    return x, y

class RoverLidar:
    def __init__(self, port:str, start_motor:bool=True, timeout:int=3,) -> None:
        # member vars
        self.port = port
        self._lidar = RPLidar(None,port,timeout)

        #map paramaters
        self.threshold = None
        self.x_lim = None
        self.y_lim = None
        self.red_lim = None
        self.resolution = None

        if not start_motor: 
            self.stopMotor() #RPLidar starts motor by default


    def setMapParams(self, x_lim:tuple[float], y_lim:tuple[float], threshold:int, 
                    red_lim:tuple[float] , resolution:float):
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

    def startMotor(self):
        self._lidar.start_motor()

    def stopMotor(self):
        self._lidar.stop_motor()

    def startSensing(self):
        self._lidar.start()

    def stopSensing(self):
        self._lidar.stop()

    def getSingleScan(self) -> list[tuple]:
        """
        Gets measurements from a single call to _lidar.iter_scans()
        TODO: how many rotations does this correspond to?
        """
        measurements = self._lidar.iter_scans()
        return np.array(list(measurements))

    def splitScan(self, scan):
        qualitites = scan[:,0]
        angles = scan[:,1]
        distances = scan[:,2]
        return qualitites,angles,distances

    def scanToMap(self,scan):
        _,angles, distances = self.splitScan(scan)

        x_points,y_points = radialToCart(scan)
        x_mag = self.x_lim[1]-self.x_lim[0]
        y_mag = self.y_lim[1]-self.y_lim[0]
    
        # the following array is a 1D array of bools. True means associated point is within x_lim and y_lim.
        truth_vals = np.all(np.vstack((x>self.x_lim[0], x<self.x_lim[1], y>self.y_lim[0], y<self.y_lim[1])),0)
        
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
    
        # create 2d array for objects 
        x_bins = int(x_mag//self.resolution)
        y_bins = int(y_mag//self.resolution)
        grid = np.zeros([x_bins,y_bins])

        # fills the grid with ones where there is an "object". 
        # Looks complicated because `objects` contains negative numbers which cannot be indices
        grid[objects[:,0]-(int(self.x_lim[0]/self.resolution)),objects[:,1]-(int(self.y_lim[0]/self.resolution))] = 1

        #get coordiantes of bins in final array
        x = np.arange(start=self.x_lim[0], stop=self.x_lim[1])
        y = np.arange(start=self.y_lim[0], stop=self.y_lim[1])
        xx,yy = np.meshgrid(x,y)

        return xx,yy,grid


    def getMap(self):
        """
        inputs:
            uses parameters from self.setMapParams() 
        returns:
            m x n 2D bool array with side lengths defined by x_lim and y_lim. True where 
            obstacles are deteceted, false otherwise.
        """
        if self._lidar.motor_running == False:
            self.startMotor()

        # start LiDAR laser and collection of data
        self.startSensing()

        # collect data from lidar
        scan = self.getSingleScan()

        # stop the LiDAR sensing, keep motor running
        # TODO: ensure the LiDAR stops
        self.stopSensing()

        #TODO: turn scans into map






    def getObstacles(self):
        """
        Inputs 
            map: 2d bool array, (0 -> empty, 1 -> object)
        returns
            color: color of zone where there are obstacles
            obstacles: coordiantes of obstacles located in map[(x1,y1),(x2,y2),...,(xn,yn)]  
        """
        color = None
        obstacles = None
        return color,obstacles