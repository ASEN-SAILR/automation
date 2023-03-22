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

        self.obc_ip = '10.203.178.120'

        # ground station vars
        self.gs_ssh_password = gs_ssh_password #'asen4018'
        self.gs_ip = gs_ip #'192.168.56.102'

        gs_str_stem = "ground-station@"+gs_ip+":"
        self.gs_telem_path = gs_str_stem + gs_telem_path
        self.gs_video_path = gs_str_stem + gs_video_path
        self.gs_image_path = gs_str_stem + gs_image_path

        self.current_cmd_num = -1
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
        return the lastest command in the file
        if there is no new command return an empty dictionary
        """

        with open(self.obcCommandPath) as f:
            file = f.read().splitlines()
        
        command_dict = {}

        try:
            lastest_command = file[-1].split(', ')
            #print(lastest_command)
            if self.current_cmd_num == lastest_command[0]:
                return command_dict
            if int(lastest_command[0]) != self.current_cmd_num:
                if len(lastest_command) == 3 and (lastest_command[1] == 'start' or lastest_command[1] == 'stop'):
                    command_dict.update({'commandType':'startStop', 'command':lastest_command[1]})
                    self.current_cmd_num = lastest_command[0]
                elif len(lastest_command) == 3 and (lastest_command[1] == 'manual' or lastest_command[1] == 'autonomous'):
                    command_dict.update({'commandType':'changeMode', 'command':lastest_command[1]})
                    self.current_cmd_num = lastest_command[0]
                elif len(lastest_command) == 5:
                    command_dict.update({'commandType':lastest_command[1], 'manualType':lastest_command[2], 'command':float(lastest_command[3])})
                    self.current_cmd_num = lastest_command[0]
                elif len(lastest_command) == 6:
                    command_dict.update({'commandType':lastest_command[1], 'LOI':[float(lastest_command[3]),float(lastest_command[4])]})
                    self.current_cmd_num = lastest_command[0]
                else:
                    None

        except:
            None
            # print("command file empty")
        
    
        return command_dict

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
        print("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcTelemPath+" "+self.gs_telem_path)
        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcTelemPath+" "+self.gs_telem_path)

    def syncVideo(self,):
        print("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcVideoPath+" "+self.gs_video_path)
        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcVideoPath+" "+self.gs_video_path)

    def syncImage(self,):
        print("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcImagePath+" "+self.gs_image_path)
        os.system("sshpass -p '"+ self.gs_ssh_password+"' rsync -ave ssh "+self.obcImagePath+" "+self.gs_image_path)


    def checkConnection(self,):
        if 0 == os.system('ping '+self.gs_ip+' -c 3 -W 1'):
            return 1
        else:
            return 0

    def startLive(self):
        self.process = Process(target=self.liveVideoServer)
        self.process.start()

    def stopTele(self):
        if self.process.is_alive():
            self.process.terminate()

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



