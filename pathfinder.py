#TODO array display, spatial awareness
from color import add_color
from random import randrange
from time import sleep
import sys
import enum

MANUAL_INPUT = True
SENSOR_INPUT = False
RANDOM_INPUT = False

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

def get_end(manual_input=False, sensor_input=False, success_rate=0.01):
    """Get input for whether the robot is at the end of the maze."""
    if manual_input or sensor_input:
        return input("End? (T/F):").lower() == 't'
    else:
        return random_success(success_rate)

def scan(direction, manual_input=False, sensor_input=False, success_rate=0.75):
    """Get input for whether a direction is valid. Can be manual or sensor input, or random."""
    if sensor_input:
        input("Scan " + direction)
        return distances.get_distance() >= 10
    elif manual_input:
        return input(direction + " valid (T/F):").lower() == 't'
    else:
        return random_success(success_rate)

def get_nearby_node(direction, current_node):
    """Get the coordinates of the adjacent node."""
    adj = list(current_node)
    if direction == 'n':
        adj[1] += 1
    elif direction == 'e':
        adj[0] += 1
    elif direction == 's':
        adj[1] -= 1
    elif direction == 'w':
        adj[0] -= 1
    return tuple(adj) 
    
def update_array(maze, start, path, array):
    """Update the graphical array."""
    array_x = {10:1, 11:3, 12:5, 13:7}
    array_y = {10:7, 11:5, 12:3, 13:1}
    array_coor = (array_x[start[0]], array_y[start[1]])
    for direction in maze[start]:
        if maze[start][direction] == "invalid":
            wall = add_color(' ', "Red", highlight  = True)
        else:
            wall = add_color(' ', "Teal", highlight = True)
        if direction == 'n':
            array[array_coor[1] - 1][array_coor[0]] = wall
        elif direction == 'e':
            array[array_coor[1]][array_coor[0] + 1] = wall
        elif direction == 's':
            array[array_coor[1] + 1][array_coor[0]] = wall
        elif direction == 'w':
            array[array_coor[1]][array_coor[0] - 1] = wall    

def find_path(maze, start, robot_pos, path, array):
    """Recursively iterate through maze nodes, constructing and solving a graph.

    Parameters:
        maze:       The nested dictionary which contains the tuple coordinates of each node
                    as the keys, and a dictionary which contains information about
                    adjacent nodes
        start:      The starting node of the maze--this represents the current node with
                    each recursive call
        robot_pos:  The current position of the physical robot
        path:       The list of nodes that the robot has traveled through

    Returns:
        The path to the end of the maze, if it exists, and None otherwise
    """
    path = path + [start]
    print_array(array)
    print_maze(maze, start, path)
    move(path[-1], robot_pos)
    if get_end(manual_input=MANUAL_INPUT, sensor_input=SENSOR_INPUT):
        return path 

    for direction in maze[start]:
        nearby_node = maze[start][direction]
        if nearby_node == "unknown":
            valid = scan(direction, manual_input = MANUAL_INPUT, sensor_input = SENSOR_INPUT)
            if valid:
                adj = get_nearby_node(direction, start)
                maze[start][direction] = adj
                if adj not in maze:
                    maze[adj] = {
                            'n': "unknown", 
                            'e': "unknown", 
                            's': "unknown", 
                            'w': "unknown", 
                            reverse(direction): path[-1]
                    }
            else:
                maze[start][direction] = "invalid"
        update_array(maze, start, path, array)
    for direction in maze[start]:
        if maze[start][direction] != "invalid" and maze[start][direction] not in path:
            newpath = find_path(maze, maze[start][direction], robot_pos, path, array)
            if newpath:
                return newpath
            else:
                move(path[-1], robot_pos)
    return None

def main():
    """Initializes maze and array, then calls find_path."""
    array = construct_maze()
    maze = {(10, 10):
        {
            'n': "unknown",
            'e': "unknown",
            's': "unknown",
            'w': "unknown",
        }
    }
    path = find_path(maze, (10,10), [10, 10], [], array)
    print(''.center(20, '='))
    if path:
        print("Finished, path: " + str(path))
    else:
        print("Impossible maze")

if __name__ == '__main__':
    main()
