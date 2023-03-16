import sys
sys.append("../.")
sys.append(".")

from RoverComms import RoverComms

if __name__ == "__main__":
    my_str = 'lol'
    comms = RoverComms(obcCommandPath="test_commands.txt",
                       obcTelemPath=my_str,
                       obcVideoPath=my_str,
                       obcImagePath=my_str,
                       gs_ssh_password=my_str,
                       gs_ip=my_str,
                       gs_telem_path=my_str,
                       gs_video_path=my_str,
                       gs_image_path=my_str)