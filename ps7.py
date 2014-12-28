# 6.00x Problem Set 7: Simulating robots

import math
import random

import ps7_visualize
import pylab

# For Python 2.7:
from ps7_verify_movement27 import testRobotMovement

# If you get a "Bad magic number" ImportError, comment out what's above and
# uncomment this line (for Python 2.6):
# from ps7_verify_movement26 import testRobotMovement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleanTiles = []#store a list/directory of clean/dirty tiles?
        
##        self.dirtyTiles = [] # might not actually need to store dirtyTiles!! ha ha!
##        e = 0
##        while e < width:
##            f = 0
##            while f < height:
##                self.dirtyTiles.append([e, f])
##                f += 1
##            e += 1
        
        
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        # if we work with flats as po's x & y co-ordinates, i think we simply need to turn them into ints
        if not [int(pos.getX()), int(pos.getY())] in self.cleanTiles:
            self.cleanTiles.append([int(pos.getX()), int(pos.getY())])
                
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return [m, n] in self.cleanTiles
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
    
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanTiles)
    
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        # IS IT GOING TO BE A PROBLEM THAT ALL THIS POSITION IS IN INTEGERS, NOT FLOATS?? WHAT IS ALTERNATIVE?
##        x = random.randint(0, self.width - 1)
##        y = random.randint(0, self.height - 1)
##        return Position(x, y)
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        if 0 <= x < self.width and 0 <= y < self.height:
            return Position(x, y)
        else: return self.getRandomPosition()
    
    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return pos.getX() < self.width and pos.getY() < self.height and pos.getX() >= 0 and pos.getY() >= 0


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.position)
        self.direction = random.uniform(0, 360) # random number between 0 and 360
        if self.direction == 360:
            self.direction = 0
       
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
            
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction
    
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position
        
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction
        
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.position.getNewPosition(self.direction, self.speed)
        #check if newPos is in the room
        if self.room.isPositionInRoom(newPos):
            self.setRobotPosition(newPos)
        #else give new direction and don't move
        else:
            newDirection = random.uniform(0, 360) # random number between 0 and 360
            if newDirection == 360:
                newDirection = 0
            self.setRobotDirection(newDirection)
        self.room.cleanTileAtPosition(self.getRobotPosition())
        
# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 3
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    trialResults = []
    for e in range(num_trials):
        print 'beginning trial', e
        print 'setting up dirty room'
        room = RectangularRoom(width, height)# set up the room
        print 'initialising timeCounter & robot list'
        timeCounter = 0
        listOfRobots = []
        for i in range(num_robots):
            listOfRobots.append(robot_type(room, speed))
            print listOfRobots
        while True:
            for i in listOfRobots:
                print'updating position of robot', i, '& cleaning!'
                i.updatePositionAndClean()  # or would it work to iterate over range of len listOfRobots, then call listOfRobots[i]??
            print 'incrementing time count'
            timeCounter += 1
            print 'checking how clean we are'
            print float(room.getNumCleanedTiles()), 'cleaned tiles'
            print 'min coverage:', min_coverage
            cleanliness = float(room.getNumCleanedTiles()) / float(room.getNumTiles())
            print 'cleanliness is now at:', cleanliness
            if cleanliness >= min_coverage:
                print 'reached target cleanliness! Terminating trial'
                trialResults.append(timeCounter)
                break
    return float(sum(trialResults)/len(trialResults))

##    trialResults = []
##    for e in range(num_trials):
##        anim = ps7_visualize.RobotVisualization(num_robots, width, height)
##        room = RectangularRoom(width, height)   # set up the room
##        timeCounter = 0
##        robots = []
##        for i in range(num_robots):
##            robots.append(robot_type(room, speed))
##        while True:
##            anim.update(room, robots)
##            for i in robots:          # call updtePsn and count on each robot
##                i.updatePositionAndClean()  # or would it work to iterate over range of len listOfRobots, then call listOfRobots[i]??
##            timeCounter += 1
##            if min_coverage <= float(room.getNumCleanedTiles()) / float(room.getNumTiles()):
##                trialResults.append(timeCounter)
##                anim.done()
##                break
##    return float(sum(trialResults)/len(trialResults))
##        
        
    # for one robot:
##            make the robot, passing in a RectangularRoom class instance, and a speed (1.0 at first)
##            call the updatePositionAndClean method of that robot
##            count the number of times said method is called
##            check the number of tiles cleaned (i.e. length of room.cleanTiles) against the number of tiles (i.e. room.getNumTiles)
##                this will need to check that min_coverage > (len(room.cleanTiles) / room.getNumTiles())
    # multiple robots will need to update shared counter for times that updatePositionAndClean is called
##        as well as updating the cleanTiles directory (already built in)

    # return mean time-steps needed to clean a specified fraction of a room
    # this is equivalent to the number of times that the program calls the updatePositionAndClean method of the StandardRobot class

# === Problem 4
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.position.getNewPosition(self.direction, self.speed)
        print 'allocated new position'
        #check if newPos is in the room
        if self.room.isPositionInRoom(newPos):
            print 'new position is in room'
            self.setRobotPosition(newPos)
            print 'moved to new position'
            newDirection = random.uniform(0, 360) # random number between 0 and 360
            print 'calculating new direction'
            if newDirection == 360:
                newDirection = 0
            print 'implementing new direction'
            self.setRobotDirection(newDirection)
        else:
            print 'now cleaning tile.'    
        self.room.cleanTileAtPosition(self.getRobotPosition())

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        print 'stuck'
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
        print 'still stuck'
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 5
#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
