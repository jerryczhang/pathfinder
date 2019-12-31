import numpy as np
import sys
import subprocess

class Display:

    def __init__(self, end_node):
        """Initialize the text blocks used for display, as well as the numpy array."""
        self.BLANK = "\033[40m  \033[0m"
        self.WALL = "\033[47m  \033[0m"
        self.CURR = "\033[40m[]\033[0m"
        self.START = "\033[42m  \033[0m"
        self.END = "\033[43m  \033[0m"
        self.PATH = "\033[40m::\033[0m"
        self.INVALID = "\033[40m><\033[0m"

        self.display = np.full((1, 1), self.BLANK)
        self.x_offset = 0
        self.y_offset = 0
        self.y_max, self.x_max = self.display.shape

        self.end_node = end_node

    def print_display(self):
        """Print the numpy array, which is the graphical representation of the maze."""
        subprocess.run("clear")
        for row in self.display:
            for item in row:
                sys.stdout.write(item)
            sys.stdout.write('\n')
        sys.stdout.write('\n')

    def expand(self, direction, num_tiles=1):
        """Expand the numpy array in a specified direction."""
        ysize, xsize = self.display.shape
        if direction == 'n':
            self.display = np.concatenate((np.full((2 * num_tiles, xsize), self.BLANK), self.display), axis=0)
            self.y_offset += 2 * num_tiles
        if direction == 'e':
            self.display = np.concatenate((self.display, np.full((ysize, 2 * num_tiles), self.BLANK)), axis=1)
        if direction == 's':
            self.display = np.concatenate((self.display, np.full((2 * num_tiles, xsize), self.BLANK)), axis=0)
        if direction == 'w':
            self.display = np.concatenate((np.full((ysize, 2 * num_tiles), self.BLANK), self.display), axis=1)
            self.x_offset += 2 * num_tiles
        self.y_max, self.x_max = self.display.shape

    def add_element(self, node, element, offset_dirs=''):
        """Add maze coordinates node to the display, offset in directions offset_dirs."""
        xcoor, ycoor = self.transform(node)
        if offset_dirs:
            if 'n' in offset_dirs:
                ycoor -= 1
            elif 's' in offset_dirs:
                ycoor += 1
            if 'e' in offset_dirs:
                xcoor += 1
            elif 'w' in offset_dirs:
                xcoor -= 1
        while xcoor > self.x_max - 1:
            self.expand('e')
        while ycoor > self.y_max - 1:
            self.expand('s')
        while xcoor < 0:
            self.expand('w')
            xcoor += 2
        while ycoor < 0:
            self.expand('n')
            ycoor += 2
        self.display[ycoor][xcoor] = element

    def transform(self, node):
        """Converts maze coordinates into array coordinates."""
        xtransform = 2 * node[0] + self.x_offset
        ytransform = 2 * node[1] + self.y_offset
        return xtransform, ytransform

    def update_display(self, maze, curr_node, path, invalid):
        """Update the graphical array."""
        self.add_element(self.end_node, self.END)
        for direction in maze[curr_node]:
            if maze[curr_node][direction] == "invalid":
                self.add_element(curr_node, self.WALL, direction)
        for offset_dir in ['ne', 'se', 'sw', 'nw']:
            self.add_element(curr_node, self.WALL, offset_dir)
        for node in maze:
            if node == curr_node:
                self.add_element(node, self.CURR)
            elif node == path[0]:
                self.add_element(node, self.START)
            elif node in path:
                self.add_element(node, self.PATH)
            elif node in invalid:
                self.add_element(node, self.INVALID)
            else:
                self.add_element(node, self.BLANK)
