import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2

def radialToCart(ang:np.ndarray, dist:np.ndarray, type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    x = np.multiply(np.cos(ang),dist)
    y = np.multiply(np.sin(ang),dist)
    return x, y

def getObjectGrid(x, y, threshold:int=5, x_lim:tuple[float]=(0,3), y_lim:tuple[float]=(-3,3), resolution:float=0.1, plot=True):
    x_mag = x_lim[1]-x_lim[0]
    y_mag = y_lim[1]-y_lim[0]
 
    # the following array is a 1D array of bools. True means associated point is within x_lim and y_lim.
    truth_vals = np.all(np.vstack((x>x_lim[0], x<x_lim[1], y>y_lim[0], y<y_lim[1])),0)
    
    # points that are false in `truth_vals` are removed
    x_rem = x[truth_vals]
    y_rem = y[truth_vals]
    
    # create 2d array for objects 
    grid = np.zeros([int(x_mag//resolution),int(y_mag//resolution)])

    # bins the x and y values into integer bins
    x_binned = [val//resolution for val in x_rem]
    y_binned = [val//resolution for val in y_rem]

    # this returns unique points and their counts
    vals,counts = np.unique(list(zip(x_binned,y_binned)),return_counts=True,axis=0)

    # objects are points where there are more hits than the threshold 
    objects = np.array(vals[counts>threshold], dtype=np.int_)
 
    # fills the grid with ones where there is an "object". 
    # Looks complicated because `objects` contains negative numbers which cannot be indices
    grid[objects[:,0]-(int(x_lim[0]/resolution)),objects[:,1]-(int(y_lim[0]/resolution))] = 1

    # collapses grid into a 1d array
    one_d_arr = np.any(grid,axis=0)

    if plot:
        #plot
        fig, ax = plt.subplots(figsize=(8,8))
        plt.scatter(x,y, 5, label='data')

        #rectangle
        rect = patches.Rectangle((x_lim[0], y_lim[0]), x_lim[1]-x_lim[0],y_lim[1]-y_lim[0], label='Decision Area', linewidth=1, edgecolor='none', facecolor='green', alpha=.2)
        ax.add_patch(rect)

        plt.scatter(0, 0, 25, label='LiDAR Sensor')
        ax.set_title('Coordinates as measured by LiDar before processing', fontsize=18)
        ax.set_xlabel('x [m]', fontsize=14)
        ax.set_ylabel('y [m]', fontsize=14)
        ax.legend()
        ax.axes.set_aspect('equal')
        ax.grid()

        #plot
        fig, ax = plt.subplots(figsize=(8,8))
        plt.scatter(np.multiply(objects[:,0],resolution),np.multiply(objects[:,1],resolution));
        ax.set_title('Coordinates as measured by LiDar after processing, th=100', fontsize=18)
        ax.set_xlabel('xn [m]', fontsize=14)
        ax.set_ylabel('yn [m]', fontsize=14)
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        ax.axes.set_aspect('equal')
        ax.grid()

        displayImg(grid) 

        displayImg(np.expand_dims(np.flip(one_d_arr ),axis=1))
     

    return one_d_arr

#flip image to match plots
def displayImg(img):
    fig, ax = plt.subplots(figsize=(8,8))
    img = np.flip(np.array(img),1) #flip along 1st axis 
    img = img.T #transpose 
    plt.imshow(img) # display


all_scans = np.load("new_data.npy")
# all_scans = [(0,5,1010),(0,10,1507),(0,10,1507),(0,100,1530)]

# convert to x,y
MAX_DIST = 2 #m
X_LIMITS = (0,3)
Y_LIMITS = (-3,3)
THRESHOLD = 100
RESOLUTION = 0.05

qual,ang,dist = zip(*all_scans)

#zip returns tuples, we need lists
ang = ([val for val in ang])
dist = np.array([val/1000 for val in dist])

x,y = radialToCart(ang,dist,type='deg')

obj_arr = getObjectGrid(x, y, x_lim=X_LIMITS, y_lim=Y_LIMITS, threshold=THRESHOLD, resolution=RESOLUTION)


plt.show()