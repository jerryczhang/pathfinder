from Color import AddColor
from random import randint
from time import sleep
#import Distances
import sys
Row = []
Array = []
for _ in range(1, 10):
	Blank = str(AddColor(" ", "Black", Highlight = True))
	Row.append(Blank)
for _ in range(1, 10):
	Array.append(list(Row))
#print array
def PrintArray():
	for Row in Array:
		for Item in Row:
			sys.stdout.write(Item)
		sys.stdout.write('\n')
#move robot
def Move(Position, RobotPos):
	XMove = Position[0] - RobotPos[0]
	YMove = Position[1] - RobotPos[1]
	if XMove >= 2 or YMove >= 2:
		return
	else:
		RobotPos[0] += XMove
		print("RobotPos:" + str(RobotPos))
		RobotPos[1] += YMove
		print("RobotPos:" + str(RobotPos))
#reverse given direction
def Reverse(Direction):
	Directions = ['n', 'e', 's', 'w', 'n', 'e', 's', 'w']
	return Directions[Directions.index(Direction) + 2]
#recursive function
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
