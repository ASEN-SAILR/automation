# Suphakan
#https://github.com/sparkfun/Qwiic_Ublox_Gps_Py
from ublox_gps import UbloxGps
import serial

import math
import time
import RoverComms
from multiprocessing import Process


## all coordinates must be in deg-decimal form, not hour-min-sec

class RoverGPS:
    def __init__(self,port:str): # -> None:
        #member vars

        #initialize stuff
        #self.comms = comms
        self.precision = 1.15
        self.port = serial.Serial(port, baudrate=38400, timeout=1)

    def readAndWriteAndSendTele(self):
        while True:
            gps = UbloxGps(self.port)
            geo = gps.geo_coords() #read GPS
            #self.comms.writeAndSendTelemetry('1,2') 
            self.comms.writeAndSendTelemetry(str(geo.lon)+','+str(geo.lat)) #write and send
    def readGPS(self):
        gps = UbloxGps(self.port)
        geo = gps.geo_coords()
        #print(geo.lon,geo.lat)
        return [geo.lon,geo.lat]
    def startTele(self):
        self.process = Process(target=self.readAndWriteAndSendTele)
        self.process.start()

    def stopTele(self):
        if self.process.is_alive():
            self.process.terminate()

    def atloi(self,LOI):
        return self.distanceToTarget(LOI)<self.precision

    def __bearingToTarget(self,tarCoor:list): # -> float:
        """
        input: 
            currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: 
            bearing in deg from north, ie. 89 (float)
        """
        #input: currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        #output: bearing in deg from north, ie. 89 (float)
        
        lat1, lon1 = self.readGPS() #self.__getGPS()
        lat2, lon2 = tarCoor
        #print(lat1,lon1)
        deg2rad = math.pi/180
        lat1 = lat1*deg2rad
        lon1 = lon1*deg2rad
        lat2 = lat2*deg2rad
        lon2 = lon2*deg2rad
        
        a = math.sin(lon2-lon1)*math.cos(lat2)
        b = math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
        bearing = math.atan2(a,b) #in rad
        return bearing*180/math.pi #convert to deg

    def distanceToTarget(self,tarCoor:list): # -> float: 
        """
        input: currCoor, tarCoor = [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: distance to target in meter (float)
        """
        lat1, lon1 = self.readGPS() #self.__getGPS()
        lat2, lon2 = tarCoor

        deg2rad = math.pi/180
        lat1 = lat1*deg2rad
        lon1 = lon1*deg2rad
        lat2 = lat2*deg2rad
        lon2 = lon2*deg2rad

        EarthRadiusMeter = 6371000
        
        #haversine formula
        a = (math.sin((lat2-lat1)/2.0))**2 + math.cos(lat1)*math.cos(lat2)*(math.sin((lon2-lon1)/2))**2
        c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        meter = EarthRadiusMeter * c
        return meter;

    def angleToTarget(self,tarCoor:list,currHeading:float): # -> float:
        """
        input: 
            currHeading = current heading to target from magnetometer in deg (float)
        output: 
            angle to target with respect to current heading in deg, positive mean to the right (float)
        """
        return self.__bearingToTarget(tarCoor)-currHeading

    def getGPS(self): # -> list of float
        with open(self.comms.obcTelemPath) as f:
            file = f.read().splitlines()
        coor = file[0].split(',')
        coor = [float(coor[0]),float(coor[1])]
        #print(coor)
        return coor

