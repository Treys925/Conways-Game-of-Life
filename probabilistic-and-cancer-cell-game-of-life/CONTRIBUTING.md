To contribute you'll need python3 with numpy, graphics.py, and matplotlib. You should be able to install these with

```
pip3 install numpy
pip3 install graphics.py
pip3 install matplotlib
pip3 install PyQt5
```

In order to run the basic program run
```
python3 main.py
```
Example Use of commmand line to run a 1% probability for 2 cells to reproduce without a gui for CSV output
```
python3 main.py --nogui --higher-prob 1 1 0.96 -1 1 1 1 1 1 --lower-prob 1 1 -1 -1 1 1 1 1 1 --steps 2000 --grid-width 100 --grid-height 100 --output data/grr.csv
```
Run this command to get an aggregate piece of data for 20 trials of 20k steps for our standard data set.
```
python3 main.py --higher-prob 1 1 0.98 -1 1 1 1 1 1 --lower-prob 1 1 -1 -1 1 1 1 1 1 --aggregate 20 --steps 20000 --cutoff 200 --grid-width 100 --grid-height 100 --nogui --output data/agg.csv
```
