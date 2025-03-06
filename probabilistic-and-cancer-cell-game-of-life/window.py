#The below are are used for gui
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#Needed for timer/math
import sys
import conway
import math as m
import numpy as np
import animals

# Draws a given grid onto the screen
def drawGrid(grid, length, qp):
    for x in range(0, grid.shape[0]):
        for y in range(0, grid.shape[1]):
            buffer=1 #gives a one pixel buffer so the window isnt all black
            offset=50 #shifts the board down 50 pixels to make room for the buttons
            # Set the brush color depending on if you're alive or dead
            if grid[x, y]:
                qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))
            else:
                qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))

            # Draw it!
            qp.drawRect(length*x+buffer, length*y+buffer+offset, length-2*buffer, length-2*buffer)


#defines the methods of window class. This is where all of the buttons and interaction go
class Window(QMainWindow):
    def __init__(self, width, height, tileN, game):
        super(Window, self).__init__()

        #Sets the Attributes of the window
        self.title = "Game of Life"
        self.top = 0 #The topmost pixel on the screen where the window begins
        self.left = 0#The leftmost pixel on the screen where the window begins
        self.width = width
        self.height = height
        self.tileN=tileN
        self.game = game
        self.grid=np.zeros((self.tileN, self.tileN))
        self.live_cells=[0]
        self.speed=100 #speed of refresh in ms
        self.timer = QBasicTimer() #initiates a timer


        #This is model code for the start button
        start = QPushButton('Start Cycle', self) #String is what the button is labeled
        start.resize(100,50) #Size of the botton in XxY pixels#
        start.move(0, 0) #places the button in the window
        start.clicked.connect(self.clickStart) #calls the ClickStart Method when clicked

        #The next four are all models of the start button
        stop = QPushButton('Stop Cycle', self)
        stop.resize(100,50)
        stop.move(100, 0)
        stop.clicked.connect(self.clickStop)

        # This button progresses the game forward one step
        forward = QPushButton('Forward', self)
        forward.resize(100,50)
        forward.move(200, 0)
        forward.clicked.connect(self.clickForward)

        # This button wipes the board to all dead cells
        wipe = QPushButton('Wipe', self)
        wipe.resize(100,50)
        wipe.move(300, 0)
        wipe.clicked.connect(self.clickWipe)

        # This button gives a randomized board
        random = QPushButton('Random', self)
        random.resize(100,50)
        random.move(400, 0)
        random.clicked.connect(self.clickRandom)

        # Export the current game data to a CSV file
        csv_export = QPushButton('Export CSV', self)
        csv_export.resize(100,50)
        csv_export.move(500, 0)
        csv_export.clicked.connect(self.clickExport)


        # This clears the game data that would be exported to a CSV file
        csv_clear = QPushButton('Clear CSV', self)
        csv_clear.resize(100,50)
        csv_clear.move(600, 0)
        csv_clear.clicked.connect(self.clickClearCSV)


        # Create Probability Sliders
        self.slidersLower = []
        self.slidersHigher = []
        self.labels = []
        for i in range(0, 9):
            sliderLower = QSlider(Qt.Horizontal, self)
            sliderLower.move(600,100 * (i + 1))
            sliderLower.setFocusPolicy(Qt.StrongFocus)
            sliderLower.setSingleStep(1)
            sliderLower.valueChanged.connect(self.valChangeLower)
            sliderLower.setMinimum(-100)
            sliderLower.setMaximum(100)
            sliderLower.setValue(self.game.probRuleLower[i] * 100)
            sliderLower.tickPosition = QSlider.NoTicks

            sliderHigher = QSlider(Qt.Horizontal, self)
            sliderHigher.move(700,100 * (i + 1))
            sliderHigher.setFocusPolicy(Qt.StrongFocus)
            sliderHigher.setSingleStep(1)
            sliderHigher.valueChanged.connect(self.valChangeHigher)
            sliderHigher.setMinimum(-100)
            sliderHigher.setMaximum(100)
            sliderHigher.setValue(self.game.probRuleHigher[i] * 100)
            sliderHigher.tickPosition = QSlider.NoTicks

            label = QLabel(self)
            label.setText("Probability Slider for " + str(i) + " neighbors")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 12))
            label.resize(300, 20)
            label.move(800, 100 * (i + 1))

            self.slidersLower.append(sliderLower)
            self.slidersHigher.append(sliderHigher)
            self.labels.append(label)


        #Does what the method says. These are inhertied from the parent window class
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        self.updateTiles()#calls the updatesTiles method, which updates the tiles

    # Update Lower Probabilities due to a change
    def valChangeLower(self):
        for i in range(0, 8):
            if i < len(self.slidersLower) and i < len(self.game.probRuleLower):
                self.game.probRuleLower[i] = self.slidersLower[i].value()/100

    # Update Higher Probabilities due to a change
    def valChangeHigher(self):
        for i in range(0, 8):
            if i < len(self.slidersHigher) and i < len(self.game.probRuleHigher):
                self.game.probRuleHigher[i] = self.slidersHigher[i].value()/100

    # Update the entire game based on previous grid state
    def updateTiles(self):
        self.grid[:] = (self.game.update(self.grid))[:] #updates the window
        self.live_cells.append(np.sum(self.grid))
        self.update()#updates the window

    # Starts the game running
    def clickStart(self): #starts timer
        self.timer.start(self.speed, self)

    # Stops the game running
    def clickStop(self): #stops timer
        self.timer.stop()

    def clickForward(self): #when forward is clicked, moves the grid state forward one step by updateing the grid
        self.updateTiles()

    def clickWipe(self): #when wipe is clicked, resets the grid, and then updates the tiles
        self.grid = np.zeros((self.tileN, self.tileN))
        self.update()

    def clickRandom(self): #when random is clicked generates a random grid and then updates the tiles
        self.grid = animals.randomGrid(self.tileN, self.tileN)
        self.update()

    def clickExport(self): #when export csv is clicked, exports all the data to a CSV file that the user picks
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            print("Exporting CSV to file: " + fileName)
            np.savetxt(fileName, [self.live_cells], delimiter=',', fmt='%d', header='Conway Game of Life, Live Cell Count :: Header')

    def clickClearCSV(self): #when clear csv is clicked clears the output that would be saved to a CSV
        self.live_cells = [0]

    def timerEvent(self, event): #updates the tiles as determined by the timer speed.
        self.updateTiles()

    def mousePressEvent(self, QMouseEvent): #gets the position of a click, converts it to a tile, and then turns that tile one or off
        pixX=0 #pixel x#
        pixY=0 #pixel y#
        tileX=0 #tile x#
        tileY=0 #tile y#
        posArray=QMouseEvent.pos() #gives a position object of the mouse click coordinates
        pixX=posArray.x() #retrieves the x coordinate from the pos object
        pixY=posArray.y() #retrieves the y coordinate from the pos object
        if (pixX<self.width and pixX >=0 and pixY<self.height+50 and pixY >=50): #determines that the mouse click was actually on the grid and not the button
            tileX=int(pixX*self.tileN/self.width) #converts pixel x to tile x, the division is why we need even division on the life.py file.
            tileY=int((pixY-50)*self.tileN/self.height)#converts pixel y to tile y, the division is why we need even division on the life.py file.
            self.grid[tileX,tileY] = not self.grid[tileX, tileY]
        self.update() #updates the grid

    def paintEvent(self, e): #this method is called by the built-in update method. This paints the squares on the window.
        painter = QPainter(self)
        drawGrid(self.grid, int(self.width/self.tileN), painter)
