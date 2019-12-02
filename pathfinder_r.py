#TODO fix naming and spacing
from color import add_color
from random import randint
from time import sleep
import sys

def construct_maze():
    """Constructs a 10 by 10 array representation of the blank maze."""
    row = []
    array = []
    for _ in range(1, 10):
        blank = str(add_color(" ", "Black", highlight = True))
        row.append(blank)
    for _ in range(1, 10):
        array.append(list(row))
    return array

def print_array(array):
    """Print out the array with color formatting."""
    for row in array:
        for item in row:
            sys.stdout.write(item)
        sys.stdout.write('\n')

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
    """Reverse the given compass direction (n, e, s, w)."""
    directions = ['n', 'e', 's', 'w', 'n', 'e', 's', 'w']
    return directions[directions.index(direction) + 2]

def FindPath(Maze, Start, Invalid, RobotPos, Path=[]):
    def RandomInput(SuccessRate):
        Number = randint(1, 100)
        if Number <= SuccessRate:
            return 't'
        else:
            return 'f'
    for Node in Maze[Start]:
        sleep(0.5)
        Path = Path + [Start]
        #start printing info
        PrintArray()
        print("==========")
        print("Current Node: " + str(Start))
        """for Key, Value in Maze.items():
            print(str(Key) + ' : ' + str(Value))"""
        print("Invalid Nodes: " + str(Invalid))
        print("Path: " + str(Path))
        #end print info
        Move(Path[-1], RobotPos)
        #check if end
        """End = input("End? (T/F):").lower()"""
        End = RandomInput(1)
        if End == 't':
            return Path
        #check if deadend
        if len(Path) >= 2 and Path[-1] == Path[-2]:
            Invalid.append(Path.pop())
            if len(Path) >= 2:
                Move(Path[-2], RobotPos)
            break
        #get surrounding nodes
        for Direction in Maze[Start]:
            NearbyNode = Maze[Start][Direction]
            if not NearbyNode:
                NearbyNodeX = Start[0]
                NearbyNodeY = Start[1]
                """input("Scan " + Direction)
                Distance = Distances.GetDistance()
                if Distance >= 10:
                    Valid = 't'
                else:
                    Valid = 'f'"""
                """Valid = input(Direction + " valid (T/F):").lower()"""
                #random input
                Valid = RandomInput(75)
                if Direction == 'n' and Start[1] == 13:
                    Valid = 'f'
                elif Direction == 'e' and Start[0] == 13:
                    Valid = 'f'
                elif Direction == 's' and Start[1] == 10:
                    Valid = 'f'
                elif Direction == 'w' and Start[0] == 10:
                    Valid = 'f'
                #get coordinates for nearby nodes
                if Valid == 't':
                    if Direction == 'n':
                        NearbyNodeY += 1
                    elif Direction == 'e':
                        NearbyNodeX += 1
                    elif Direction == 's':
                        NearbyNodeY -= 1
                    elif Direction == 'w':
                        NearbyNodeX -= 1
                    NearbyNode = (NearbyNodeX, NearbyNodeY)
                    Maze[Start][Direction] = NearbyNode
                    Empty = {'n': False, 'e': False, 's': False, 'w': False, Reverse(Direction): Path[-1]}
                    #create new node
                    Maze[NearbyNode] = Empty
                    #update array
                    ArrayX = {10:1, 11:3, 12:5, 13:7}
                    ArrayY = {10:7, 11:5, 12:3, 13:1}
                    ArrayCoorX = ArrayX[Start[0]]
                    ArrayCoorY = ArrayY[Start[1]]
                    if len(Path) > 1:
                        PrevArrayX = ArrayX[Path[-2][0]]
                        PrevArrayY = ArrayY[Path[-2][1]]
                        Array[PrevArrayY][PrevArrayX] = AddColor(" ", "Yellow", Highlight = True)
                        Array[ArrayCoorY][ArrayCoorX] = AddColor(" ", "Green", Highlight = True)
                    for Direction in Maze[Start]:
                        if Maze[Start][Direction] == False:
                            Wall = AddColor(" ", "Red", Highlight  = True)
                        else:
                            Wall = AddColor(" ", "Teal", Highlight = True)
                        if Direction == 'n':
                            Array[ArrayCoorY - 1][ArrayCoorX] = Wall
                        elif Direction == 'e':
                            Array[ArrayCoorY][ArrayCoorX + 1] = Wall
                        elif Direction == 's':
                            Array[ArrayCoorY + 1][ArrayCoorX] = Wall
                        elif Direction == 'w':
                            Array[ArrayCoorY][ArrayCoorX - 1] = Wall    
        #find next
        for Direction in Maze[Start]:
            if Maze[Start][Direction] and Maze[Start][Direction] not in Path and Maze[Start][Direction] not in Invalid:
                NewPath = FindPath(Maze, Maze[Start][Direction], Invalid, RobotPos, Path)
                if NewPath:
                    return NewPath
    return None

Maze = {(10, 10):
    {
        'n': False,
        'e': False,
        's': False,
        'w': False,
    }
}
Invalid = []
Path = FindPath(Maze, (10,10), Invalid, [10, 10])
print("=======================")
if Path:
    print("Finished, Path: " + str(Path))
else:
    print("Impossible Maze")

#Solve Second Time
"""input("Ready?")
RobotPos = [10,10]
for Tile in Path:
    Move(Tile, RobotPos)"""
