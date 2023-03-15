from RoverComms import RoverComms

# # onboard computer comms vars
obcVideoPath = "~/SeniorProjects/automation/videos/"
obcCommandPath = "commandTest.txt"
obcTelemPath = "telemetry.txt"
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

print(comms.readCommand())