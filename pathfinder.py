import interface
from random import randint
from time import sleep

MANUAL = 0
RANDOM = 1
SENSOR = 2
FULL   = 3

class PathfinderBot:
    """Represents the pathfinder bot.""" 

    def __init__(self, mode, start_node, end_node):
        """Initializes the robot.

        Parameters:
            mode: The operating mode of the robot--can be MANUAL, RANDOM, SENSOR, or FULL
            start_node: The node where the robot is starting
            end_node: The target node of the maze that the robot is reaching

        """
        self.mode = mode
        self.robot_pos = list(start_node)
        self.start_node = start_node
        self.end_node = end_node
        
        self.solution = []
        self.invalid = []
        self.display = interface.Display(end_node)
        self.maze = {start_node:
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

    def get_directions(self, node):
        """Return directions sorted such that directions toward end_node are prioritized."""
        x_dist = self.end_node[0] - node[0]
        y_dist = self.end_node[1] - node[1]
        if y_dist > 0:
            y_dirs = ['s', 'n']
        else:
            y_dirs = ['n', 's']
        if x_dist > 0:
            x_dirs = ['e', 'w'] 
        else:
            x_dirs = ['w', 'e']
        if abs(y_dist) > abs(x_dist):
            y_dirs[1:1] = x_dirs
            return y_dirs
        else:
            x_dirs[1:1] = y_dirs
            return x_dirs

    def update_surroundings(self, node):
        """Scan surrounding nodes and update maze accordingly."""
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
                                self.reverse(direction): node
                        }
                    else:
                        self.maze[node][direction] = "invalid"
                elif self.maze[adj][self.reverse(direction)] == "invalid":
                    self.maze[node][direction] = "invalid"
                else:
                    self.maze[node][direction] = adj

    def find_path(self, node=None, path=[]):
        """Recursively iterate through maze nodes, constructing and solving a graph."""
        if node == None:
            node = self.start_node
        if self.mode == RANDOM:
            sleep(0.1)
        path = path + [node]
        self.move(path[-1])
    
        self.display.update_display(self.maze, path, self.invalid)
        self.display.print_display()
        self.update_surroundings(node)
        self.display.update_display(self.maze, path, self.invalid)
        
        if node == self.end_node or node in self.solution:
            return path 

        for direction in self.get_directions(node):
            if (
                self.maze[node][direction] != "invalid" 
                and self.maze[node][direction] not in path 
                and self.maze[node][direction] not in self.invalid
            ):
                next_node = self.maze[node][direction]
                new_path = self.find_path(next_node, path)
                if new_path:
                    return new_path
                else:
                    self.invalid.append(self.maze[node][direction])
                    self.move(path[-1])
        self.display.print_display()
        return None

    def second_solve(self, solution):
        """Finds the way out of the maze starting from a new location."""
        if self.mode == MANUAL:
            x_start = int(input("Enter x coordinate of new start: "))
            y_start = int(input("Enter y coordinate of new start: "))
            new_start = (x_start, y_start)
        else:
            new_start = (0, 0)
        self.invalid = []
        self.solution = solution
        path = self.find_path(node=new_start)
        path_index = solution.index(path[-1]) + 1
        return path + solution[path_index:]

def main():
    """Initializes robot and finds path."""
    pathfinder = PathfinderBot(RANDOM, (0, 0), (3, -3))
    path = pathfinder.find_path()
    if path:
        print("Finished, path: " + str(path))
        print(pathfinder.second_solve(path))
    else:
        print("Impossible maze")

if __name__ == '__main__':
    main()
