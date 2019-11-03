import os
import time
import random
import copy

def clear(): #for clear screen
    _= os.system('cls')


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

    def __init__(self, N, difficulty):
        """
        Preconditions:
            N : the size of the grid, an Integer Value
            start,goal,myRewards,myObstacles assigned randomly.
        """
        #Invariants
        assert type(N) == int, "N should be of type int "
        assert difficulty in ["H","E"], "Invalid Difficulty"
        global P
        self.N = N
        points = []
        if self.N == 2:
            noOfPoints = 1
        elif self.N == 3:
            noOfPoints = self.N
        elif self.N == 4:
            noOfPoints = self.N
        elif difficulty[0] == 'H':
            noOfPoints = 2 * self.N
        elif difficulty[0] == 'E':
            noOfPoints = self.N
        boundaryList = [1,self.N]
        while len(points) != 2:
            first = random.sample(range(1, self.N + 1), 1)
            if first in boundaryList:
                second = random.sample(range(1, self.N + 1), 1)
                second = second[0]
            else:
                second = random.sample(range(2), 1)
                second = boundaryList[second[0]]
                # print(second)
            newPoint = (first[0],second)
            if newPoint not in points:
                points.append(newPoint)
        while len(points) != 2 * noOfPoints + 2:
            #generate tuple
            ptX = random.sample(range(1, self.N + 1), 1)
            ptY = random.sample(range(1, self.N + 1), 1)
            pt = (ptX[0],ptY[0])
            if pt not in points:
                points.append(pt)
        self.start = points[0]
        self.goal = points[1]
        self.myObstacles = []
        self.myRewards = []
        for i in range(2, 2 + noOfPoints):
            obstacle = Obstacle(points[i][0], points[i][1])
            self.myObstacles.append(obstacle)
        for i in range(2 + noOfPoints, 2 + 2 * noOfPoints):
            value = random.sample(range(1,10), 1)
            reward = Reward(points[i][0], points[i][1], value[0])
            self.myRewards.append(reward)
        # print(self.start,self.goal,self.myObstacles,self.myRewards)
        # self.showGrid()
        P.setPosition(self.start[0],self.start[1])

    def rotateAnticlockwise(self, n):
        """
        Rotates the grid anti-clockwise n times by 90 degrees. The position of goal position
        and player doesn't change.
        Parameters:
            n: The number of times the grid has to be rotated
        """
        global P
        for k in range(n % 4):
            newobstacle = []
            newreward = []
            for i in self.myObstacles:
                j = Obstacle(i.y, self.N - i.x +1)
                newobstacle.append(j)
            for i in self.myRewards:
                j = Reward(i.y, self.N - i.x + 1, i.getValue())
                newreward.append(j)
            self.myObstacles = copy.deepcopy(newobstacle)
            self.myRewards = copy.deepcopy(newreward)
        check = self.isObstacle(P.getPosition())
        if check[0]:
            print("Grid can't be rotated. Player clashing with obstacle.")
            time.sleep(2)
            self.rotateClockwise((n % 4))
            # P.increaseEnergy(1)
        else:
            self.checkEvent(P)
            for i in range(n):
                P.decreaseEnergy(self.N//3)
        pass

    def rotateClockwise(self, n):
        """
        Rotates the grid clockwise n times by 90 degrees. The position of goal position
        and player doesn't change.
        Parameters:
            n: The number of times the grid has to be rotated
        """
        self.rotateAnticlockwise(n * 3)
        for i in range(2 * n):
            P.increaseEnergy(self.N//3)
        pass

    def showGrid(self):
        """
        Prints the grid on the console. Representation of game objects:
        Obstacles: '#'
        Rewards: By their Value
        Empty Cells: '.'
        Player: '0'
        """
        global P, visited
        clear()
        print("ENERGY:", P.getEnergy())
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                # temp = Point(i,j)
                temp = (j,i)
                rew = self.isReward(temp)
                ob = self.isObstacle(temp)
                if temp == P.getPosition(): #start will be changed to player pos after every turn
                    print("O", end = " ")
                elif temp == self.goal:
                    print("G", end = " ")
                elif temp in visited:
                    print("X", end = " ")
                elif rew[0]:
                    print(rew[1].getValue(), end =" ")
                elif ob[0]:
                    print("#", end =" ")
                else:
                    print(".", end = " ")
            print()
        time.sleep(1)

    def isReward(self, pt):
        ans = (False,False)
        for i in self.myRewards:
            if i.isEqual(pt):
                ans = (True,i)
        return ans

    def isObstacle(self, pt):
        ans = (False,1)
        for i in self.myObstacles:
            if i.isEqual(pt):
                ans = (True,i)
        return ans

    def checkEvent(self, player):
        rew = self.isReward(player.getPosition())
        ob = self.isObstacle(player.getPosition())
        if player.getPosition() == self.goal and len(self.myRewards) == 0:
            gameOver = True
            return True
        elif player.getPosition() == self.goal:
                print("Collect all rewards and come back to win the game.")
                time.sleep(2)
        elif rew[0]:
            player.increaseEnergy(rew[1].getValue() * initialEnergy)
            self.myRewards.remove(rew[1])
        elif ob[0]:
            player.decreaseEnergy(4 * initialEnergy)
            # self.myObstacles.remove(ob[1])
        player.decreaseEnergy(1)
        if player.getEnergy() <= 0:
            gameOver = True
            return False
        pass

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

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isEqual(self, pt):
        return self.x == pt[0] and self.y == pt[1]


class Reward:
    """
    Represented by its value on the grid.

    Data Members:
        x: x-coordinate of reward
        y: y-coordinate of reward
        value: Value of the reward
    No Member Functions
    """

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def isEqual(self, pt):
        return self.x == pt[0] and self.y == pt[1]

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

    def __init__(self, x, y, energy):
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
        global visited
        s = s.upper()
        visited.append((self.x,self.y))
        for i in range(len(s)):
            if s[i].isalpha():
                for j in range(i + 1,len(s)):
                    if s[j].isalpha():
                        j -= 1
                        break
                val = int(s[i+1:j + 1])
                if s[i] == 'R':
                    self.makeMoveRight(val)
                elif s[i] == 'L':
                    self.makeMoveLeft(val)
                elif s[i] == 'U':
                    self.makeMoveUp(val)
                elif s[i] == 'D':
                    self.makeMoveDown(val)
                elif s[i] == 'C':
                    G.rotateClockwise(val)
                    self.energy += 1
                elif s[i] == 'A':
                    G.rotateAnticlockwise(val)
                    self.energy += 1
                i = i + j - 1
        pass

    def makeMoveRight(self, value):
        global G,gameOver,visited
        for i in range(value):
            self.x += 1
            if G.getN() < self.x:
                self.x = 1
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True:
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False:
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()
            # G.checkEvent((self.x,self.y))
            # G.showGrid()

    def makeMoveLeft(self, value):
        global G,gameOver,visited
        for i in range(value):
            self.x -= 1
            if self.x < 1:# G.setStart(self.pos)
                self.x = G.getN()
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True:
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False:
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()

    def makeMoveUp(self, value):
        global G,gameOver,visited
        for i in range(value):
            self.y -= 1
            if self.y < 1:
                self.y = G.getN()
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True:
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False:
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()

    def makeMoveDown(self, value):
        global G,gameOver,visited
        for i in range(value):
            self.y += 1
            if G.getN() < self.y:
                self.y = 1
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True:
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False:
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()

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

    def increaseEnergy(self, e):
        """
        Increases the player energy by e
        Parameters:
            e : The value by which energy is to be incremented
        """
        self.energy += e

    def decreaseEnergy(self, e):
        """
        Decreases the player energy by e
        Parameters:
            e : The value by which energy is to be decremented
        """
        self.energy -= e

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
        return (self.x,self.y)


visited = []
print("What should be the size of the grid?")
N = int(input())
print("Choose difficulty: 'H' for Hard and 'E' for Easy:")
diff = input()

initialEnergy = N
P = Player(0,0,2 * initialEnergy)
G = Grid(N,diff)
gameOver = False
s=''

while s != 'EXIT' and not(gameOver):
    visited = []
    clear()
    print("ENERGY:",P.getEnergy())
    G.showGrid()
    s = input()
    if s != 'EXIT':
        P.makeMove(s)
