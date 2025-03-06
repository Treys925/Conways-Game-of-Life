import matplotlib.pyplot as pl
import matplotlib.animation as animation
import numpy as np
import random
import statistics

# These are the probabilities for sensory data read from each direction
# The adjacent cells represent the probability of live cell being read as alive
# a dead cell being read as alive
# The center cell represents the chance that a cell is alive provided that the rules
# say that it should be alive in the next iteration and provided the rules say it should be dead

example1PL = np.array([[0.002, 0.8, 0.95],
                       [0.75, 1, 0.75],
                       [0.95, 0.8, 0.002]
                      ])
example1PD = np.array([[0, 0.0015, 0.03],
                       [0.001, 0, 0.001],
                       [0.03, 0.0015, 0]
                      ])

# This helper function makes a true or false call based on a probability between 0 and 1 of true

def decision(probability):
    return random.random() < probability

# This helper function makes a three way decision based on two probabilities
# We use this to distinguish between a cell dying, staying the same as the previous state
# or being reproduced

def decisionThree(probability1, probability2):
    r = 2 * random.random() - 1
    if r < probability1:
        return -1
    elif  probability1 <= r and r < probability2:
        return 0
    else:
        return 1

# This function draws a grid to a canvas in order to visualize it

def draw(grid):
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    plt.show()

# These three indexers implement different surfaces that we can play the game on

def indexerNone(ix, iy, x_len, y_len):
    # Check that ix and iy are within the bounds
    usable = 0 <= ix < x_len and 0 <= iy < y_len
    return (ix, iy, usable)

def indexerTorus(ix, iy, x_len, y_len):
    # Exploit a python hack to implement torus behavior
    return (ix % x_len, iy % y_len, True)

def indexerKlein(ix, iy, x_len, y_len):
    if 0 <= ix < x_len:
        return indexerTorus(ix, iy, x_len, y_len)
    else:
        # Reverse orientation and again exploit a Python hack
        return indexerTorus(ix, y_len - iy, x_len, y_len)

class Game:
    # This constructor creates a game with the default parameters corresponding to the traditional game of life.
    def __init__(self, anIndexer=indexerTorus, anUpdateInterval=100, aProbLiving=np.ones((3,3)), aProbDead=np.zeros((3,3)), aProbRuleLower = [1,1,-1,-1,1,1,1,1,1], aProbRuleHigher = [1,1,1,-1,1,1,1,1,1], frms = 1000, saves = 0):
        self.indexer = anIndexer
        self.updateInterval = anUpdateInterval
        self.probLiving = aProbLiving.copy()
        self.probDead = aProbDead.copy()
        self.probRuleLower = aProbRuleLower.copy()
        self.probRuleHigher = aProbRuleHigher.copy()
        self.frames = frms
        self.saves = saves

    # Counts the number of neighbors that a cell has
    def neighbors(self, grid, x, y):
        total = 0
        live = 0
        # Loop through each of the 9 ways one can move from a square
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:

                # Call a custom indexer
                (ix, jy, usable) = self.indexer(x + i, y + j, grid.shape[0], grid.shape[1])

                # Check that we're not at the same cell
                nonzero = i != 0 or j != 0

                if usable and nonzero:
                    # Count both the alive and dead cells, using probLiving and probDead to commit sensory errors
                    if grid[ix, jy] and decision(self.probLiving[i+1,j+1]):
                        live += 1
                    elif (not grid[ix, jy]) and decision(self.probDead[i+1,j+1]):
                        live += 1
                    total += 1
        return (live, total - live)

    # Calculate the next value of a cell based on the rules of the game
    def newCell(self, grid, x, y):
        # Get the number of neighbors
        (live, dead) = self.neighbors(grid, x, y)

        # Store our result intitially as where we were in the previous step
        result = grid[x, y]

        # Use the probability matrix in order to decide whether we are alive or dead or stay the same next turn
        dec = decisionThree(self.probRuleLower[live], self.probRuleHigher[live])
        if dec == -1:
            result = False
        elif dec == 1:
            result = True


        # Update the results based on the probability matrix at the center
        if result:
            return decision(self.probLiving[1, 1])
        else:
            return decision(self.probDead[1, 1])

    # Update an entire grid to the next step of the game
    def update(self, grid):
        newGrid = grid.copy()
        for y in range(0, grid.shape[1]):
            for x in range(0, grid.shape[0]):
                newGrid[x, y] = self.newCell(grid, x, y)
        return newGrid

    # Run the specified grid through the program for a specified number of steps
    # The optional parameter m tells you how often to report which step that you're running
    def runSteps(self, grid, n, m = 10):
        the_grid = grid
        live = [np.sum(the_grid)]
        for i in range(1, n + 1):
            if (i % m) == 0 or i == 1:
                print("Running step: " + str(i))
            the_grid = self.update(the_grid)
            live.append(np.sum(the_grid))
        return (the_grid, live)

    # This function grabs FFT data for the run using numpy
    def runFFT(self, grid, n, cutoff=1, m=10):
        (the_grid, live) = self.runSteps(grid, n, m)

        # Cutoff the data based on the cutoff variable
        newlive_unshifted = live[(cutoff-1):]

        # Shift the data to have mean zero in order to get better FFT data
        live_avg = statistics.mean(newlive_unshifted)
        newlive = list(map(lambda x: (float) (x - live_avg), newlive_unshifted))

        # Run and return the FFT
        liveFFT = np.fft.fft(newlive)
        liveFFTFreq = np.fft.fftfreq(len(newlive))
        return (the_grid, live, newlive, liveFFTFreq, liveFFT)


    # Run the game for some data and output it to CSV
    def runCSV(self, grid, n, fileName, cutoff=1, m = 10):
        (the_grid, live, newlive, liveFFTFreq, liveFFT) = self.runFFT(grid, n, cutoff, m)
        arr = np.array([newlive, liveFFTFreq, np.abs(liveFFT)])
        np.savetxt(fileName, arr, delimiter=',', fmt='%f', header='Conway Game of Life, Live Cell Count :: Header')
        return (the_grid, live, newlive, liveFFTFreq, liveFFT)


    # Run and display the game running in a matplot field, used for testing before we had window.py
    def run(self, grid):
        def anim_update(frameNum, img, grid):
            grid[:] = (self.update(grid))[:]
            img.set_data(grid)
            return img

        fig, ax = plt.subplots()
        img = ax.imshow(grid, interpolation='nearest')

        ani = animation.FuncAnimation(fig, anim_update, fargs=(img, grid, ),interval=self.updateInterval, frames=self.frames, save_count=self.saves)
        plt.show()

# The original Game of Life designed by Conway
gameOfLife = Game()

# The Game of Life described in the paper without the diagonal
gameProbExten = Game()
gameProbExten.probDead = example1PD

# Probablistic Rules, a group of 3 has a 99% chance to reproduce
gameProb3Repro = Game()
gameProb3Repro.probRuleLower[3] = -0.98
gameProb3Repro.probRuleHigher[3] = -0.98

# Probablistic Rules, a group of 2 has a 2% chance to reproduce
gameProb2Repro = Game()
gameProb2Repro.probRuleLower[2] = -1
gameProb2Repro.probRuleHigher[2] = 0.98

# A different probablistic ruleset, overpopulation doesn't always kill
gameProbOverpop = Game()
gameProbOverpop.probRuleLower[3] = -0.98
gameProbOverpop.probRuleHigher[3] = -0.98
gameProbOverpop.probRuleLower[4] = 0.98
gameProbOverpop.probRuleHigher[4] = 1
