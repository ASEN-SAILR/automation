import os
from math import floor
from adafruit_rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
import time
#https://github.com/SkoltechRobotics/rplidar

NAME = "TRR_scan_20230221_trash_"

def radialToCart(ang,dist,type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    x = np.multiply(np.cos(ang),dist)
    y = np.multiply(np.sin(ang),dist)
    return x, y

# Setup the RPLidar
PORT_NAME = 'COM9'
SCAN_TIME = 2
lidar = RPLidar(None, PORT_NAME, timeout=3)
# lidar.reset()
time.sleep(1)



# used to scale data to fit on the screen
max_distance = 0

def process_data(data):
    print(data)

scan_time = 1

scan_data = np.array([0]*360)
all_scans = list([])
try:
#    print(lidar.get_info())
    count = 0
    while count<15:
        count+=1
        start_time = time.time()
        scan = []
        for temp_scan in lidar.iter_scans():
            if(start_time+scan_time<time.time()):
                break
            # print(temp_scan)
        
            for (_, angle, distance) in temp_scan:
                pass
            scan.extend(temp_scan)
            
        print(f"scan {count}")
        np.save(os.path.join(r"C:\\Users\\luker\\Documents\\repos\\SAILR\\automation\\lidar\\data",f"{NAME}{count}.npy"),np.array(scan))
        all_scans.append(scan)


except KeyboardInterrupt:
    print("Didn't get data, maybe LiDar is disconnected")
    
    pass

# print('scan',all_scans)

# convert to x,y
for i,scan in enumerate(all_scans):
    degs = [i for i in range(360)]
    qual,ang,dist = zip(*scan)

    x,y = radialToCart(ang,dist,type='deg')

    # print('x',x)
    # print('y',y)
    #plot
    fig, ax = plt.subplots(figsize=(8,8))
    plt.scatter(x,y);
    ax.set_title(f"{NAME}{i}", fontsize=18)
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.grid()
    ax.set_aspect('equal')
    plt.savefig(os.path.join(r"C:\\Users\\luker\Documents\\repos\\SAILR\\automation\\lidar\\images",f"{NAME}{i}.jpg"),dpi=200)
    plt.close(fig)


#stop (disconnects, but doesn't turn it off, idk why)
# lidar.stop_motor()
lidar.stop()
lidar.disconnect()
print('Stopping.')
