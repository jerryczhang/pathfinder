import interface
from random import randint
from time import sleep

MANUAL = 0
RANDOM = 1
SENSOR = 2
FULL   = 3

class PathfinderBot:
    """Represents the pathfinder bot.""" 

    def __init__(self, mode, end_node):
        self.mode = mode
        self.robot_pos = [0,0] 
        self.end_node = end_node
        
        self.invalid = []
        self.display = interface.Display()
        self.maze = {(0, 0):
            {
                'n': "unknown",
                'e': "unknown",
                's': "unknown",
                'w': "unknown",
            }
        }

    def move(self, position):
        """Moves the robot to position from robot_pos."""
        if self.mode == FULL:
            pass
        self.robot_pos = position

    def reverse(self, direction):
        """Reverses the given compass direction (n, e, s, w)."""
        directions = ['n', 'e', 's', 'w', 'n', 'e', 's', 'w']
        return directions[directions.index(direction) + 2]

    def random_success(self, rate):
        """Returns true with the frequency provided by rate."""
        return randint(1, 100) <= rate * 100

    def scan(self, direction, success_rate=0.4):
        """Get input for whether a direction is valid. Can be manual or sensor input, or random."""
        if self.mode == SENSOR or self.mode == FULL:
            input("Scan " + direction)
            return distances.get_distance() >= 10
        elif self.mode == MANUAL:
            return input(direction + " valid (T/F):").lower() == 't'
        else:
            return self.random_success(success_rate)

    def get_nearby_node(self, node, direction):
        """Get the coordinates of the adjacent node."""
        adj = list(node)
        if direction == 'n':
            adj[1] -= 1
        elif direction == 'e':
            adj[0] += 1
        elif direction == 's':
            adj[1] += 1
        elif direction == 'w':
            adj[0] -= 1
        return tuple(adj) 

    def find_path(self, node=(0,0), path=[]):
        """Recursively iterate through maze nodes, constructing and solving a graph.

        Parameters:
            path:       The list of nodes that the robot has traveled through

        Returns:
            The path to the end of the maze, if it exists, or None otherwise
        """
        if self.mode == RANDOM:
            sleep(0.1)
        path = path + [node]
        self.display.update_display(self.maze, path, self.invalid)
        self.display.print_display()
        self.move(path[-1])
        if node == self.end_node:
            return path 

        for direction in self.maze[node]:
            if self.maze[node][direction] == "unknown":
                adj = self.get_nearby_node(node, direction)
                if adj not in self.maze or self.maze[adj][self.reverse(direction)] == "unknown":
                    valid = self.scan(direction)
                    if valid:
                        self.maze[node][direction] = adj
                        self.maze[adj] = {
                                'n': "unknown", 
                                'e': "unknown", 
                                's': "unknown", 
                                'w': "unknown", 
                                self.reverse(direction): path[-1]
                        }
                    else:
                        self.maze[node][direction] = "invalid"
                elif self.maze[adj][self.reverse(direction)] == "invalid":
                    self.maze[node][direction] = "invalid"
                else:
                    self.maze[node][direction] = adj
        self.display.update_display(self.maze, path, self.invalid)
        for direction in self.maze[node]:
            if (
                self.maze[node][direction] != "invalid" 
                and self.maze[node][direction] not in path 
                and self.maze[node][direction] not in self.invalid
            ):
                node = self.maze[node][direction]
                new_path = self.find_path(node, path)
                if new_path:
                    return new_path
                else:
                    self.invalid.append(self.maze[node][direction])
                    self.move(path[-1])
        return None

def main():
    """Initializes maze and display, then calls find_path."""

    pathfinder = PathfinderBot(MANUAL, (10, 10))
    path = pathfinder.find_path()
    print(''.center(20, '='))
    if path:
        print("Finished, path: " + str(path))
    else:
        print("Impossible maze")

if __name__ == '__main__':
    main()
