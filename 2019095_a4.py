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
        goal: position to reach in order to win
        myObstacles: an list of obstacles
        myRewards: an list of rewards

    Member Functions:
        rotateClockwise(n) : rotates the grid clockwise n times by 90 degrees.
        rotateAnticlockwise(n) : rotates the grid anti-clockwise n times by 90 degrees .
        showGrid() : prints the grid on the console.
        isReward(pt) : returns True if point pt is one of the reward point
        isObstacle(pt) : returns True if point pt is one of the obstacle point
        checkEvent(player) : checks the status of grid after each turn and handles energy increment/ decrement.
    """

    def __init__(self, N, difficulty):
        """
        Preconditions:
            N : the size of the grid, an Integer Value
            difficulty : an character having 'H' for hard difficulty and 'E' for easy difficulty
            start,goal,myRewards,myObstacles assigned randomly.
        """
        #Invariants
        assert type(N) == int, "N should be of type int "
        assert difficulty in ["H","E","h","e"], "Invalid Difficulty"
        global P
        difficulty = difficulty.upper()
        self.N = N
        points = []
        if self.N == 2: #difficulty doesn't matter when N < 5 because it isn't possible to have 4*n + 2 points in grid size < 5
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
        while len(points) != 2: # to make sure start and goal are points at the boundary
            first = random.sample(range(1, self.N + 1), 1)
            if first in boundaryList: # if x coordinate on boundary then y can be anything
                second = random.sample(range(1, self.N + 1), 1)
                second = second[0]
            else: # if x coordinate not on boundary then y has to be on boundary
                second = random.sample(range(2), 1)
                second = boundaryList[second[0]]
                # print(second)
            newPoint = (first[0],second)
            if newPoint not in points:
                points.append(newPoint)
        while len(points) != 2 * noOfPoints + 2:#sets 2*n + 2 unique points in points list which then get assigned to obstacle rewards. start, goal
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
        for i in range(2, 2 + noOfPoints): # initialisation of obstacles
            obstacle = Obstacle(points[i][0], points[i][1])
            self.myObstacles.append(obstacle)
        for i in range(2 + noOfPoints, 2 + 2 * noOfPoints): # initialisation of rewards
            value = random.sample(range(1,10), 1)
            reward = Reward(points[i][0], points[i][1], value[0])
            self.myRewards.append(reward)
        # print(self.start,self.goal,self.myObstacles,self.myRewards)
        # self.showGrid()
        P.setPosition(self.start[0],self.start[1])# initialising player position to start

    def rotateAnticlockwise(self, n):
        """
        Rotates the grid anti-clockwise n times by 90 degrees. The position of goal position
        and player doesn't change.
        Parameters:
            n: The number of times the grid has to be rotated
        """
        global P, visited
        for k in range(n): # since after 4 rotation, grid back to original position
            newobstacle = []
            newreward = []
            for i in self.myObstacles:
                j = Obstacle(i.y, self.N - i.x +1) # formula for rotation which i got from doing rotation in my notebook
                newobstacle.append(j)
            for i in self.myRewards:
                j = Reward(i.y, self.N - i.x + 1, i.getValue())
                newreward.append(j)
            self.myObstacles = copy.deepcopy(newobstacle) # myObstacles assigned new rotated obstacles
            self.myRewards = copy.deepcopy(newreward) # myRewards assigned new rotated rewards
        check = self.isObstacle(P.getPosition())
        if check[0]:
            print("Grid can't be rotated. Player clashing with obstacle.") # if clashing with obstacle
            time.sleep(2)
            self.rotateClockwise(n) # undo rotate antiCLockwise by rotating clockWise same number of times
            # P.increaseEnergy(1)
        else:
            visited = []
            for i in range(n): #decreaseEnergy for each n
                P.decreaseEnergy(self.N//3)
            # self.checkEvent(P)
        pass

    def rotateClockwise(self, n):
        """
        Rotates the grid clockwise n times by 90 degrees. The position of goal position
        and player doesn't change.
        Parameters:
            n: The number of times the grid has to be rotated
        """
        global P
        self.rotateAnticlockwise(n * 3) # rotating n clockwise is same as rotating 3*n anti clockwise
        for i in range(2 * n):
            P.increaseEnergy(self.N//3)
        # self.checkEvent(P)
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
        if P.getEnergy() > 0:
            e = P.getEnergy()
        else:
            e = 0
        print("ENERGY:", e)
        for i in range(1, self.N+1):
            for j in range(1, self.N+1): # iterating through every point, if point is reward then print corresponding value if obstacle then # if goal then G if player then O else .
                temp = (j,i)
                rew = self.isReward(temp)
                ob = self.isObstacle(temp)
                if temp == P.getPosition():
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
        time.sleep(1) # delay to show each step

    def isReward(self, pt):
        """
        Parameters:
            pt: A tuple of the form (x,y)

        Function returns (True,index of reward pt that is equal to pt) if point pt is one of the points in myRewards else (false,false)
        """
        ans = (False,False)
        for i in self.myRewards:
            if i.isEqual(pt):
                ans = (True,i)
        return ans

    def isObstacle(self, pt):
        """
        Parameters:
            pt: A tuple of the form (x,y)

        Function returns (True, index of obstacle pt that is equal to pt) if point pt is one of the points in myObstacles else (false,1)
        """
        ans = (False,1)
        for i in self.myObstacles:
            if i.isEqual(pt):
                ans = (True,i)
        return ans

    def checkEvent(self, player):
        """
        Handles energy and checks if Game Over or not after each step
        Returns true if game over and player won
        Returns false if game over and player lost
        Returns none if game not over
        """
        rew = self.isReward(player.getPosition()) # performing checks if player on a reward
        ob = self.isObstacle(player.getPosition())# performing checks if player on an obstacle
        if player.getPosition() == self.goal and len(self.myRewards) == 0: # if all rewards eaten and player on goal
            gameOver = True
            return True
        elif player.getPosition() == self.goal: # if player on goal but all rewards not eaten
                print("Collect all rewards and come back to win the game.")
                time.sleep(2)
        elif rew[0]: # if player on reward then increase energy value*n
            player.increaseEnergy(rew[1].getValue() * initialEnergy)
            self.myRewards.remove(rew[1])
        elif ob[0]: # if player on obstacle then decrease energy 4*n
            player.decreaseEnergy(4 * initialEnergy) # obstacle not removed after hitting obstacle
            # self.myObstacles.remove(ob[1])
        player.decreaseEnergy(1)
        if player.getEnergy() <= 0: # if playe renergy non- positive then game Over
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
    Member Functions:
        isEqual(pt) : returns True if point pt equals the obstacle point
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isEqual(self, pt):
        """
        Parameters:
            pt : A tuple of form (x,y)
        Returns true if pt is equal to coordinates of obstacle
        """
        return self.x == pt[0] and self.y == pt[1]


class Reward:
    """
    Represented by its value on the grid.

    Data Members:
        x: x-coordinate of reward
        y: y-coordinate of reward
        value: Value of the reward
    Member Functions:
        isEqual(pt) : returns True if point pt equals the reward point
    """

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def isEqual(self, pt):
        """
        Parameters:
            pt: A tuple of the form (x,y)
        Returns true if pt is equal to coordinates of reward
        """
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
        getEnergy(): returns the energy of the player
        setEnergy(e) : sets the energy of the player to e
        increaseEnergy(e) : increases the energy of the player by e
        decreaseEnergy(e) : decreases the energy of the player by e
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
        global visited, gameOver
        s = s.upper()
        visited.append((self.x,self.y)) # to display 'x' as trail
        for i in range(len(s)):
            if s[i].isalpha(): # if found an alphabet then it sees the number ahead of it and puts the number in value
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
                    self.energy += 1 # because energy to be decreased is ony n//3 and checkEvent decreases 1 for every move
                    check = G.checkEvent(self)
                    if check == True: # if won the game
                        G.showGrid()
                        print("You Won")
                        gameOver = True
                        break
                    elif check == False: # if lost the game
                        G.showGrid()
                        print("You Lose")
                        gameOver = True
                elif s[i] == 'A':
                    G.rotateAnticlockwise(val)
                    self.energy += 1 # because energy to be decreased is ony n//3 and checkEvent decreases 1 for every move
                    check = G.checkEvent(self)
                    if check == True: # if won the game
                        G.showGrid()
                        print("You Won")
                        gameOver = True
                        break
                    elif check == False: # if lost the game
                        G.showGrid()
                        print("You Lose")
                        gameOver = True
                i = i + j - 1 # goes directly to the new alphabet
        pass

    def makeMoveRight(self, value):
        """
        Parameters :
            value : the amount by which the player had to be moved
        Moves the player to the right
        """
        global G,gameOver,visited
        for i in range(value):
            self.x += 1
            if G.getN() < self.x: # if player on last colum then spawm player at the first column
                self.x = 1
            visited.append((self.x,self.y)) # adds trail
            check = G.checkEvent(self)
            if check == True: # if won the game
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False: # if lost the game
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()
            # G.checkEvent((self.x,self.y))
            # G.showGrid()

    def makeMoveLeft(self, value):
        """
        Parameters :
            value : the amount by which the player had to be moved
        Moves the player to the left
        """
        global G,gameOver,visited
        for i in range(value):
            self.x -= 1
            if self.x < 1: # if player on the first columnn then ove player to last column
                self.x = G.getN()
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True: # if player won
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False: # if player lost
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()

    def makeMoveUp(self, value):
        """
        Parameters :
            value : the amount by which the player had to be moved
        Moves the player above
        """
        global G,gameOver,visited
        for i in range(value):
            self.y -= 1
            if self.y < 1: # if player on the first row then move player to the last row
                self.y = G.getN()
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True: # if won the game
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False: # if lost the game
                G.showGrid()
                print("You Lose")
                gameOver = True
                break
            else:
                G.showGrid()

    def makeMoveDown(self, value):
        """
        Parameters :
            value : the amount by which the player had to be moved
        Moves the player downwards
        """
        global G,gameOver,visited
        for i in range(value):
            self.y += 1
            if G.getN() < self.y: # if player on the last row then move paer to the first row
                self.y = 1
            visited.append((self.x,self.y))
            check = G.checkEvent(self)
            if check == True: # if player own the game
                G.showGrid()
                print("You Won")
                gameOver = True
                break
            elif check == False: # if player lost the game
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


#INPUT
visited = [] # since no point visited
print("What should be the size of the grid?")
N = int(input())
print("Choose difficulty: 'H' for Hard and 'E' for Easy:")
diff = input()
#INITIALISING THE OBJECTS
initialEnergy = N
P = Player(0,0,2 * initialEnergy)  # initialising the player object
G = Grid(N,diff) # initialising grid
gameOver = False # gameover boolean
s=''
#MAIN GAME RUNNER LOOP
while s != 'EXIT' and not(gameOver): # s!= EXIT condition to forcefully quit the code
    visited = [] # to remove trail after every move
    clear()
    print("ENERGY:",P.getEnergy()) # display energy and grid after every move
    G.showGrid()
    s = input() # taking next move till game not over
    if s != 'EXIT':
        P.makeMove(s)
