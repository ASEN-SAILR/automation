import numpy as np
import matplotlib.pyplot as plt

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
    x = np.where(truth_vals, x, np.nan)
    y = np.where(truth_vals, y, np.nan)
    
    grid = np.zeros([int(x_mag//resolution),int(y_mag//resolution)])

    print('x before',x)
    x_dig = [val//resolution for val in x]
    y_dig = [val//resolution for val in y]
    print('x_bins',x_dig)
    print('y_bins',y_dig)

    



# all_scans = np.load("new_data.npy")
all_scans = [(0,5,1010),(0,10,1507),(0,100,1530)]

# convert to x,y
MAX_DIST = 2 #m
degs = [i for i in range(360)]
qual,ang,dist = zip(*all_scans)
ang = np.array([val for val in ang])
dist = np.array([val/1000 for val in dist])

ang_n = np.where(dist<MAX_DIST,ang,np.nan)
dist_n = np.where(dist<MAX_DIST,dist,np.nan)
print('cond', dist<MAX_DIST)

x,y = radialToCart(ang_n,dist_n,type='deg')

getObjectGrid(x,y)

#plot
fig, ax = plt.subplots(figsize=(8,8),subplot_kw={'projection': 'polar'})
plt.scatter(np.multiply(ang_n,3.14/180),dist_n);
ax.set_title('Coordinates as measured by LiDar', fontsize=18)
# ax.set_xlabel('x', fontsize=14)
# ax.set_ylabel('y', fontsize=14)
plt.show()