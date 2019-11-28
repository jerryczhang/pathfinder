from time import sleep
import Hybrid
import Distances
Available = {"North" : True, "East" : True, "South": False, "West" : False}
PathFinder = Hybrid.PathFinderHandler()
PathFinder.Refresh(Available)
while True:
	PathFinder.PrintMatrix()
	End = input("End? (TRUE/FALSE): ")
	if End.upper() == "TRUE":
		PathFinder.ReachedGoal()
		break
	Next = PathFinder.NextAvailableTile()
	if Next == None:
		print("Ended the first maze simulation due to " + PathFinder.ExitStatus)
		print("Origin Path: " + "-".join(PathFinder.Path))
		break
	Available = PathFinder.GetCurrentTile().GetSurroundingTiles(PathFinder)[Next].Available
	for Direction in PathFinder.Directions:
		CurrentTile = PathFinder.GetCurrentTile().GetSurroundingTiles(PathFinder)[Next]
		if CurrentTile == None or CurrentTile.Available[Direction] == None:
			input("Scan " + Direction + " (Press Enter)")
			Distance = Distances.GetDistance()
			if Distance >= 10:
				Available[Direction] = True
			else:
				Available[Direction] = False
	PathFinder.MoveToTile(Next, Available)
PathFinder.Reset()
while True:
	PathFinder.PrintMatrix()
	Next = PathFinder.NextAvailableTile()
	if Next == None:
		print("Ended the second maze simulation due to " + PathFinder.ExitStatus)
		print("Second Path: " + "-".join(PathFinder.Path))
		break
	PathFinder.MoveToTile(Next, Available)
	sleep(0.5)
"""def GetAvailable(PreviousMove):
	global XPos
	global YPos
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
		PathFinder.MoveToTile(Next, GetAvailable(Next))
		PathFinder.MoveToTile(Next, GetAvailable(Next))	
	PathFinder.PrintMatrix()
	sleep(1)"""
