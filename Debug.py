from Hybrid import PathFinderHandler
from time import sleep
from random import randint, randrange
def MoveDirection(Direction):
	global XPos
	global YPos
	if Direction == "North":
		YPos -= 1
	elif Direction == "South":
		YPos += 1
	elif Direction == "West":
		XPos -= 1
	elif Direction == "East":
		XPos += 1
def GetAvailable(PreviousMove):
	global XPos
	global YPos
	Available = PathFinder.GetCurrentTile().GetSurroundingTiles(PathFinder)[PreviousMove].Available
	for Direction in PathFinder.Directions:
		CurrentTile = PathFinder.GetCurrentTile().GetSurroundingTiles(PathFinder)[PreviousMove]
		if CurrentTile == None or CurrentTile.Available[Direction] == None:
			if (	XPos == 1 and Direction == "West" or 
				XPos == 4 and Direction == "East" or
				YPos == 1 and Direction == "North" or
				YPos == 4 and Direction == "South"	):
				Available[Direction] = False
			else:
				Available[Direction] = randrange(100) < 50
	return Available
while True:
	PathFinder = PathFinderHandler()
	PathFinder.Refresh({"North":False, "East":True, "South":True, "West":False})
	XPos = 1
	YPos = 1
	while True:
		if XPos == 4 and YPos == 4:
			PathFinder.ReachedGoal()
		Next = PathFinder.NextAvailableTile()
		MoveDirection(Next)
		if Next == None:
			print("Ended the first maze simulation due to " + PathFinder.ExitStatus)
			print("Origin Path: " + "-".join(PathFinder.Path))
			break
		PathFinder.MoveToTile(Next, GetAvailable(Next))
	PathFinder.Reset()
	while True:
		Next = PathFinder.NextAvailableTile()
		if Next == None:
			print("Ended the second maze simulation due to " + PathFinder.ExitStatus)
			print("Second Path: " + "-".join(PathFinder.Path))
			break
		PathFinder.MoveToTile(Next, GetAvailable(Next))	
	PathFinder.PrintMatrix()
	sleep(1)
