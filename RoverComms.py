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
import os

class RoverComms:
    def __init__(self,commandPath,telemPath,cameraPath):# -> None:
        # member vars
        self.commandPath = commandPath
        self.telemPath = telemPath
        self.cameraPath = cameraPath
        self.currCmdNum = 0

        # initialize stuff as needed

    #probably not needed now?
    #def isNewCommand(self): 
        """
        checks for a new command in the command file

        input:
            none
        returns:
            command index if new command
            False if nothing new
        """
    #    file = open(self.commandPath)
    #    cmdNum = int(file.readline(1))
    #    if cmdNum>self.currCmdNum:
    #        return cmdNum

    #    return False

    def readCommand(self): # -> dict or None:
        
        """
        read command from commands text file.
        
        **Throw error if there are multiple new commands. 
        Clear commands if this happens and send message to ground station** maybe not, maybe just take the latest command?

        inputs:
            none
        return:
            dictionary of command (FORMAT TBD)
            None if there is no command
        """
        file = open(self.commandPath)
        line = file.readline()
        if int(line[0]) > self.currCmdNum+1:
            #sendError("")
            return

        #if not error, increment currCmdNum and return a dictionary of command
        self.currCmdNum += 1

        lin = line.split()
        
        return {"mode" : lin[1],
        "command" : lin[2],
        "dist" : float(lin[3]),
        "LOI" : lin[4].split(',')}

    def writeTelemetry(self,toWrite): # -> bool:
        """
        write telemetry to telemetry file

        input:
            toWrite: telemetry to write to file (FORMAT TBD)
        """

        with open(self.telemPath, 'a') as f:
            f.write('\n'+toWrite)
        

    def syncOutbound(self,path):
        system_password = 'asen4018'
        sender_path = '/root/comms-gs/test.txt'
        receiver_ip = '192.168.56.102'
        receiver_path = receiver_ip+':/root/comms-gs/test.txt'

        # os.system("sshpass -p '"+system_password+"' rsync -ave ssh /root/comms-gs/test.txt 192.168.56.102:/root/comms-gs/test.txt")
        os.system("sshpass -p '"+system_password+"' rsync -ave ssh "+sender_path+" "+receiver_path)


comm = RoverComms("commandTest.txt","teleTest.txt",3)
#print(comm.isNewCommand())
comm.writeTelemetry('102,103')
print(comm.readCommand())