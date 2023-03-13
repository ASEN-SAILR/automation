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
import cv2
import socket
import pickle
import struct

class RoverComms:
    def __init__(self,obcCommandPath:str,obcTelemPath:str,obcVideoPath:str,obcImagePath:str,gs_ssh_password:str,gs_ip:str,gs_telem_path:str,gs_video_path:str,gs_image_path:str):
        # onboard computer vars
        self.obcCommandPath = obcCommandPath
        self.obcTelemPath = obcTelemPath
        self.obcVideoPath = obcVideoPath
        self.obcImagePath = obcImagePath
        self.currCmdNum = 0

        self.obc_ip = '10.203.178.120'

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

    def writeAndSendTelemetry(self,gpsCoor:str): # -> bool:
        """
        write telemetry to telemetry file

        input:
            toWrite: telemetry to write to file (FORMAT TBD)
        """

        with open(self.obcTelemPath, 'a') as f:
            f.write(gpsCoor+'\n')

        self.syncTelem()
        

    def syncTelem(self,):

        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcTelemPath+" "+self.gs_telem_path)

    def syncVideo(self,):

        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcVideoPath+" "+self.gs_video_path)

    def syncImage(self,):

        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcImagePath+" "+self.gs_image_path)


    def checkConnection(self,):
        if 0 == os.system('ping '+self.gs_ip+' -c 3 -W 1'):
            return 1
        else:
            return 0

    def liveVideoServer(self,):

        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        # host_ip = socket.gethostbyname(host_name)
        host_ip = self.obc_ip
        print('Host IP:', host_ip)
        port = 9999
        socket_address = (host_ip, port)

        # Bind the socket to a public host and a port
        server_socket.bind(socket_address)

        # Listen for incoming connections
        server_socket.listen(5)

        print('Waiting for client...')
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print('Client connected:', client_address)

            # Open the webcam
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FPS,30)
            # Set the video dimensions
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))

            # Send the video dimensions to the client
            client_socket.send(struct.pack("I", frame_width))
            client_socket.send(struct.pack("I", frame_height))

            # Start streaming the video
            while True:
                # Read a frame from the webcam
                ret, frame = cap.read()

                # Convert the frame to a byte string
                data = pickle.dumps(frame)

                # Send the frame size to the client
                client_socket.send(struct.pack("I", len(data)))

                # Send the frame to the client
                client_socket.send(data)



