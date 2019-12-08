#TODO implement numpy array, unicode formatting
from color import add_color
import numpy as np
import sys

class Display:

    def __init__(self):
        self.BLANK = "\033[40m  \033[0m"
        self.WALL = "\033[47m  \033[0m"
        self.CURR = "\033[40m[]\033[0m"
        self.display = np.full((3, 3), self.BLANK)
        self.x_offset = 1
        self.y_offset = 1

    def print_display(self):
        """Print the maze in graphical form with color formatting."""
        for row in self.display:
            for item in row:
                sys.stdout.write(item)
            sys.stdout.write('\n')

    def expand(self, direction):
        (y, x) = self.display.shape
        if direction == 'n':
            self.display = np.concatenate((np.full((2, x), self.BLANK), self.display), axis=0)
            self.y_offset += 2
        if direction == 'e':
            self.display = np.concatenate((self.display, np.full((y, 2), self.BLANK)), axis=1)
        if direction == 's':
            self.display = np.concatenate((self.display, np.full((2, x), self.BLANK)), axis=0)
        if direction == 'w':
            self.display = np.concatenate((np.full((y, 2), self.BLANK), self.display), axis=1)
            self.x_offset += 2

    def transform(self, node):
        xt = 2 * node[0] + self.x_offset
        yt = 2 * node[1] + self.y_offset
        return xt, yt

    def update_display(self, path, maze):
        """Update the graphical array."""
        x, y = self.transform(path[-1])
        if x >= self.display.shape[1] - 1:
            self.expand('e')
        if y >= self.display.shape[0] - 1:
            self.expand('s')
        if x <= 0:
            self.expand('w')
            x += 2
        if y <= 0:
            self.expand('n')
            y += 2
        for direction in maze[path[-1]]:
            if maze[path[-1]][direction] == "invalid":
                if direction == 'n':
                    self.display[y-1][x] = self.WALL
                elif direction == 'e':
                    self.display[y][x+1] = self.WALL
                elif direction == 's':
                    self.display[y+1][x] = self.WALL
                elif direction == 'w':
                    self.display[y][x-1] = self.WALL 
        self.display[y][x] = self.CURR
        if len(path) >= 2:
            x_prev, y_prev = self.transform(path[-2])
            self.display[y_prev][x_prev] = self.BLANK
            for x1 in [-1, 1]:
                for y1 in [-1, 1]:
                    self.display[y_prev + y1][x_prev + x1] = self.WALL
def print_maze(maze, start, path):
    """Print the text representation of the maze.""" 
    print(''.center(20, '='))
    print("Current Node: " + str(start))
    for key, value in maze.items():
        print(str(key) + ' : ' + str(value))
    print("path: " + str(path))
