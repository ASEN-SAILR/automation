import time
from math import atan2, degrees
import board
import adafruit_lis3mdl

class RoverMagnet:
    def __init__(self): # -> None:
        #member vars

        #initialize stuff
        port = ""
        self.port = serial.Serial(port, baudrate=38400, timeout=1)
        self.sensor = adafruit_lis3mdl.LIS3MDL(port)


    def vector_2_degrees(x, y):
        angle = degrees(atan2(y, x))
        if angle < 0:
            angle += 360
        return angle


    def get_heading(_sensor):
        magnet_x, magnet_y, _ = _sensor.magnetic
        return vector_2_degrees(magnet_x, magnet_y)