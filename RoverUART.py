# Luke
import struct
import serial
import time

class RoverUART:
    def __init__(self,teensy_port) -> None:
        #member vars
        self.ser = serial.Serial(teensy_port, 115200, timeout=1)

    def sendStopCmd(self):
        """
        send stop command to teensy
        """
        cmdString = "s" + struct.pack("<f",0.0)
        self.sendUartCmd(cmdString)

    def sendRotateCmd(self,rad) -> bool:
        """
        sends teensy a command to rotate over UART connection
        """
        cmdString = "r" + struct.pack("<f",rad)
        self.sendUartCmd(cmdString)

    def sendTranslateCmd(self,meter):
        """
        sends teensy a command to translate over UART connection
        """
        cmdString = "t" + struct.pack("<f",meter)
        self.sendUartCmd(cmdString)

    def getMagneticAzm(self):
        """
        gets the azimuth to magnetic north
        """
        cmdString = "m" + struct.pack("<f",0.0)
        self.sendUartCmd(cmdString)
        time.sleep(0.25)
        string = self.readLine()
        if string[0] != 'm':
            return -999
        return float(string[1:-1])



    def sendUartCmd(self,cmd):
        """
        sends the command specified by cmd
        """
        self.ser.write(cmd)
 
    def msgsWaiting(self):
        """
        returns number lines available to read from teensy
        """
        return self.ser.in_waiting


    def readLine(self):
        """
        read from serial buffer until a newline is reached
        """
        if self.ser.in_waiting>0:
            return self.ser.readline()
        return -1