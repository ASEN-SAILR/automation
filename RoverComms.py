"""
types of commands:
id: 0, timestamp: 08.45.32, type: autonomous, lat: 40.423, lon: -101.249,
id: 1, timestamp: 08.46.04, type: stop,
id: 2, timestamp: 08.46.45, type: manual, command: rotate, degrees: -45,
id: 3, timestamp: 08.48.10, type: photo, 

cmd_dict = {id:2,timestamp:08.46.45....}

print(cmd_dict['id'])
# 2

"""


class RoverComms:
    def __init__(self,commandPath,telemPath) -> None:
        # member vars
        self.commandPath = commandPath
        self.telemPath = telemPath
        self.currCmdNum = 0

        # initialize stuff as needed

        pass 

    def isNewCommand(self):
        """
        checks for a new command in the command file

        input:
            none
        returns:
            True if new command
            False if nothing new
        """

    def readCommand(self) -> dict:
        """
        read command from commands text file.
        
        Throw error if there are multiple new commands. 
        Clear commands if this happens and send message to gruond station

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