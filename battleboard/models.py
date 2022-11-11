from .CONSTS import HitActionState, ShipDirectionState

class BattlShipBoard(object):
    """ A BattlShipBoard Model for BattleShip Game
        Board consists of Ships, BoardMap and Dimension
        BoardMap actually holds the actual board ( 2D Array ) keeping the reference of ship in each co-ordinates
    """
    __ships = []

    def __init__(self, dimension, ships):
        self.initializeBoard(dimension)
        self.setShips(ships)

    # getter method for boardmap
    def getBoardMap(self):
        return self.__boardMap   

    # Initialize board that includes dimension and boardmap      
    def initializeBoard(self, dimension):
        # Set Board Dimension
        self.__dimension = dimension
        self.__boardMap = [[0 for i in range(self.__dimension[1])] for j in range(self.__dimension[0])]  

    # setter method of ships
    def setShips(self, ships):
        for ship in ships:
            self.setIndividualShip(ship)

    # getter method of ships
    def getShips(self):
        return self.__ships

    # getter method of ship by uuid
    def getShip(self, uuid):
        for ship in self.getShips():
            if ship.getShipId() == uuid:
                return ship

    # hit ship method for playing
    def hitShip(self, point):
        
        # check if point is valid and available then it is WATER state
        if self.isBoxAvailAndValid(point):
            return HitActionState.WATER_STATE
        # check if point is valid but not available then it could be HIT | WATER
        elif self.isBoxValid(point): 
            # get ship uuid from board mapping
            ship_uuid = self.getBoardMap()[point[0]][point[1]]
            
            # get ship from uuid
            ship = self.getShip(ship_uuid)
            
            # check if ship is not sinkable
            if ship.isSinkAble() == False:
                ship.hitComponent(point)

                if ship.isSinkAble():
                    return HitActionState.SINK_STATE
            
            return HitActionState.HIT_STATE
        else:
            raise "Exception Raised: Out of Bound Hit"

    # create individual ship from data point
    def setIndividualShip(self, ship):
        try:
            # set input vars    
            x = ship.get('x')
            y = ship.get('y')
            origin = (x, y)
            size = ship.get('size')
            direction = ship.get('direction')

            # get all points of ship in w.r.t the origin, size and direction
            all_points = BattleShip.getShipPoints( origin, size, direction)
                    
            # create ship if points and boardmap are set
            if len(all_points)>0 and len(self.__boardMap) >0:
                points_status = True
                for point in all_points:
                    points_status &= self.isBoxAvailAndValid(point)
                
                # create ship if all points(squares) are available
                if points_status:
                    shipObject = BattleShip(size, direction, origin, all_points, self.__boardMap)
                    self.__ships.append(shipObject)
                else:
                    raise ValueError("Exception Raised: Ship Overlapped or Out Of Bound")    

        except Exception as e:
            raise ValueError(e)                 

    # check board's square out of bound state
    def isBoxValid(self, point):
        return  ( 
                point[0] >= 0 and point[0] < self.__dimension[0]
                and point[1] >= 0 and point[1] < self.__dimension[1]
            )   
    # check board's square out of bound state and availability
    def isBoxAvailAndValid(self, point):
        if self.isBoxValid(point) and self.__boardMap[point[0]][point[1]] == 0:
            return True
        
        return False        

class BattleShip(object):
    """ A BattleShip Model for BattleShip Game
        This is an individual ship which will be used in the game. 
    """
    __components = []

    def __init__(self, size, direction, origin, points, map):
        from uuid import uuid4
        self.__direction = direction
        self.__size = size
        self.__origin = origin
        self.__uuid = uuid4()
        self.assignComponents(points, map)

    # create ship components and assign to board for points (squares)  
    def assignComponents(self, points, map):
        self.__components = []
        for point in points:
            # create ship component w.r.t poin
            shipComponent = BattleShipComponent(point)
            
            # update board map point with ship uuid
            map[point[0]][point[1]] = str(self.__uuid)
            self.__components.append(shipComponent)

    # static method ( class level ) to get ship points w.r.t to origin, size and direction
    @staticmethod
    def getShipPoints(origin, size, direction):
        
        # first index of tuple is x
        x = origin[0] 
        # second index of tuple is y
        y = origin[1]

        # create points for horitzontal state
        if direction == ShipDirectionState.HORIZONTAL_STATE:
            all_points = [(i,y) for i in range(x,x+size)]
        # create points for vertical state
        elif direction == ShipDirectionState.VERTICAL_STATE:
            all_points = [(x,i) for i in range(y,y+size)]
        else:
            raise "Invalid Direction"    

        return all_points    

    # getter method for ship uuid
    def getShipId(self):
        return str(self.__uuid)

    # method to check ship sink state
    # if any component of a ship is not hit then this gives false
    def isSinkAble(self):
        sink_status = True
        for item in self.__components:
            sink_status &= item.isHit()
        return sink_status
    
    # method to hit componenet of a ship
    # if component is placed on a point then it is set as HIT
    def hitComponent(self, point):
        for component in self.__components:
            if component.isPlacedAtPoint(point):
                component.setHit(True)
                break

class BattleShipComponent(object):
    """ A BattleShipComponent Model for BattleShip Game
        this component represent each square of a ship with its HITS status
    """
    
    def __init__(self, point) -> None:
        self.__point = point
        self.__isHit = False

    # method to check HIT state of a component
    def isHit(self):
        return self.__isHit

    # setter method for property __isHit
    def setHit(self, status):
        self.__isHit = status

    # getter method for property __point
    def getPoint(self):
        return self.__point
    
    # method to check component at a give point placed
    def isPlacedAtPoint(self, point):
        return ( self.__point[0] == point[0] and self.__point[1] == point[1] )     