# Suphakan
class RoverGPS:
    def __init__(self) -> None:
        #member vars

        #initialize stuff

        pass

    def bearingToTarget(currCoor,tarCoor) -> float:
        """
        input: 
            currCoor, tarCoor = set of coordinates [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: 
            bearing in deg from north, ie. 89 (float)
        """
        pass

    def distanceToTarget(currCoor,tarCoor) -> float: 
        """
        input: currCoor, tarCoor = [lat,lon], ie. [23.0231,-34.204] (object of floats)
        output: distance to target in meter (float)
        """
        pass

    def angleToTarget(currHeading,currCoor,tarCoor) -> float:
        """
        input: 
            currHeading = current heading to target from magnetometer in deg (float)
            currCoor, tarCoor = current and target coordinate [lat,lon], ie. [23.0231,-34.204] (object of strings)
        output: 
            angle to target with respect to current heading in deg, positive mean to the right (float)
        """
        pass

    def getCoor():
        pass