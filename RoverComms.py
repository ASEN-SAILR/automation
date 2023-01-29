class RoverComms:
    def __init__(self,commandPath,telemPath) -> None:
        # member vars
        self.commandPath = commandPath
        self.telemPath = telemPath

        # initialize stuff as needed

        pass 

    def readCommand(self) -> dict:
        """
        read command from commands text file

        inputs:
            none
        return:
            dictionary of command (FORMAT TBD)
            None if there is no command
        """
        pass

    def writeTelemetry(self,toWrite) -> bool:
        """
        write telemetry to telemetry file

        input:
            toWrite: telemetry to write to file (FORMAT TBD)
        """
        pass