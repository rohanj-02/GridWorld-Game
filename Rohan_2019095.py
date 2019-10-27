import os
import time
import random

class Point:
    """
    Defines a point in the 2-D space.
    Data Members:
        x: x-coordinate of the Point
        y: y-coordinate of the Point
    Member Functions:
    """

    def __init__(self, x, y):
        """
        Preconditions:
            x: an Integer
            y: an Integer
        """
        assert type(x) == int, "x should be an Integer"
        assert type(y) == int, "y should be an Integer"

        self.x = x
        self.y = y

    def setXY(self, x , y):
        """
        Sets x and y coordinate.
        Parameters:
            x: x-coordinate of the Point
            y: y-coordinate of the Point
        """
        self.x = x
        self.y = y
        assert type(x) == int, "x should be an Integer"
        assert type(y) == int, "y should be an Integer"


    def getX(self):
        """
        Returns the x-coordinate of the Point
        Return type: Integer
        """
        return self.x

    def getY(self):
        """
        Returns the y-coordinate of the Point
        Return type: Integer
        """
        return self.y

    def show(self):
        """
        Prints the coordinates of the Point
        """
        print(self.getX(),self.getY())

    def isEqual(self, p2):
        """
        Returns true if p2 is equal to the point object.
        Parameters:
            p2: an object of type point
        """
        assert type(p2) == Point, "p2 should be of type Point"
        return self.x == p2.x and self.y == p2.y


class Grid:
    """
    Data Members:
        N : size of the grid
        start : original position of the player
        goal: final position of the player
        myObstacles: an array of obstacles
        myRewards: an array of rewards

    Member Functions:
        rotateClockwise(n) : rotates the grid clockwise n times by 90 degrees.
        rotateAnticlockwise(n) : rotates the grid anti-clockwise n times by 90 degrees .
        showGrid() : prints the grid on the console.
    """

    def __init__(self, N, start, goal, myObstacles, myRewards):
        """
        Preconditions:
            N : an Integer
            start : an object of type Point
            goal: an object of type Point
            myObstacles: a list of objects of obstacles
            myRewards: a list of objects of Rewards
        """
        #Invariants
        assert type(N) == int, "N should be of type int "
        assert type(start) == Point, "start should be of type Point"
        assert type(goal) == Point, "Goal should be of type Point"
        assert assertObstacles(myObstacles), "myObstacles should be a list containing obstacles"
        assert assertRewards(myRewards), "myRewards should be a list containing rewards"

        self.N = N
        self.start = start
        self.goal = goal
        self.myObstacles = myObstacles
        self.myRewards = myRewards

    def rotateClockwise(self, n):
        """
        Rotates the grid clockwise n times by 90 degrees. The position of goal position
        and player doesn't change.
        Parameters:
            n: The number of times the grid has to be rotated
        """
        pass

    def rotateAnticlockwise(self, n):
        """
        Rotates the grid anti-clockwise n times by 90 degrees. The position of goal position
        and player doesn't change.
        Parameters:
            n: The number of times the grid has to be rotated
        """
        pass

    def showGrid(self, playerPos):
        """
        Prints the grid on the console. Representation of game objects:
        Obstacles: '#'
        Rewards: By their Value
        Empty Cells: '.'
        Player: '0'
        """
        for i in range(self.N):
            for j in range(self.N):
                temp = Point(i,j)
                for reward in myRewards:
                    if temp.isEqual(reward.getPos()):
                        print(reward.getValue(), end=" ")
                if temp in self.myObstacles:
                    print("#", end =" ")
                elif temp.isEqual(start): #start will be changed to player pos after every turn
                    print("O", end = " ")
                elif temp.isEqual(goal):
                    print("G", end = " ")
                else:
                    print(".", end = " ")
            print()
        pass

    def checkEvent(self, playerPos):


    def setN(self, n):
        """
        Sets the size of the grid to n
        Parameters:
            n: an Integer Value depicting the size of the grid
        """
        self.N = n

    def getN(self):
        """
        Returns the size of the grid
        """
        return self.N

    def setStart(self, st):
        """
        Sets the start position
        Parameters:
            st: a Point object depicting the start position
        """
        self.start = st

    def getStart(self):
        """
        Returns the start position of the player
        """
        return self.start

    def setGoal(self, go):
        """
        Sets the Goal position
        Parameters:
            go: a Point object depicting the goal position
        """
        self.goal = go

    def getGoal(self):
        """
        Returns the end position of the player
        """
        return self.goal


class Obstacle:
    """
    Represented as '#' on the grid.

    Data Members:
        x: x-coordinate of obstacle
        y: y-coordinate of obstacle
    No Member Functions
    """

    def __init(self, x, y):
        self.x = x
        self.y = y


class Reward:
    """
    Represented by its value on the grid.

    Data Members:
        x: x-coordinate of reward
        y: y-coordinate of reward
        value: Value of the reward
    No Member Functions
    """

    def __init(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def getValue(self):
        """
        Returns the value of the reward
        """
        return self.value

    def setValue(self, newValue):
        """
        Sets the value of the reward to newValue
        Parameters:
            newValue: The new value of the reward
        """
        self.value = newValue


class Player:
    """
    Represented by 'O' on the grid.

    Data Members:
        x: x-coordinate of player
        y: y-coordinate of player
        energy: Energy of the player

    Member Functions:
        makeMove(s) : moves the player
    """

    def __init(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def makeMove(self, s):
        """
        Moves the player according to the user input.
        R: Moves the player to the Right
        L: Moves the player to the Left
        U: Moves the player to the Up
        D: Moves the player to the Down
        A: Rotates the grid anti-clockwise
        C: Rotates the grid clockwise

        Parameters:
            s: The string containing instructions to move.
            eg. s = "R4D3L2U1" means move 4 units to the right, then 3 units down,
            then 2 units to the left and finally 1 unit upwards.
        """
        instructions = s.upper()

        pass
    def makeMoveRight(self, value):
        for i in range(value):
            self.pos.setXY(self.pos.getX()+1,self.pos.getY())
            # G.setStart(self.pos)
            self.energy -= 1
            G.checkEvent(self.pos)

    def getEnergy(self):
        """
        Returns player energy
        """
        return self.energy

    def setEnergy(self, e):
        """
        Sets the player energy to e
        Parameters:
            e : The value to which energy is to be set
        """
        self.energy = e

    def setPosition(self, xNew, yNew):
        """
        Sets the position of player to x,y

        Parameters:
            x: The x-coordinate to which the player has to move
            y: The y-coordinate to which the player has to move
        """
        self.x = xNew
        self.y = yNew

    def getPosition(self):
        """
        Returns the position of player in a (x,y) format
        """
        return self.x,self.y
