import pygame
import numpy as np
import time

pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

# Number of cells for each axis
nxC, nyC = 50, 50

# Dimension of ceach cell (height and width)
dimCW = width / nxC
dimCH = height / nyC

# Table with the state of each cell; 0 -> Dead - 1 -> Alive
game_state = np.zeros((nxC, nyC))

# Automata palo
# game_state[5, 3] = 1
# game_state[5, 4] = 1
# game_state[5, 5] = 1

game_state[21, 21] = 1
game_state[22, 22] = 1
game_state[22, 23] = 1
game_state[21, 23] = 1
game_state[20, 23] = 1

# Execution control
pause_exec = True

def get_alive_neighbour_count(posX, posY, matrix):
    alive = matrix[(x-1) % nxC, (y-1) % nyC] + \
            matrix[(x) % nxC, (y-1) % nyC] + \
            matrix[(x+1) % nxC, (y-1) % nyC] + \
            matrix[(x-1) % nxC, (y) % nyC] + \
            matrix[(x+1) % nxC, (y) % nyC] + \
            matrix[(x-1) % nxC, (y+1) % nyC] + \
            matrix[(x) % nxC, (y+1) % nyC] + \
            matrix[(x+1) % nxC, (y+1) % nyC]
    return alive

while True:
    new_game_state = np.copy(game_state)
    screen.fill(bg)
    time.sleep(0.1)

    # Register keyboard events
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:
            pause_exec = not pause_exec

    mouse_click = pygame.mouse.get_pressed()
    # Here we have a tuple with the button pressed represented with 1 value
    if sum(mouse_click) > 0:
        posX, posY = pygame.mouse.get_pos()
        cellX, cellY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
        # 'Kills' a cell is mouse click with second or central button
        new_game_state[cellX, cellY] = not mouse_click[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pause_exec:
                # Get number of adjacent alive cells
                count_alive = get_alive_neighbour_count(x, y, game_state)

                if game_state[x, y] == 1 and (count_alive == 3 or count_alive == 2):
                    # Rule 1: Any live cell with two or three live neighbors survives
                    new_game_state[x, y] = 1
                elif game_state[x, y] == 0 and count_alive == 3:
                    # Rule 2: Any dead cell with three live neighbors becomes a live cell
                    new_game_state[x, y] = 1
                else:
                    # Rule 3: All other live cells die in the next generation. Similarly, all other dead cells stay dead.
                    new_game_state[x, y] = 0

            cell_color = (128, 128, 128)
            cell_border_width = 1

            if new_game_state[x, y] == 1:
                cell_color = (255, 255, 255)
                cell_border_width = 0

            # Define each cell coordinate
            cell = [
                (x          * dimCW, y          * dimCH),
                ((x + 1)    * dimCW, y          * dimCH),
                ((x + 1)    * dimCW, (y + 1)    * dimCH),
                (x          * dimCW, (y + 1)    * dimCH)
            ]
            # Draw the grid in the screen, with a cell color and the cell coordinates
            pygame.draw.polygon(screen, cell_color, cell, cell_border_width)

    # Update the game state with the calculated new one
    game_state = np.copy(new_game_state)

    # Update the screen
    pygame.display.flip()