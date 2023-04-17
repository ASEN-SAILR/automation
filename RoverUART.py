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

    def getMagneticAzm(self,timeout=3):
        """
        gets the azimuth to magnetic north
        """
        logging.info(f"asking for magnetic azm")
        _ = self.readAll()
        mode = "m"
        cmdString = mode.encode("utf-8") + struct.pack("<f",float(0.0))
        self.sendUartCmd(cmdString)

        
        
        
        start_time = time.time()
        try:
            while((time.time()-start_time) < timeout):
                time.sleep(0.2)
                mystring = self.readLine()
                if mystring[0:1] == 'm':
                    #print(float(mystring[1:-1]))
                    magval = float(mystring[1:-1])
                    self.lastmag = magval
                    print("UART Mag: ",magval)
                    return magval
        except: 
            pass
        logging.warning("mag string was not in expected form. string: {mystring}")
        print("Mag failed")
        return self.lastmag
        



    def sendUartCmd(self,cmd):
        """
        sends the command specified by cmd
        """
        self.readAll()
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
        #print(f"uart readLine(): {to_return}")
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
             #print(".")
             #buffer.append(self.ser.readline().decode("utf-8").rstrip())
             buffer.append(self.ser.readline().decode("utf-8").rstrip())
        return buffer
    
    def checkMotionStatus(self,timeout=10):
        start_time = time.time()
        #line = self.readLine()
        while((time.time()-start_time) < timeout):
            time.sleep(0.1)
            line = self.readLine()
            print("checking motion status")
            if line == 'd':
                logging.info(f"motion complete recieved after {time.time()-start_time} seconds")
                print(f"confimraiton of motion complete recieved after {time.time()-start_time} seconds")
                return True
        logging.warning(f"no confimraiton of motion complete recieved after {timeout} seconds")
        print(f"no confimraiton of motion complete recieved after {timeout} seconds")
        return False
            
