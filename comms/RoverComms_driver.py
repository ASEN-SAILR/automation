import sys
sys.path.append("../.")
sys.path.append(".")
import time

from RoverComms import RoverComms

if __name__ == "__main__":
    my_str = 'lol'
    comms = RoverComms(obcCommandPath="comms\\excommands.txt",
                       obcTelemPath=my_str,
                       obcVideoPath=my_str,
                       obcImagePath=my_str,
                       gs_ssh_password=my_str,
                       gs_ip=my_str,
                       gs_telem_path=my_str,
                       gs_video_path=my_str,
                       gs_image_path=my_str)
    
    while True:
        print(comms.readCommand())
        time.sleep(1)