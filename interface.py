import numpy as np
import sys

class Display:

    def __init__(self):
        """Initialize the text blocks used for display, as well as the np array."""
        self.BLANK = "\033[40m  \033[0m"
        self.WALL = "\033[47m  \033[0m"
        self.CURR = "\033[40m[]\033[0m"
        self.START = "\033[40m<>\033[0m"
        self.PATH = "\033[40m::\033[0m"
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
        """Expand the np array in a specified direction."""
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

    def add_element(self, node, element, offset_dirs=None):
        """Add maze coordinates node to the display, offset in directions offset_dirs."""
        x, y = self.transform(node)
        if offset_dirs:
            if 'n' in offset_dirs:
                y -= 1
            elif 's' in offset_dirs:
                y += 1
            if 'e' in offset_dirs:
                x += 1
            elif 'w' in offset_dirs:
                x -= 1
        if x > self.display.shape[1] - 1:
            self.expand('e')
        if y > self.display.shape[0] - 1:
            self.expand('s')
        if x < 0:
            self.expand('w')
            x += 2
        if y < 0:
            self.expand('n')
            y += 2
        self.display[y][x] = element

    def transform(self, node):
        """Converts maze coordinates into array coordinates."""
        xt = 2 * node[0] + self.x_offset
        yt = 2 * node[1] + self.y_offset
        return xt, yt

    def update_display(self, path, maze):
        """Update the graphical array."""
        curr_node = path[-1]
        for direction in maze[curr_node]:
            if maze[curr_node][direction] == "invalid":
                self.add_element(curr_node, self.WALL, direction)
        for offset_dir in ['ne', 'se', 'sw', 'nw']:
            self.add_element(curr_node, self.WALL, offset_dir)
        for node in maze:
            if node == path[0]:
                self.add_element(node, self.START)
            elif node == path[-1]:
                self.add_element(node, self.CURR)
            elif node in path:
                self.add_element(node, self.PATH)
            else:
                self.add_element(node, self.BLANK)
