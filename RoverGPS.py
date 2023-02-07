# Suphakan

import serial
import math
from ublox_gps import UbloxGps

class RoverGPS:
    def __init__(self,port,tarCoor): # -> None:
        #member vars

        #initialize stuff
        self.tarCoor = tarCoor
        self.port = port

    def bearingToTarget(currCoor): # -> float:
        """
        input: 
            currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: 
            bearing in deg from north, ie. 89 (float)
        """
        #input: currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        #output: bearing in deg from north, ie. 89 (float)
        
        lat1, lon1 = self.readGPS()
        lat2, lon2 = self.tarCoor

        deg2rad = math.pi/180
        lat1 = lat1*deg2rad
        lon1 = lon1*deg2rad
        lat2 = lat2*deg2rad
        lon2 = lon2*deg2rad
        
        a = math.sin(lon2-lon1)*math.cos(lat2)
        b = math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
        bearing = math.atan2(a,b) #in rad
        return bearing*180/math.pi #convert to deg

    def distanceToTarget(currCoor,tarCoor): # -> float: 
        """
        input: currCoor, tarCoor = [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: distance to target in meter (float)
        """
        lat1, lon1 = self.readGPS()
        lat2, lon2 = self.tarCoor

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

    def angleToTarget(currHeading): # -> float:
        """
        input: 
            currHeading = current heading to target from magnetometer in deg (float)
            currCoor, tarCoor = current and target coordinate [lat,lon], ie. [23.0231,-34.204] (object of strings)
        output: 
            angle to target with respect to current heading in deg, positive mean to the right (float)
        """
        return bearingToTarget(self.readGPS(),self.tarCoor)-currHeading

    def readGPS(self):

        port = serial.Serial(self.port, baudrate=38400, timeout=1)
        gps = UbloxGps(port)
        geo = gps.geo_coords()
        return [geo.lon,geo.lat]
