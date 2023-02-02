# Luke
class RoverUART:
    def __init__(self) -> None:
        #member vars

        #initialize

        pass

    def sendStopCmd(self):
        """
        send stop command to teensy
        """
        cmdString = "we need a standard for this"
        self.sendUartCmd(cmdString)

    def sendRotateCmd(self,rad) -> bool:
        """
        sends teensy a command to rotate over UART connection
        """
        cmdString = "we need a standard for this"
        self.sendUartCmd(cmdString)

    def sendTranslateCmd(self,rotation):
        """
        sends teensy a command to translate over UART connection
        """
        cmdString = "we need a standard for this"
        self.sendUartCmd(cmdString)
        

    def sendUartCmd(self,cmd):
        """
        sends the cmd specified by cmd
        """
        pass