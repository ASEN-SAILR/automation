import numpy as np

def radialToCart(ang:np.ndarray, dist:np.ndarray, type = "rad"):
    if type == "deg":
        ang = [val*3.1415/180 for val in ang]
    x = np.multiply(np.cos(ang),dist)
    y = np.multiply(np.sin(ang),dist)
    return x, y

def cartToRadial(x:np.ndarray, y:np.ndarray, type = "rad"):
    dist = np.sqrt(x**2+y**2)
    ang = np.arctan2(y,x)
    return ang,dist

if __name__ == "__main__":
    LOAD_PATH = r"lidar\data\lidar_mulch_0_2022_11_16_mod.npy"
    OUT_PATH = r"lidar\data\lidar_mulch_CDR_2022_11_16.npy"
    var = np.load(LOAD_PATH)
    
    qual,ang,dist = zip(*var)

    qual = np.array([val for val in qual])
    ang = np.array([val*3.14/180 for val in ang])
    dist = np.array([val for val in dist])

    x,y = radialToCart(ang,dist,type='rad')

    truth_vals = np.all(np.vstack((x>-500, x<2500, y>-500, y<1000)),0)
    x_rem = x[truth_vals]
    y_rem = y[truth_vals]
    qual_rem = qual[truth_vals]
    ang,dist = cartToRadial(x_rem,y_rem,"rad")

    out = np.column_stack((qual_rem,ang*180/3.14,dist))

    
    # print(out)
    np.save(OUT_PATH,out)



