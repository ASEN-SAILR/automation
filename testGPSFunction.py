import math


currCoor = [40.0097551,-105.24409899999999] 
tarCoor = [40.0091687,-105.243807]
#tarCoor = [40.01,-105.24409899999999]

currCoor = [40.00924734,-105.24391305] 
tarCoor = [40.0093664,-105.2439658]



def distanceToTarget(currCoor:list,tarCoor:list): # -> float: 
        """
        input: currCoor, tarCoor = [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: distance to target in meter (float)
        """
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

def bearingToTarget(currCoor:list,tarCoor:list): # -> float:
        """
        input: 
            currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: 
            bearing in deg from north, ie. 89 (float)
        """
        #input: currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        #output: bearing in deg from north, ie. 89 (float)
        
        lat1, lon1 = currCoor
        lat2, lon2 = tarCoor
        #print(lat1,lon1)
        deg2rad = math.pi/180
        lat1 = lat1*deg2rad
        lon1 = lon1*deg2rad
        lat2 = lat2*deg2rad
        lon2 = lon2*deg2rad
        
        a = math.sin(lon2-lon1)*math.cos(lat2)
        b = math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)
        bearing = math.atan2(a,b) #in rad
        return bearing*180/math.pi
        
print(distanceToTarget(currCoor,tarCoor)) #69.7863
print(bearingToTarget(currCoor,tarCoor))#159.1229