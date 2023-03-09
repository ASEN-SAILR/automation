import time
from math import atan2, degrees
import board
import adafruit_lis3mdl

class RoverMagnet:
    def __init__(self,port:str): # -> None:
        #initialize stuff
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.sensor = adafruit_lis3mdl.LIS3MDL(i2c)


    def vector_2_degrees(x, y):
        angle = degrees(atan2(y, x))
        if angle < 0:
            angle += 360
        return angle


    def get_heading(_sensor):
        magnet_x, magnet_y, _ = _sensor.magnetic
        return vector_2_degrees(magnet_x, magnet_y)