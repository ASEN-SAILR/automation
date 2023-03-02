# Luke
import struct
import serial
class RoverUART:
    def __init__(self,teensy_port) -> None:
        #member vars
        self.ser = serial.Serial(teensy_port, 115200, timeout=1)
    
        #initialize

        

    def sendStopCmd(self):
        """
        TODO: send stop command to teensy
        """
        cmdString = "we need a standard for this"
        self.sendUartCmd(cmdString)

    def sendRotateCmd(self,rad) -> bool:
        """
        sends teensy a command to rotate over UART connection
        """
        cmdString = "r" + struct.pack("<f",rad)
        self.sendUartCmd(cmdString)

    def sendTranslateCmd(self,rotation):
        """
        TODO: sends teensy a command to translate over UART connection
        """
        cmdString = "we need a standard for this"
        self.sendUartCmd(cmdString)
        

    def sendUartCmd(self,cmd):
        """
        sends the cmd specified by cmd
        """
        self.ser.write(cmd)

    def readFromTeensy(self):
        # TODO: reads message from teensy
        pass

    def teensyMsgAvail(self):
        if self.ser.in_waiting>0:
            return True
        return False