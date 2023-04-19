# Suphakan
#https://github.com/sparkfun/Qwiic_Ublox_Gps_Py
from ublox_gps import UbloxGps
import serial
import logging
from datetime import datetime
import pytz
import math
import time
import RoverComms
from multiprocessing import Process,Value


## all coordinates must be in deg-decimal form, not hour-min-sec

class RoverGPS:
    def __init__(self,gpsport:str,comms:RoverComms): # -> None:
        #member vars

        #initialize stuff
        self.comms = comms
        self.precision = 5
        self.gps_port = gpsport
        self.tele_flag = Value('b',True)
        # self.ser = serial.Serial(port, baudrate=38400, timeout=1)

    def readAndWriteAndSendTele(self,gps_port,tele_flag):
        def readGPS(ser): #only for testing, on actual rover implementation, never call this
            gps = UbloxGps(ser)
            geo = gps.geo_coords()
            #print(geo.lat,geo.lon)
            return [geo.lat,geo.lon]
        # print('tele_flag: ',tele_flag)
        ser = serial.Serial(gps_port, baudrate=38400, timeout=1)
        while tele_flag.value:
            coor = readGPS(ser)
            #self.comms.writeAndSendTelemetry('1,2') 
            logging.info(f"writing {coor} to telem file")
            print("Sending telem")
            lineToWrite = str(coor[0])+','+str(coor[1])+', '+str(datetime.now(pytz.timezone('US/Mountain')))[:-10]
            #self.writeLocalTXT(lineToWrite)
            self.comms.writeAndSendTelemetry(lineToWrite) #write and send

    def writeLocalTXT(self,gpsStr:str): #temporary use for testing without comms
        with open('telemetry.txt') as f:
            lines = f.read().splitlines()
            if len(lines)>=99999: #1 sec per 1 point
                lines=lines[1:]
        with open('telemetry.txt', 'w') as f:
            for line in lines:
                f.write(line+'\n')
            f.write(gpsStr+'\n')
    
    def startTele(self):
        self.process = Process(target=self.readAndWriteAndSendTele,args=(self.gps_port,self.tele_flag,))
        self.process.daemon = True
        self.process.start()

    def stopTele(self):
        self.tele_flag.value = False #this ensure we end it properly without causing any error
        # if self.process.is_alive():
        #     self.process.terminate()

    def atloi(self,LOI):
        return self.distanceToTarget(LOI)<self.precision

    def bearingToTarget(self,tarCoor:list): # -> float:
        """
        input: 
            currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: 
            bearing in deg from north, ie. 89 (float)
        """
        #input: currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        #output: bearing in deg from north, ie. 89 (float)
        
        lat1, lon1 = self.getGPS()
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
        lat1, lon1 = self.getGPS()
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
        bearingToTar = self.bearingToTarget(tarCoor)-currHeading
        if abs(bearingToTar)>180:
            if bearingToTar < 0:
                bearingToTar = 360-abs(bearingToTar)
            else:
                bearingToTar = bearingToTar-360
        #print(bearingToTar)
        return bearingToTar

    def getGPS(self): # -> list of float
        #with open(self.comms.obcTelemPath) as f:
        with open('telemetry.txt') as f: #temporary for testinng
            file = f.read().splitlines()
        coor = file[-1].split(', ')
        # coor = coor.split(',') 
        coor = coor[0].split(',')
        coor = [float(coor[0]),float(coor[1])] # [123,123]
        #print(coor)
        return coor

