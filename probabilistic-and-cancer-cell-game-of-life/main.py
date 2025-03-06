from window import Window #This is the winodw.py file
#The below are are used for gui
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

import numpy as np

#this is for the timer
import sys
import os
import argparse
import time

# Conway module
import conway
import animals

#TileN must evenly divide width
width=600 #Width in Pixels of the board
height=width#Height in Pixels of the board
tileN=30 #Number of tiles in a row or column

# Add in all the different arguments that we take on the command line with defaults and help instructioons
parser = argparse.ArgumentParser(description="Conway's Probabilistic Game of Life")
parser.add_argument('--nogui', dest='nogui', action='store_true',
                    help='Run Without the GUI')
parser.add_argument('--steps', dest='steps', type=int, default=1000, help='Steps to run nogui for')
parser.add_argument('--output', dest='output', action='store',
                    default='data/output.csv',
                    help='Desired output file')
parser.add_argument('--lower-prob', dest='lowerProb', type=float,nargs='+', help='Lower Probabilities for the neighbors', default=[1,1,-1,-1,1,1,1,1,1])
parser.add_argument('--higher-prob', dest='higherProb', type=float, nargs='+', help='Higher Probabilities for the neighbors', default=[1,1,1,-1,1,1,1,1,1])
parser.add_argument('--grid-width', dest='gridWidth', type=int, help='Grid Width', default=30)
parser.add_argument('--grid-height', dest='gridHeight', type=int, help='Grid Height', default=30)
parser.add_argument('--cutoff', dest='cutoff', type=int, help='Cutoff Time for CSV', default=250)
parser.add_argument('--aggregate', dest='aggregate', type=int, help='Whether to Aggregate CSV data, 0 means the flag is off', default=0)

# Helper function which checks whether or not a file can be written to.
def check_file_writable(fnm):
    if os.path.exists(fnm):
        # path exists
        if os.path.isfile(fnm): # is it a file or a dir?
            # also works when file is a link and the target is writable
            return os.access(fnm, os.W_OK)
        else:
            return False # path is a dir, so cannot write as a file
    # target does not exist, check perms on parent dir
    pdir = os.path.dirname(fnm)
    if not pdir: pdir = '.'
    # target is creatable if parent dir is writable
    return os.access(pdir, os.W_OK)

def main():
    # Parse out the arguments
    args = parser.parse_args()
    game = conway.Game(aProbRuleLower=args.lowerProb, aProbRuleHigher=args.higherProb)

    # Run the game in the GUI if we can
    if not args.nogui:
        game = conway.gameProb2Repro

        #This makes the program actually run
        App = QApplication(sys.argv)
        window = Window(width, height, args.gridWidth, game)
        window.show()
        sys.exit(App.exec())
    elif check_file_writable(args.output):
        # Check if we're doing an aggregate run for CSV Data selection
        if args.aggregate == 0:
            # Generate a random grid and run a CSV output
            grid = animals.randomGrid(args.gridWidth, args.gridHeight)
            game.runCSV(grid, args.steps, args.output, args.cutoff)
        else:
            print("Running Trial: 1")

            # Run the first trial to seed all the variables
            init_grid = animals.randomGrid(args.gridWidth, args.gridHeight)
            (_, _, _, liveFFTFreq, liveFFT) = game.runFFT(init_grid, args.steps, args.cutoff)
            avgFFT = np.abs(liveFFT)/args.aggregate

            # Run the rest of the trials
            for i in range(1, args.aggregate):
                print("Running Trial: " + str(i + 1))

                # Initialize grid and run FFT, update the average FFT signal
                grid = animals.randomGrid(args.gridWidth, args.gridHeight)
                (_, _, _, _, newFFT) = game.runFFT(grid, args.steps, args.cutoff)
                avgFFT += np.abs(newFFT)/args.aggregate

                # Save the current average to a file in order not to lose data in the case of incomplete runs
                arr = np.transpose([liveFFTFreq, avgFFT])
                print("Saving Trial: " + str(i + 1))
                if check_file_writable(args.output.replace('.csv', f'-{i:03}.csv')):
                    np.savetxt(args.output.replace('.csv', f'-{i:03}.csv'), arr, delimiter=',', fmt='%f', header='Conway Game of Life, Aggregated Frequency Count for ' + str(args.aggregate) + ' trials :: Header')

            # Save the total run and data
            arr = np.transpose([liveFFTFreq, avgFFT])
            np.savetxt(args.output, arr, delimiter=',', fmt='%f', header='Conway Game of Life, Aggregated Frequency Count for ' + str(args.aggregate) + ' trials :: Header')
    else:
        print("ERROR: No output file specified in nogui mode")

if __name__ == "__main__":
    main()
