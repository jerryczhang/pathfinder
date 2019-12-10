import interface
from random import randrange
from time import sleep

MANUAL_INPUT = False
SENSOR_INPUT = False
RANDOM_INPUT = True

def move(position, robot_pos):
    """Moves the robot to position from robot_pos."""
    xdist = position[0] - robot_pos[0]
    ydist = position[1] - robot_pos[1]
    robot_pos[0] += xdist
    robot_pos[1] += ydist
    print("Robot position: " + str(robot_pos))

def reverse(direction):
    """Reverses the given compass direction (n, e, s, w)."""
    directions = ['n', 'e', 's', 'w', 'n', 'e', 's', 'w']
    return directions[directions.index(direction) + 2]

def random_success(rate):
    """Returns true with the frequency provided by rate."""
    return randrange(100) <= rate * 100

def get_end(path, maze, success_rate=0.01):
    """Get input for whether the robot is at the end of the maze."""
    if MANUAL_INPUT or SENSOR_INPUT:
        return input("End? (T/F):").lower() == 't'
    else:
        sleep(0.1)
        return random_success(success_rate)

def scan(direction, manual_input=False, sensor_input=False, success_rate=0.4):
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
        adj[1] -= 1
    elif direction == 'e':
        adj[0] += 1
    elif direction == 's':
        adj[1] += 1
    elif direction == 'w':
        adj[0] -= 1
    return tuple(adj) 
    
def find_path(maze, start, robot_pos, path, display):
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
    display.update_display(path, maze)
    display.print_display()
    move(path[-1], robot_pos)
    if get_end(path, maze):
        return path 

    for direction in maze[start]:
        if maze[start][direction] == "unknown":
            adj = get_nearby_node(direction, start)
            if adj not in maze or maze[adj][reverse(direction)] == "unknown":
                valid = scan(direction, manual_input = MANUAL_INPUT, sensor_input = SENSOR_INPUT)
                if valid:
                    maze[start][direction] = adj
                    maze[adj] = {
                            'n': "unknown", 
                            'e': "unknown", 
                            's': "unknown", 
                            'w': "unknown", 
                            reverse(direction): path[-1]
                    }
                else:
                    maze[start][direction] = "invalid"
            elif maze[adj][reverse(direction)] == "invalid":
                maze[start][direction] = "invalid"
            else:
                maze[start][direction] = adj
            display.update_display(path, maze)
    for direction in maze[start]:
        if maze[start][direction] != "invalid" and maze[start][direction] not in path:
            newpath = find_path(maze, maze[start][direction], robot_pos, path, display)
            if newpath:
                return newpath
            else:
                move(path[-1], robot_pos)
    return None

def main():
    """Initializes maze and display, then calls find_path."""
    display = interface.Display()
    maze = {(0, 0):
        {
            'n': "unknown",
            'e': "unknown",
            's': "unknown",
            'w': "unknown",
        }
    }
    path = find_path(maze, (0,0), [0, 0], [], display)
    print(''.center(20, '='))
    if path:
        print("Finished, path: " + str(path))
    else:
        print("Impossible maze")

if __name__ == '__main__':
    main()
