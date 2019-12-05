#TODO refactor, documentation, array display
from color import add_color
from random import randrange
from time import sleep
import sys

def construct_maze():
    """Constructs a 10 by 10 array representation of the blank maze."""
    row = []
    array = []
    for _ in range(1, 10):
        blank = str(add_color(' ', "Black", highlight = True))
        row.append(blank)
    for _ in range(1, 10):
        array.append(list(row))
    return array

def print_array(array):
    """Print the maze in graphical form with color formatting."""
    for row in array:
        for item in row:
            sys.stdout.write(item)
        sys.stdout.write('\n')

def print_maze(maze, start, path):
    """Print the text representation of the maze.""" 
    print(''.center(20, '='))
    print("Current Node: " + str(start))
    for key, value in maze.items():
        print(str(key) + ' : ' + str(value))
    print("invalid Nodes: " + str(invalid))
    print("path: " + str(path))

def move(position, robot_pos):
    """Moves the robot to position from robot_pos."""
    xdist = position[0] - robot_pos[0]
    ydist = position[1] - robot_pos[1]
    if xdist >= 2 or ydist >= 2:
        return
    else:
        robot_pos[0] += xdist
        robot_pos[1] += ydist
        print("Robot position: " + str(robot_pos))

def reverse(direction):
    """reverse the given compass direction (n, e, s, w)."""
    directions = ['n', 'e', 's', 'w', 'n', 'e', 's', 'w']
    return directions[directions.index(direction) + 2]

def random_success(rate):
    """Returns true with the frequency provided by rate."""
    return randrange(100) <= rate * 100

def get_end(manual_input=False, success_rate=0.01):
    """Get input for whether the robot is at the end of the maze."""
    if manual_input:
        return input("End? (T/F):").lower() == 't'
    else:
        return random_success(success_rate)

def scan(direction, manual_input=False, sensor_input=False, success_rate=0.4):
    """Get input for whether a direction is valid. Can be manual or sensor input, or random."""
    if sensor_input:
        input("Scan " + direction)
        return distances.get_distance() >= 10
    elif manual_input:
        return input(direction + " valid (T/F):").lower() == 't'
    else:
        return random_succeses(success_rate)
    
def find_path(maze, start, invalid, robot_pos, path=[]):
    """Recursively iterate through maze nodes, constructing and solving a graph.

    Parameters:
        maze:       The nested dictionary which contains the tuple coordinates of each node
                    as the keys, and a dictionary which contains information about
                    adjacent nodes
        start:      The starting node of the maze--this represents the current node with
                    each recursive call
        invalid:    The list containing all nodes that lead to dead-ends 
        robot_pos:  The current position of the physical robot
        path:       The list of nodes that the robot has traveled through

    Returns:
        The path to the end of the maze, if it exists, and None otherwise
    """
    path = path + [start]
    print_array(array)
    print_maze(maze, start, path)
    move(path[-1], robot_pos)
    if get_end(manual_input=True):
        return path 
    if len(path) >= 2 and path[-1] == path[-2]:
        invalid.append(path.pop())
        if len(path) >= 2:
            move(path[-2], robot_pos)
        return

    for direction in maze[start]:
        nearby_node = maze[start][direction]
        if not nearby_node:
            nearby_node_x = start[0]
            nearby_node_y = start[1]
            valid = scan(direction, manual_input=True)
            if direction == 'n' and start[1] == 13:
                valid = False
            elif direction == 'e' and start[0] == 13:
                valid = False
            elif direction == 's' and start[1] == 10:
                valid = False
            elif direction == 'w' and start[0] == 10:
                valid = False
            #get coordinates for nearby nodes
            if valid == True:
                if direction == 'n':
                    nearby_node_y += 1
                elif direction == 'e':
                    nearby_node_x += 1
                elif direction == 's':
                    nearby_node_y -= 1
                elif direction == 'w':
                    nearby_node_x -= 1
                nearby_node = (nearby_node_x, nearby_node_y)
                maze[start][direction] = nearby_node
                empty = {'n': False, 'e': False, 's': False, 'w': False, reverse(direction): path[-1]}
                #create new node
                maze[nearby_node] = empty
                #update array
                array_x = {10:1, 11:3, 12:5, 13:7}
                array_y = {10:7, 11:5, 12:3, 13:1}
                array_coor_x = array_x[start[0]]
                array_coor_y = array_y[start[1]]
                if len(path) > 1:
                    prev_array_x = array_x[path[-2][0]]
                    prev_array_y = array_y[path[-2][1]]
                    array[prev_array_y][prev_array_x] = add_color(' ', "Yellow", highlight = True)
                    array[array_coor_y][array_coor_x] = add_color(' ', "Green", highlight = True)
                for direction in maze[start]:
                    if maze[start][direction] == False:
                        wall = add_color(' ', "Red", highlight  = True)
                    else:
                        wall = add_color(' ', "Teal", highlight = True)
                    if direction == 'n':
                        array[array_coor_y - 1][array_coor_x] = wall
                    elif direction == 'e':
                        array[array_coor_y][array_coor_x + 1] = wall
                    elif direction == 's':
                        array[array_coor_y + 1][array_coor_x] = wall
                    elif direction == 'w':
                        array[array_coor_y][array_coor_x - 1] = wall    
    #find next
    for direction in maze[start]:
        if maze[start][direction] and maze[start][direction] not in path and maze[start][direction] not in invalid:
            newpath = find_path(maze, maze[start][direction], invalid, robot_pos, path)
            if newpath:
                return newpath
    return None

array = construct_maze()
maze = {(10, 10):
    {
        'n': False,
        'e': False,
        's': False,
        'w': False,
    }
}
invalid = []
path = find_path(maze, (10,10), invalid, [10, 10])
print("=======================")
if path:
    print("Finished, path: " + str(path))
else:
    print("Impossible maze")

#Solve Second Time
"""input("Ready?")
RobotPos = [10,10]
for Tile in path:
    Move(Tile, RobotPos)"""
