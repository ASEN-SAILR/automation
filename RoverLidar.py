# Luke
class RoverLidar:
    def __init__(self) -> None:
        # member vars

        # initialize stuff

        pass

    def getMap(self):
        """
        returns a 2d array of "objects"
        """
        pass

    def getObstacles(self):
        """
        Inputs 
            map: 2d bool array, (0 -> empty, 1 -> object)
        returns
            color: color of zone where there are obstacles
            obstacles: coordiantes of obstacles located in map[(x1,y1),(x2,y2),...,(xn,yn)]  
        """
        color = None
        obstacles = None
        return color,obstacles