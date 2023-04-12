# Luke
import struct
import serial
import time
import logging

class RoverUART:
    def __init__(self,teensy_port) -> None:
        #member var
        logging.info(f"attaching to {teensy_port}")
        self.ser = serial.Serial(teensy_port, 115200, timeout=1)
        self.lastmag = -999

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
        #print("TESTING")
        logging.info(f"sending translation command: meter: {meter}")
        mode = "t"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(meter))
        self.sendUartCmd(cmdString)

    def getMagneticAzm(self):
        """
        gets the azimuth to magnetic north
        """
        logging.info(f"asking for magnetic azm")
        _ = self.readAll()
        mode = "m"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(0.0))
        self.sendUartCmd(cmdString)
        time.sleep(0.1)
        mystring = self.readLine()
        #_ = self.readAll()
        try:
            #print(float(mystring[1:-1]))
            magval = float(mystring[1:-1])
            self.lastmag = magval
            print(magval)
            return magval
        except:
            logging.warning("mag string was not in expected form. string: {mystring}")
            return self.lastmag
        



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
        #if self.ser.in_waiting>0:
        to_return = self.ser.readline().decode("utf-8").rstrip()
        logging.info(f"read {to_return} from teensy")
        return to_return
        #return "nothing read"

    def readAll(self):
        """
        read from serial buffer until empty
        """
        #print("in readAll()")
        buffer = []
        while self.ser.in_waiting>0:
             print(".")
             #buffer.append(self.ser.readline().decode("utf-8").rstrip())
             buffer.append(self.ser.readline().decode("utf-8").rstrip())
        return buffer
