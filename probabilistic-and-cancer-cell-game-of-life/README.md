# Conway's Game of Life Implementation and Extensions

This python program implements Conway's Game of Life as well as a number of probabilistic extensions to Conway's Game of Life. The program includes both a GUI mode where you can experience the Game of Life and the extensions in real time as well as a GUI-less mode for collecting data. In order to start into the GUI for basic use one can just run the command
```
python3 main.py
```
For contributing to the project and data collection. One can see CONTRIBUTING.md

## Project Layout

As far as the layout of the modules in the code. There are four primary files:

- main.py: This file handles all the initial command line user input to the program. This consists of command-line arguments as well as flags. Every time a user runs the program it should be through this file directly.
- conway.py: This file implements Conway's Game of Life as well as the extensions in an object oriented way. It also implements the data collection process and output to CSV.
- window.py: This file implements the GUI for Conway's Game of Life that is displayed on screen. It uses PyQt5 to display all the output from conway.py as well as to feed user input into the program.
- animals.py: This is a utility file for testing the program. It includes a number of common configurations in Conway's Game of Life, such as gliders and oscillators

## Usage

Although the command line inputs can be rather daunted, they are all explained by running
```
python3 main.py --help
```
For context, the lower probabilities and upper probabilities are used to determine the probababilistic extension used. There is one such probability for each number of alive neighbors 0-8, entrered as an array. The lower probability and the higher probability partition the interval [-1, 1] into three pieces. When updating a cell with that number of neighbors, the program randomly selects one of these pieces in a manner proportional to its length. If it picks the left piece, the cell dies, if it picks the middle piece the cell's state stays the same, and if it picks the right piece then the cell will be alive the next turn.

Conway's original game of life, which is the default, can also be reproduced with these options by running:
```
python3 main.py --lower-prob [1,1,-1,-1,1,1,1,1,1] --higher-prob [1,1,1,-1,1,1,1,1,1]
```
The most common probabilistic extension that we consider gives cells with two neighbors a slight 1% chance of reproducing. This is achieved with the following options:
```
python3 main.py --lower-prob [1,1,-1,-1,1,1,1,1,1] --higher-prob [1,1,0.98,-1,1,1,1,1,1]
```

## Dependencies

The program has the following dependencies:

- numpy
- graphics.py
- matplotlib
- PyQt5

These can all be installed by running `pip3 install <dependency>`

## Example GIF

![](example.gif)

## LICENSE

We use the [MIT](https://opensource.org/licenses/MIT) license, which can be found at at LICENSE.md


