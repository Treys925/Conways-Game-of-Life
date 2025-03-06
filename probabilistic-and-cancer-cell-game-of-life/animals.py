import numpy as np

# A standard oscillator
oscillator = np.array(
             [
               [False, True, False],
               [False, True, False],
               [False, True, False],
             ])

# An oscillator on a torus
wack_oscillator = np.array(
             [
               [False, True, False],
               [False, True, False],
               [False, False, False],
               [False, False, False],
               [False, True, False]
             ])

# A standard Glider
glider = np.array(
         [
           [False, True, False],
           [False, False, True],
           [True, True, True],
         ])

# A beehive still life
still_life = np.array(
         [
           [False, True, False],
           [True, False, True],
           [True, False, True],
           [False, True, False],
         ])

empty_grid = np.zeros((51, 51))

# Place an animal into a grid with corner at (i, j)
def insert_animal_mut(grid, animal, i, j):
    (i_len, j_len) = animal.shape
    grid[i:i + i_len, j:j + j_len] = animal
    return grid

# Copy a grid and rlace an animal into the new grid with corner at (i, j)
def insert_animal(grid, animal, i, j):
    return insert_animal_mut(grid.copy(), animal, i, j)

# Generates a random grid.
def randomGrid(shapex, shapey, prob=0.5):
    return (np.random.rand(shapex, shapey) < prob)
