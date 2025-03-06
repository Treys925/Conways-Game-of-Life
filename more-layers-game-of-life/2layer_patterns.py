import pygame
import numpy as np
import matplotlib.pyplot as plt
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)
y = []
t=0
#This file is very cool, can find oscillators, have a lot of nice patterns showing up, looking forward to develop.


#Here's the update function, it initializes the grid to all zeros first, cur.shape contains the information of the size
#of the grid, 0 is dimx and 1 is dimy
#The for loop iterates over each cell in the grid and calculates the number of alive cells based on the 2_layer
#Rules.

def update(surface, cur, sz):
    nxt = np.zeros((cur.shape[0], cur.shape[1]))

    for r, c in np.ndindex(cur.shape):
        #implement boundary with %, add feature that you can click, will save you a lot of time.
        weight_alive1 = np.sum(cur[r - 1:r + 2, c - 1:c + 2]) - cur[r, c]
        weight_alive2 = 0.25 * (np.sum(cur[r - 2:r + 3, c - 2:c + 3]) - np.sum(cur[r - 1:r + 2, c - 1:c + 2]))
        num_alive = weight_alive1 + weight_alive2
        #weight_alive3 = (1/8)*(np.sum(cur[r - 3:r + 4, c - 3:c + 4])- np.sum(cur[r - 2:r + 3, c - 2:c + 3]))
        #weight_alive4 = (1/16)*(np.sum(cur[r - 4:r + 5, c - 4:c + 5])- np.sum(cur[r - 3:r + 4, c - 3:c + 4]))
        #weight_alive5 = (1/25)*(np.sum(cur[r - 5:r + 6, c - 5:c + 6])- np.sum(cur[r - 4:r + 5, c - 4:c + 5]))
        #weight_alive6 = (1/36)*(np.sum(cur[r - 6:r + 7, c - 6:c + 7])- np.sum(cur[r - 5:r + 6, c - 5:c + 6]))

        if cur[r, c] == 1 and num_alive < 2.75 or num_alive > 4.5:
            col = col_alive
        elif (cur[r, c] == 1 and 2.75 <= num_alive <= 4.5) or (cur[r, c] == 0 and 3.25 <= num_alive <= 4.5):  # Pretty dope
            nxt[r, c] = 1
            col = col_alive

        col = col if cur[r, c] == 1 else col_background
        pygame.draw.rect(surface, col, (c * sz, r * sz, sz - 1, sz - 1))
#Here the population documents how many live cells are currently living.
    population = np.sum(cur[0:199, 0:199])
    y.append(population)
    print(population)
    return nxt

#Here's the initialization of patterns that are interesting, if you find more, you should add them here:)
def init(dimx, dimy):
    cells = np.zeros((dimy, dimx))
    #stable
    pos_atom = (0, 30)
    pos_egg = (0, 40)
    pos_shell = (0, 50)

    #oscillators
    pos_T = (10, 10)
    pos_Y = (10, 20)
    pos_Z = (10, 30)
    pos_star = (10, 40)
    pos_double = (10, 50)
    pos_prime = (10,60)
    pos_knot = (10,70)

    #gliders
    pos_turtle = (20, 10)
    pos_camel = (30, 10)
    pos_gun = (70, 30)

    oscillator_star = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_star[0]:pos_star[0] + oscillator_star.shape[0], pos_star[1]:pos_star[1] + oscillator_star.shape[1]] = oscillator_star
    #

    oscillator_prime = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_prime[0]:pos_prime[0] + oscillator_prime.shape[0],
    pos_prime[1]:pos_prime[1] + oscillator_prime.shape[1]] = oscillator_prime
    #

    oscillator_double = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_double[0]:pos_double[0] + oscillator_double.shape[0],
    pos_double[1]:pos_double[1] + oscillator_double.shape[1]] = oscillator_double
    #

    oscillator_knot = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                  [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_knot[0]:pos_knot[0] + oscillator_knot.shape[0],
    pos_knot[1]:pos_knot[1] + oscillator_knot.shape[1]] = oscillator_knot
    #

    oscillator_T = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_T[0]:pos_T[0] + oscillator_T.shape[0],
    pos_T[1]:pos_T[1] + oscillator_T.shape[1]] = oscillator_T
    #

    oscillator_Y = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_Y[0]:pos_Y[0] + oscillator_Y.shape[0],
    pos_Y[1]:pos_Y[1] + oscillator_Y.shape[1]] = oscillator_Y
    #

    oscillator_Z = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_Z[0]:pos_Z[0] + oscillator_Z.shape[0],
    pos_Z[1]:pos_Z[1] + oscillator_Z.shape[1]] = oscillator_Z
    #

    glider_turtle = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                              [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_turtle[0]:pos_turtle[0] + glider_turtle.shape[0],
    pos_turtle[1]:pos_turtle[1] + glider_turtle.shape[1]] = glider_turtle
    #

    glider_camel = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                             [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
                             [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_camel[0]:pos_camel[0] + glider_camel.shape[0],
    pos_camel[1]:pos_camel[1] + glider_camel.shape[1]] = glider_camel
    #

    stable_atom = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_atom[0]:pos_atom[0] + stable_atom.shape[0],
    pos_atom[1]:pos_atom[1] + stable_atom.shape[1]] = stable_atom
    #

    stable_egg = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_egg[0]:pos_egg[0] + stable_egg.shape[0],
    pos_egg[1]:pos_egg[1] + stable_egg.shape[1]] = stable_egg
    #

    stable_shell = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                             [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    cells[pos_shell[0]:pos_shell[0] + stable_shell.shape[0],
    pos_shell[1]:pos_shell[1] + stable_shell.shape[1]] = stable_shell
    #
    return cells


#Here's the main function, don't worry too much about this part.
def main(dimx, dimy, cellsize):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("More Layers Game of Life")
    cells = init(dimx, dimy)

    while True:
        global t
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        surface.fill(col_grid)
        cells = update(surface, cells, cellsize)
        pygame.display.update()

#In out.png you can check out the population graph of the game. You can add that manually yourself, and even change the
        #file name
        x = range(len(y))
        plt.plot(x, y)
        plt.savefig("out.png")

#This part is important(dimension x, dimension y, grid size,
# you can change the grid size to say (200,200,5) it's just a lot slower, also make sure you make
#the size compatible for your screen.
if __name__ == "__main__":
    main(100, 100, 11)


#In case you need to store data in a file
    # y = np.sum(cur[0:99, 0:99])
    # f = open("alright.txt", "w")
    # f.write(str(y))
    # f.close()
    # open and read the file after the appending:
    # f = open("alright.txt", "r")
    # print(f.read())


# Questions:Can you prove there's monovariant that forces the game to end in either still life or vaniish.
    # What's the game length bound?
    # Who are the players?
    # what periods of oscillators are possible to be constructued, conway's 19, not possible?
