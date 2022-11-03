import math


def bearingToTarget(currCoor,tarCoor): 
    #input: currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231N,-34.204] (object of floats)
    #output: bearing in deg from north, ie. 89 (float)
    
    lat1, lon1 = currCoor
    lat2, lon2 = tarCoor

    deg2rad = math.pi/180
    lat1 = lat1*deg2rad
    lon1 = lon1*deg2rad
    lat2 = lat2*deg2rad
    lon2 = lon2*deg2rad
    
    a = math.sin(lon2-lon1)*math.cos(lat2)
    b = math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
    bearing = math.atan2(a,b) #in rad
    return bearing*180/math.pi #convert to deg

def distanceToTarget(currCoor,tarCoor): 
    #input: currCoor, tarCoor = [lat,lon], ie. [23.0231,-34.204] (object of floats)
    #output: distance to target in meter (float)

    lat1, lon1 = currCoor
    lat2, lon2 = tarCoor

    deg2rad = math.pi/180
    lat1 = lat1*deg2rad
    lon1 = lon1*deg2rad
    lat2 = lat2*deg2rad
    lon2 = lon2*deg2rad

    EarthRadiusMeter = 6371000
    
    #haversine formula
    a = (math.sin((lat2-lat1)/2.0))**2 + math.cos(lat1)*math.cos(lat2)*(math.sin((lon2-lon1)/2))**2
    c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    
    meter = EarthRadiusMeter * c
    return meter;

def angleToTarget(currHeading,currCoor,tarCoor):
    #input: currHeading = current heading to target from magnetometer in deg (float)
    #       currCoor, tarCoor = current and target coordinate [lat,lon], ie. ["23.0231N","34.204W"] (object of strings)
    #output: angle to target with respect to current heading in deg, positive mean to the right (float)
    return bearingToTarget(currCoor,tarCoor)-currHeading

def parseCoor(coor): 
    #input: lat and lon in format such as ["23.0231N","33.213W"] (string)
    #output: lat or lon in format such as [23.0231,-33.213] (for W and S) (float)
    #this function is probably not used because GPS device gives coordinates in desired format already(as in output)

    #extract lat, lon of current and target location 
    lat, lon = coor
    
    
    if (lat[-1] != "N") & (lat[-1] != "S"):
        print("Error: wrong latitude format.")
        return
    if (lon[-1] != "W") & (lat[-1] != "E"):
        print("Error: wrong longtitude format.")
        return
    
    try:
        if lat[-1] == "S":
            lat = -float(lat[:-1])
        else:
            lat = float(lat[:-1])
        if lon[-1] == "W":
            lon = -float(lon[:-1])
        else:
            lon = float(lon[:-1])
    except TypeError:
        print("Not a valid number.")
    
    lat = lat
    lon = lon
    
    return [lat,lon]

def getCoor():
    #get coordinate from GPS
    #parse GPS messege and output as coordinate [lat,lon], ie. [23.1241,-45.0921] (object of floats)
    return [23.1241,-45.0921]


#simulate main structure
tarCoor = [23.1242,-45.0929] #input from user
currCoor = getCoor() #read from GPS
currHeading = 10 #read from magnetometer, in deg


print("Angle to target:",angleToTarget(currHeading,currCoor,tarCoor)," degrees")
print("Distance to target:",distanceToTarget(currCoor,tarCoor)," meters")