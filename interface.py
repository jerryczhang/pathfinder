#TODO implement numpy array, unicode formatting
from color import add_color
import numpy as np
import sys

BLANK = "\033[40m  \033[0m"
WALL = "\033[47m  \033[0m"

def construct_display():
    """Constructs a 10 by 10 display representation of the blank maze."""
    display = np.full((9,9), BLANK)
    return display 

def print_display(display):
    """Print the maze in graphical form with color formatting."""
    for row in display:
        for item in row:
            sys.stdout.write(item)
        sys.stdout.write('\n')

def print_maze(maze, start, path):
    """Print the text representation of the maze.""" 
    print(''.center(20, '='))
    print("Current Node: " + str(start))
    for key, value in maze.items():
        print(str(key) + ' : ' + str(value))
    print("path: " + str(path))

def update_display(maze, start, path, display):
    """Update the graphical array."""
    display_x = {10:1, 11:3, 12:5, 13:7}
    display_y = {10:7, 11:5, 12:3, 13:1}
    display_coor = (display_x[start[0]], display_y[start[1]])
    for direction in maze[start]:
        if maze[start][direction] == "invalid":
            if direction == 'n':
                display[display_coor[1] - 1][display_coor[0]] = WALL
            elif direction == 'e':
                display[display_coor[1]][display_coor[0] + 1] = WALL
            elif direction == 's':
                display[display_coor[1] + 1][display_coor[0]] = WALL
            elif direction == 'w':
                display[display_coor[1]][display_coor[0] - 1] = WALL 
    for x in [-1, 1]:
        for y in [-1, 1]:
            display[display_coor[1]+x][display_coor[0]+y] = WALL
