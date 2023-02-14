# Luke
# https://github.com/adafruit/Adafruit_CircuitPython_RPLIDAR

from adafruit_rplidar import RPLidar 
class RoverLidar:
    def __init__(self, port:str, threshold:int, start_motor:bool=True, timeout:int=3,) -> None:
        # member vars
        self.port = port
        self._lidar = RPLidar(None,port,timeout)

        

        if not start_motor: self.stopMotor() #RPLidar starts motor by default

        # begin lidar rotation

        pass

    def startMotor(self):
        self._lidar.start_motor()

    def stopMotor(self):
        self._lidar.stop_motor()

    def startSensing(self):
        self._lidar.start()

    def stopSensing(self):
        self._lidar.stop()

    def getSingleScan(self):
        measurements = self._lidar.iter_scans()
        return list(measurements)

    def getMap(self):
        """
        returns a 2d array of "objects"
        """
        if self._lidar.motor_running == False:
            self.startMotor()

        self.startSensing()
        scan = self.getSingleScan()
        

        pass

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