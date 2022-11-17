import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from copy import copy,deepcopy
import cv2

PLOT_FONT = {"fontname":"Comic Sans"}

def radialToCart(ang:np.ndarray, dist:np.ndarray, type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    # x = np.multiply(np.cos(ang),dist)
    # y = np.multiply(np.sin(ang),dist)
    x = np.cos(ang)*dist
    y = np.sin(ang)*dist
    return x, y

def getObjectGrid(x, y, threshold:int=5, x_lim:tuple[float]=(0,3), y_lim:tuple[float]=(-3,3), red_lim = (0,0), resolution:float=0.1, plot=True):
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
        #unproccessed plot
        fig, ax = plt.subplots(figsize=(8,8))

        #rectangle

        #orange rectangles
        rect_oran_1 = patches.Rectangle((x_lim[0], red_lim[1]), x_lim[1]-x_lim[0],y_lim[1]-red_lim[1], label='Orange Zone', linewidth=1, edgecolor='none', facecolor='orange', alpha=.2)
        rect_orang_2 = patches.Rectangle((x_lim[0], y_lim[0]), x_lim[1]-x_lim[0],red_lim[1]-y_lim[0], linewidth=1, edgecolor='none', facecolor='orange', alpha=.2)
        rect_red = patches.Rectangle((x_lim[0], red_lim[0]), x_lim[1]-x_lim[0],red_lim[1]-red_lim[0], label="Red Zone", linewidth=1, edgecolor='none', facecolor='red', alpha=.2)
        
        #add orange and red zones
        ax.add_patch(rect_oran_1)
        ax.add_patch(rect_orang_2)
        ax.add_patch(rect_red)

        plt.scatter(x,y, 5, label='data')
        plt.scatter(0, 0, 75, label='LiDAR Sensor',color='green')

        ax.set_title('Coordinates as measured by LiDAR before processing', fontsize=18, **PLOT_FONT)
        ax.set_xlabel('x [m]', fontsize=14)
        ax.set_ylabel('y [m]', fontsize=14)
        ax.legend(loc="upper right")
        ax.axes.set_aspect('equal')
        ax.grid()

        #processed data plot
        fig, ax = plt.subplots(figsize=(8,8))

        rect_oran_1 = patches.Rectangle((x_lim[0], red_lim[1]), x_lim[1]-x_lim[0],y_lim[1]-red_lim[0], label='Orange ', linewidth=1, edgecolor='none', facecolor='orange', alpha=.2)
        rect_orang_2 = patches.Rectangle((x_lim[0], y_lim[0]), x_lim[1]-x_lim[0],red_lim[1]-y_lim[0], linewidth=1, edgecolor='none', facecolor='orange', alpha=.2)
        rect_red = patches.Rectangle((x_lim[0], red_lim[0]), x_lim[1]-x_lim[0],red_lim[1]-red_lim[0], linewidth=1, edgecolor='none', facecolor='red', alpha=.2)
        
        #add orange and red zones
        ax.add_patch(rect_oran_1)
        ax.add_patch(copy(rect_orang_2))
        ax.add_patch(copy(rect_red))

        plt.scatter(np.multiply(objects[:,0],resolution),np.multiply(objects[:,1],resolution), label="Processed Data")
        plt.scatter(0, 0, 75, label='LiDAR Sensor',color="green")
        # ax.set_title(F"LiDAR Data After Processing, th={threshold}", fontsize=18)
        
        ax.set_title(F"LiDAR Data After Processing", fontsize=18)
        ax.set_xlabel('x [m]', fontsize=14)
        ax.set_ylabel('y [m]', fontsize=14)
        plt.xlim(x_lim)
        plt.ylim(y_lim)
        ax.legend(loc="upper right")
        ax.axes.set_aspect('equal')
        ax.grid()

        fig,ax = displayImg(grid) 
        # ax.xlabel

        fig,ax = displayImg(np.expand_dims(np.flip(one_d_arr ),axis=1))
     

    return one_d_arr

#flip image to match plots
def displayImg(img):
    fig, ax = plt.subplots(figsize=(8,8))
    img = np.flip(np.array(img),1) #flip along 1st axis 
    img = img.T #transpose 
    plt.imshow(img) # display
    return fig,ax


# all_scans = [(0,5,1010),(0,10,1507),(0,10,1507),(0,100,1530)]

if __name__ == "__main__":
    # convert to x,y
    MAX_DIST = 2 #m
    X_LIMITS = (0,3.5)
    Y_LIMITS = (-.6,.6)
    THRESHOLD = 10
    RESOLUTION = 0.05
    RED_ZONE_LIMITS = (-0.3,0.3)
    FILE_PATH= r"lidar\data\lidar_mulch_CDR_2022_11_16.npy"

    all_scans = np.load(FILE_PATH)

    print(all_scans)
    qual,ang,dist = zip(*all_scans)

    #zip returns tuples, we need lists
    ang = ([val for val in ang])
    dist = np.array([val/1000 for val in dist])

    x,y = radialToCart(ang,dist,type='deg')

    obj_arr = getObjectGrid(x, y, x_lim=X_LIMITS, y_lim=Y_LIMITS, red_lim=RED_ZONE_LIMITS, threshold=THRESHOLD, resolution=RESOLUTION)


    plt.show()