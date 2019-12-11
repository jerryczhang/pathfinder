import interface
from random import randint
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

def reverse(direction):
    """Reverses the given compass direction (n, e, s, w)."""
    directions = ['n', 'e', 's', 'w', 'n', 'e', 's', 'w']
    return directions[directions.index(direction) + 2]

def random_success(rate):
    """Returns true with the frequency provided by rate."""
    return randint(1, 100) <= rate * 100

def get_end():
    xend = input("Enter x-coordinate of end: ")
    yend = input("Enter y-coordinate of end: ")
    return (int(xend), int(yend))

def scan(direction, success_rate=0.4):
    """Get input for whether a direction is valid. Can be manual or sensor input, or random."""
    if SENSOR_INPUT:
        input("Scan " + direction)
        return distances.get_distance() >= 10
    elif MANUAL_INPUT:
        return input(direction + " valid (T/F):").lower() == 't'
    else:
        return random_success(success_rate)

def get_nearby_node(current_node, direction):
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

def find_path(maze, start, end, robot_pos, display, path=[], invalid=[]):
    """Recursively iterate through maze nodes, constructing and solving a graph.

    Parameters:
        maze:       The nested dictionary which contains the tuple coordinates of each node
                    as the keys, and a dictionary which contains information about
                    adjacent nodes
        start:      The starting node of the maze--this represents the current node with
                    each recursive call
        robot_pos:  The current position of the physical robot
        path:       The list of nodes that the robot has traveled through
        display:    The display containing the graphical representation of the maze

    Returns:
        The path to the end of the maze, if it exists, or None otherwise
    """
    if RANDOM_INPUT:
        sleep(0.1)
    path = path + [start]
    display.update_display(maze, path, invalid)
    display.print_display()
    move(path[-1], robot_pos)
    if start == end:
        return path 

    for direction in maze[start]:
        if maze[start][direction] == "unknown":
            adj = get_nearby_node(start, direction)
            if adj not in maze or maze[adj][reverse(direction)] == "unknown":
                valid = scan(direction)
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
    display.update_display(maze, path, invalid)
    for direction in maze[start]:
        if (
            maze[start][direction] != "invalid" 
            and maze[start][direction] not in path 
            and maze[start][direction] not in invalid
        ):
            newpath = find_path(maze, maze[start][direction], end, robot_pos, display, path, invalid)
            if newpath:
                return newpath
            else:
                invalid.append(maze[start][direction])
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
    path = find_path(maze, (0,0), get_end(), [0, 0], display)

    print(''.center(20, '='))
    if path:
        print("Finished, path: " + str(path))
    else:
        print("Impossible maze")

if __name__ == '__main__':
    main()
