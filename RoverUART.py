# Luke
import struct
import serial
import time
import logging

class RoverUART:
    def __init__(self,teensy_port) -> None:
        #member vars
        self.ser = serial.Serial(teensy_port, 115200, timeout=1)

    def sendStopCmd(self):
        """
        send stop command to teensy
        """
        mode = "s"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(0.0))
        self.sendUartCmd(cmdString)

    def sendRotateCmd(self,rad) -> bool:
        """
        sends teensy a command to rotate over UART connection
        """
        logging.info(f"sending rotation command: rad: {rad}")
        mode = "r"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(rad))
        self.sendUartCmd(cmdString)

    def sendTranslateCmd(self,meter):
        """
        sends teensy a command to translate over UART connection
        """
        logging.info(f"sending translation command: meter: {meter}")
        mode = "t"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(meter))
        self.sendUartCmd(cmdString)

    def getMagneticAzm(self):
        """
        gets the azimuth to magnetic north
        """
        logging.info(f"asking for magnetic azm")
        mode = "m"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(0.0))
        self.sendUartCmd(cmdString)
        time.sleep(0.25)
        mystring = self.readLine().decode('utf-8').rstrip()
        if mystring[0] != 'm':
            return -999
        try:
            return float(mystring[1:-1])
        except:
            logging.warning("mag string was not in expected form. string: {mystring}")
            return 0
        



    def sendUartCmd(self,cmd):
        """
        sends the command specified by cmd
        """
        logging.info(f"sending {cmd} to teensy")
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
            to_return = self.ser.readline()
            logging.info(f"read {to_return} from teensy")
            return to_return
        return -1

    def readAll(self):
        """
        read from serial buffer until empty
        """
        buffer = []
        while self.ser.in_waiting>0:
             #buffer.append(self.ser.readline().decode("utf-8").rstrip())
             buffer.append(self.ser.readline())
        return buffer
