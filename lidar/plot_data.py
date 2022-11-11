import numpy as np
import matplotlib.pyplot as plt
import cv2

def radialToCart(ang,dist,type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    x = np.multiply(np.cos(ang),dist)
    y = np.multiply(np.sin(ang),dist)
    return x, y

def getObjectGrid(x, y, threshold:int=5, x_lim:tuple[float]=(0,3), y_lim:tuple[float]=(-3,3), resolution:float=0.1):
    x_mag = x_lim[1]-x_lim[0]
    y_mag = y_lim[1]-y_lim[0]
 
    #the following array is a 1D array of bools. True means associated point is within x_lim and y_lim.
    truth_vals = np.all(np.vstack((x>x_lim[0], x<x_lim[1], y>y_lim[0], y<y_lim[1])),0)
    
    #points that are false in `truth_vals` are removed
    # x = np.where(truth_vals, x, None)
    # y = np.where(truth_vals, y, None)
    x = x[truth_vals]
    y = y[truth_vals]
    
    grid = np.zeros([int(x_mag//resolution),int(y_mag//resolution)])

    print('x before',x)
    x_dig = [val//resolution for val in x]
    y_dig = [val//resolution for val in y]
    print('x_bins',x_dig)
    print('y_bins',y_dig)

    vals,counts = np.unique(list(zip(x_dig,y_dig)),return_counts=True,axis=0)

    objects = vals[counts>threshold]
    print('objects',objects)

    #this for loop is not working as intended. The indexing is incorrect. Can get negative indexes
    for i,val in enumerate(vals):
        if counts[i]>threshold:
            print('val',val)
            grid[int(val[0])][int(val[1])] = 1 # may need to flip axes of grid

    # displayImg(grid) #this also does not work because above is not working 

    return np.multiply(objects[:,0],resolution),np.multiply(objects[:,1],resolution)
    # return np.multiply(x_dig,resolution),np.multiply(y_dig,resolution)

def displayImg(img):
    plt.imshow(img)


all_scans = np.load("new_data.npy")
# all_scans = [(0,5,1010),(0,10,1507),(0,10,1507),(0,100,1530)]

# convert to x,y
MAX_DIST = 2 #m
degs = [i for i in range(360)]
qual,ang,dist = zip(*all_scans)
ang = np.array([val for val in ang])
dist = np.array([val/1000 for val in dist])

# ang_n = np.where(dist<MAX_DIST,ang,np.nan)
# dist_n = np.where(dist<MAX_DIST,dist,np.nan)
# print('cond', dist<MAX_DIST)

x,y = radialToCart(ang,dist,type='deg')

xn,yn = getObjectGrid(x,y,threshold=500,resolution=0.05)


#plot
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(x,y);
ax.set_title('Coordinates as measured by LiDar before processing', fontsize=18)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
ax.grid()

#plot
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(xn,yn);
ax.set_title('Coordinates as measured by LiDar after processing', fontsize=18)
ax.set_xlabel('xn', fontsize=14)
ax.set_ylabel('yn', fontsize=14)
ax.grid()
plt.show()