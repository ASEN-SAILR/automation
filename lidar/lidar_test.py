import os
from math import floor
from adafruit_rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
#https://github.com/SkoltechRobotics/rplidar

def radialToCart(ang,dist,type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    x = np.multiply(np.cos(ang),dist)
    y = np.multiply(np.sin(ang),dist)
    return x, y

# Setup the RPLidar
PORT_NAME = 'COM9'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# used to scale data to fit on the screen
max_distance = 0

def process_data(data):
    print(data)

scan_data = np.array([0]*360)
all_scans = [];
try:
#    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            print(angle,distance)
            # scan_data[min([359, floor(angle)])] = distance
            all_scans+=scan
        # process_data(scan_data)
        

except KeyboardInterrupt:
    print("Didn't get data, maybe LiDar is disconnected")
    np.save("new_data.npy",np.array(all_scans))
    pass

print('scan',all_scans)

# convert to x,y
degs = [i for i in range(360)]
qual,ang,dist = zip(*all_scans)
print('ang',ang)
print('dist',dist)
x,y = radialToCart(ang,dist,type='deg')

print('x',x)
print('y',y)
#plot
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(x,y);
ax.set_title('Coordinates as messured by LiDar', fontsize=18)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
plt.show()

#stop (disconnects, but doesn't turn it off, idk why)
# lidar.stop_motor()
lidar.stop()
lidar.disconnect()
print('Stopping.')
