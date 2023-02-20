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
    def __init__(self,obcCommandPath,obcTelemPath,obcVideoPath,obcImagePath,gs_ssh_password,gs_ip,gs_telem_path,gs_video_path,gs_image_path):# -> None:
    
        # onboard computer vars
        self.obcCommandPath = obcCommandPath
        self.obcTelemPath = obcTelemPath
        self.obcVideoPath = obcVideoPath
        self.obcImagePath = obcImagePath
        self.currCmdNum = 0

        # ground station vars
        self.gs_ssh_password = gs_ssh_password #'asen4018'
        self.gs_ip = gs_ip #'192.168.56.102'

        self.gs_telem_path = gs_telem_path 
        self.gs_video_path = gs_video_path
        self.gs_image_path = gs_image_path

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

        with open(self.obcCommandPath) as f:
            file = f.read().splitlines()
        print(file[0])
        return
        line = file[0]

        #probably not need to send error when multiple commands because we read the newest command instead of throwing error

        if int(line[0]) == self.currCmdNum: #this means no new command
            return None

        #if new command found, update currCmdNum and return a dictionary of command
        self.currCmdNum = int(line[0])

        lin = line.split()
        
        return {"mode" : lin[1],
        "command" : lin[2],
        "dist" : float(lin[3]),
        "LOI" : lin[4].split(',')}

    def writeTelemetry(self,gpsCoor): # -> bool:
        """
        write telemetry to telemetry file

        input:
            toWrite: telemetry to write to file (FORMAT TBD)
        """

        with open(self.obcTelemPath, 'a') as f:
            f.write('\n'+str(self.checkConnection())+' '+gpsCoor)

        self.syncTelem()
        

    def syncTelem(self,):

        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcTelemPath+" "+self.gs_telem_path)

    def syncVideo(self,):

        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcVideoPath+" "+self.gs_video_path)

    def syncImage(self,):

        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcImagePath+" "+self.gs_image_path)


    def checkConnection(self,):
        if 0 == os.system('ping '+self.gs_ip+' -c 3 -W 5'):
            return 1
        else:
            return 0


comm = RoverComms("commandTest.txt","teleTest.txt",'0','0','0','129.0.0.1','0','0','0')
#print(comm.isNewCommand())
comm.writeTelemetry('102.123124,103.241214')
print(comm.readCommand())
