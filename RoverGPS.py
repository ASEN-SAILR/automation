# Suphakan

import serial
import math
import time
import RoverComms
from ublox_gps import UbloxGps

class RoverGPS:
    def __init__(self,comms:RoverComms,port): # -> None:
        #member vars

        #initialize stuff
        self.comms = comms
        self.port = port

    def writeTele(self):
        t = time.time()
        while True:
            if time.time()-t>5:
                t = time.time()
                comms.writeTelemetry(self.readGPS())

    def startTele(self):
        self.recordingProcess = Process(target=self.writeTele,args=None)
        self.recordingProcess.start()

    def stopTele(self):
        self.recordingProcess = Process(target=self.writeTele,args=None)
        self.recordingProcess.terminate()


    def bearingToTarget(self,tarCoor): # -> float:
        """
        input: 
            currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: 
            bearing in deg from north, ie. 89 (float)
        """
        #input: currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        #output: bearing in deg from north, ie. 89 (float)
        
        lat1, lon1 = self.readGPS()
        lat2, lon2 = tarCoor

        deg2rad = math.pi/180
        lat1 = lat1*deg2rad
        lon1 = lon1*deg2rad
        lat2 = lat2*deg2rad
        lon2 = lon2*deg2rad
        
        a = math.sin(lon2-lon1)*math.cos(lat2)
        b = math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
        bearing = math.atan2(a,b) #in rad
        return bearing*180/math.pi #convert to deg

    def distanceToTarget(self,tarCoor): # -> float: 
        """
        input: currCoor, tarCoor = [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: distance to target in meter (float)
        """
        lat1, lon1 = self.readGPS()
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

    def angleToTarget(self,tarCoor,currHeading): # -> float:
        """
        input: 
            currHeading = current heading to target from magnetometer in deg (float)
        output: 
            angle to target with respect to current heading in deg, positive mean to the right (float)
        """
        return self.bearingToTarget(self.readGPS(),tarCoor)-currHeading

    def readGPS(self):

        gps = UbloxGps(self.port)
        geo = gps.geo_coords()
        return [geo.lon,geo.lat]

port = serial.Serial('/dev/ttyACM0', baudrate=38400, timeout=1)
gps = RoverGPS(port,[12.02,34.42])

while True:
    t = time.time()
    print(gps.readGPS())
    print(time.time()-t)
