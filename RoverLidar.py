# Luke
# https://github.com/adafruit/Adafruit_CircuitPython_RPLIDAR

from adafruit_rplidar import RPLidar 
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
        return list(measurements)

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