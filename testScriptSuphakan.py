
#import RoverMove
from RoverComms import RoverComms
from RoverGPS import RoverGPS
#import RoverLidar
from RoverCamera import RoverCamera
#import RoverUART
import logging
import time
from multiprocessing import Process

def main():
    # start reading commands from commands log
    # leaving these in for testing on automation end but should be taken out
    commands_path = r"/commands.txt"
    telemetry_path = r"telemetry.txt"
    # # onboard computer comms vars
    obcVideoPath = "~/SeniorProjects/automation/videos/"
    obcCommandPath = commands_path
    obcTelemPath = telemetry_path
    obcImagePath = "~/SeniorProjects/automation/images/"
    #currCmdNum = 0 #not needed, automatically defined in RoverComms
    # ground station comms vars
    gs_ssh_password = "asen-sailr"
    gs_ip = "192.168.1.3"
    gs_home_path = "~/comms-gs/"
    gs_telem_path = gs_home_path+"telemetry.txt"
    gs_video_path = gs_home_path+"videos"
    gs_image_path = gs_home_path+"images"
    #start comms
    comms = RoverComms(obcCommandPath,obcTelemPath,obcVideoPath,obcImagePath,gs_ssh_password,gs_ip,gs_telem_path,gs_video_path,gs_image_path)


    # start video recording (class)
    camPort = [0,4,8]
    vidLength = 15 #unit is second
    photoPath = obcImagePath
    photoResolution = [640,360] #format: tuple (480,480)
    videoPath = obcVideoPath
    fps = 30 
    videoResolution =[640,360] #format: tuple (480,480)
    cam = RoverCamera(comms,camPort,vidLength,photoPath,photoResolution,videoPath,fps,videoResolution) #need comms so that we can send video after recording
    #cam.startRecording() 

    # start uart comms with Teensy
    teensy_port = r"/dev/tty/1"
    #uart = RoverUART(teensy_port,baud=115200) 

    # start lidar
    lidar_port = r"/dev/tty/2"
    #lidar = RoverLidar(lidar_port) # more params?

    # start gps 
    gps_port = r"/dev/tty/2"
    # gps = RoverGPS(comms,gps_port) # more params?

    # start move
    #move = RoverMove(gps,lidar)

    if True:
       # cam.record()
       # print("Record and sync video done.")
        cam.take360()
        print("Take 360 and sync done.")
    if False: #True to test GPS reading background process
        gps.startTele()
        t = time.time()
        while time.time()-t<1:pass
        gps.stopTele()
    if False: #True to test distanceToTarget and bearingToTarget from txt file
        LOI = [50,50]
        currHeading = 0
        print('distance=',gps.distanceToTarget(LOI),'m')
        print('angle=',gps.angleToTarget(LOI,currHeading),'deg')


if __name__ == "__main__":
    main()
