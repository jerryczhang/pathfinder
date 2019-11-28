from Color import AddColor
import Distances as d
class Tile(object):
	def __init__(self, Identifier, Available):
		self.Identifier = Identifier
		self.Available = Available
		self.Valid = True
		self.Visited = False
		self.EndPoint = False
		self.Visitations = 0
	def GetSurroundingTiles(self, PathFinder):
		#Returns tiles surrounding self in PathFinder.Matrix
		for Ypos in range(0, len(PathFinder.Matrix)):
			for Xpos in range(0, len(PathFinder.Matrix[0])):
				if PathFinder.Matrix[Ypos][Xpos].Identifier == self.Identifier:
					CurrentXpos = Xpos
					CurrentYpos = Ypos
		SurroundingTiles = {}
		if CurrentYpos - 1 >= 0:
			SurroundingTiles["North"] = PathFinder.Matrix[CurrentYpos - 1][CurrentXpos]
		else:
			SurroundingTiles["North"] = None
		if CurrentXpos + 1 < len(PathFinder.Matrix[0]):
			SurroundingTiles["East"] = PathFinder.Matrix[CurrentYpos][CurrentXpos + 1]	
		else:
			SurroundingTiles["East"] = None
		if CurrentXpos - 1 >= 0:
			SurroundingTiles["West"] = PathFinder.Matrix[CurrentYpos][CurrentXpos - 1]	
		else:
			SurroundingTiles["West"] = None
		if CurrentYpos + 1 < len(PathFinder.Matrix):
			SurroundingTiles["South"] = PathFinder.Matrix[CurrentYpos + 1][CurrentXpos]
		else:
			SurroundingTiles["South"] = None
		return SurroundingTiles
	def AvailableForInvalidation(self, PathFinder):
		SurroundingTiles = self.GetSurroundingTiles(PathFinder)
		Temp = 0
		for Direction in SurroundingTiles:
			if SurroundingTiles[Direction] != None:
				if SurroundingTiles[Direction].Valid == True and self.Available[Direction] == True:
					Temp += 1
		if Temp > 1:
			return False
		return True
class PathFinderHandler(object):
	def __init__(self):
		self.CurrentPosition = 0
		self.Directions = ["North","East","South","West"]
		self.NextTileIdentifier = 0
		self.Matrix = [[Tile(self.NextTileIdentifier, {"North":None,"East":None,"South":None,"West":None})]]
		self.NextTileIdentifier += 1
		self.SecondVisitation = False
		self.FirstRun = True
		self.NoWallPrint = AddColor(" ", "Blue", Highlight = True)
		self.WallPrint = AddColor(" ", "Red", Highlight = True)
		self.UnknownPrint = AddColor(" ", "Black", Highlight = True)
		self.ExitStatus = None
		self.Path = []
		#self.TestPrint = AddColor(" ", "Teal", Highlight = True)
	def PrintMatrix(self):
		#Prints the matrix and all specified walls
		PrintDesignator = ""
		for _ in range(0, len(self.Matrix[0])):
			PrintDesignator += "=="
		PrintDesignator += "="
		print(PrintDesignator)
		TempMatrix = []
		for RowNum in range(1, len(self.Matrix) + 1):
			TempMatrix.append([])
			TempMatrix.append([])
			if RowNum == 1:
				TempMatrix.append([])
			for TileNum in range(0, len(self.Matrix[RowNum - 1])):
				Tile = self.Matrix[RowNum - 1][TileNum]
				#Handles the placement of all symbols above the tiles (first row only)
				if RowNum == 1:
					TempMatrix[(RowNum * 2) - 2].append(self.WallPrint)
					if Tile.Available["North"] == True:
						TempMatrix[(RowNum * 2) - 2].append(self.NoWallPrint)
					elif Tile.Available["North"] == False:
						TempMatrix[(RowNum * 2) - 2].append(self.WallPrint)
					else:
						TempMatrix[(RowNum * 2) - 2].append(self.UnknownPrint)
				#Handles the placement of all symbols below the tiles
				TempMatrix[(RowNum * 2)].append(self.WallPrint)
				if Tile.Available["South"] == True:
					TempMatrix[(RowNum * 2)].append(self.NoWallPrint)
				elif Tile.Available["South"] == False:
					TempMatrix[(RowNum * 2)].append(self.WallPrint)
				else:
					TempMatrix[(RowNum * 2)].append(self.UnknownPrint)
				#Handles the placement of all symbols to the left of the tiles
				if Tile.Available["West"] == True:
					TempMatrix[(RowNum * 2) - 1].append(self.NoWallPrint)
				elif Tile.Available["West"] == False:
					TempMatrix[(RowNum * 2) - 1].append(self.WallPrint)
				else:
					TempMatrix[(RowNum * 2) - 1].append(self.UnknownPrint)
				#Places the tiles in the current row
				if self.NextAvailableTile() != None and Tile.Identifier == self.GetCurrentTile().GetSurroundingTiles(self)[self.NextAvailableTile()].Identifier:
					TempMatrix[(RowNum * 2) - 1].append(AddColor(chr(Tile.Identifier + 65), "Green", Highlight = True))
				else:
					if Tile.Valid == False:				
						TempMatrix[(RowNum * 2) - 1].append(AddColor(chr(Tile.Identifier + 65), "Red", Vibrant = True))
					elif Tile.Visited == True:
						TempMatrix[(RowNum * 2) - 1].append(AddColor(chr(Tile.Identifier + 65), "Yellow", Highlight = True))
					else:
						TempMatrix[(RowNum * 2) - 1].append(chr(Tile.Identifier + 65))
				#Handles the placement of all tiles to the right of the tiles (only last column)
				if TileNum == len(self.Matrix[RowNum - 1]) - 1:
					TempMatrix[(RowNum * 2) - 2].append(self.WallPrint)
					if Tile.Available["East"] == True:
						TempMatrix[(RowNum * 2) - 1].append(self.NoWallPrint)
					elif Tile.Available["East"] == False:
						TempMatrix[(RowNum * 2) - 1].append(self.WallPrint)
					else:
						TempMatrix[(RowNum * 2) - 1].append(self.UnknownPrint)
		TempMatrix[len(TempMatrix) - 1].append(self.WallPrint)
		for Row in TempMatrix:
			print("".join(Row))
		print(PrintDesignator)
	def InverseDirection(self, Direction):
		#Returns the direction 180 degrees opposed to the input direction ("West" returns "East")
		for Pos in range(0, len(self.Directions)):
			if self.Directions[Pos] == Direction:
				return self.Directions[Pos - 2]
	def ExpandMatrix(self, Direction):
		#Expands the matrix in a direction
		if Direction == self.Directions[0]: #If the direction is North
			self.Matrix.insert(0, [])
			for TilePos in range(0, len(self.Matrix[1])):
				TempAvailable = {
					"North":None,
					"East":None,
					"South":self.Matrix[1][TilePos].Available["North"],
					"West":None
				}
				self.Matrix[0].append(Tile(self.NextTileIdentifier, TempAvailable))
				self.NextTileIdentifier += 1
		elif Direction == self.Directions[1]: #If the direction is East
			for Row in self.Matrix:
				TempAvailable = {
					"North":None,
					"East":None,
					"South":None,
					"West":Row[len(Row) - 1].Available["East"]
				}
				Row.append(Tile(self.NextTileIdentifier, TempAvailable))
				self.NextTileIdentifier += 1
		elif Direction == self.Directions[2]: #If the direction is South
			self.Matrix.append([])
			for TilePos in range(0, len(self.Matrix[len(self.Matrix) - 2])):
				TempAvailable = {
					"North":self.Matrix[len(self.Matrix) - 2][TilePos].Available["South"],
					"East":None,
					"South":None,
					"West":None
				}
				self.Matrix[len(self.Matrix) - 1].append(Tile(self.NextTileIdentifier, TempAvailable))
				self.NextTileIdentifier += 1	
		elif Direction == self.Directions[3]: #If the direction is West
			for Row in self.Matrix:
				TempAvailable = {
					"North":None,
					"East":Row[0].Available["East"],
					"South":None,
					"West":None
				}				
				Row.insert(0, Tile(self.NextTileIdentifier, TempAvailable))
				self.NextTileIdentifier += 1	
	def GetCurrentTile(self):
		#Returns the tile specified by the identifier stored in self.CurrentPosition
		for Row in self.Matrix:
			for Tile in Row:
				if Tile.Identifier == self.CurrentPosition:
					return Tile
	def Refresh(self, Available):
		#Refreshes the surrounding area based on new data
		CurrentTile = self.GetCurrentTile()
		CurrentTile.Visited = True
		SurroundingTiles = CurrentTile.GetSurroundingTiles(self)
		#Expands the matrix if it is not large enough for the observed tiles
		for Direction in Available:
			if Available[Direction] == True and SurroundingTiles[Direction] == None:
				self.ExpandMatrix(Direction)
		#Updates the current tile and all existing surrounding tiles
		SurroundingTiles = CurrentTile.GetSurroundingTiles(self)				
		for Direction in Available:
			CurrentTile.Available[Direction] = Available[Direction]
			if SurroundingTiles[Direction] != None:
				SurroundingTiles[Direction].Available[self.InverseDirection(Direction)] = Available[Direction]
	def NextAvailableTile(self):
		#Generates the next available position based on validity and previous visitations
		CurrentTile = self.GetCurrentTile()
		SurroundingTiles = CurrentTile.GetSurroundingTiles(self)
		if CurrentTile.EndPoint == True:
			self.ExitStatus = "Completion"
			return None
		if (self.InvalidMaze() == True and self.FirstRun == True)or self.ExitStatus == "Invalidation":
			self.ExitStatus = "Invalidation"				
			return None
		for Direction in self.Directions:
			if SurroundingTiles[Direction] == None:
				SurroundingTiles.pop(Direction)
			elif CurrentTile.Available[Direction] == False:
				SurroundingTiles.pop(Direction)
		LowestValue = {}
		for Direction in SurroundingTiles:
			if SurroundingTiles[Direction].Valid == True and SurroundingTiles[Direction].Visited == False:
				return Direction
		for Direction in SurroundingTiles:
			if SurroundingTiles[Direction].Valid == True:
				self.SecondVisitation = True
				LowestValue[Direction] = SurroundingTiles[Direction].Visitations 
		if LowestValue != {}:
			#returns the direction for the tile with the lowest number of visitations
			return list(LowestValue.keys())[list(LowestValue.values()).index(min(LowestValue.values()))]
		self.ExitStatus = "Immobilization"
		return None
	def MoveToTile(self, Direction, Available):
		#Updates all variables after the robot moves to a tile and scans for data
		CurrentTile = self.GetCurrentTile()
		SurroundingTiles = CurrentTile.GetSurroundingTiles(self)
		if self.SecondVisitation == True and CurrentTile.Identifier != 0:
			if self.FirstRun == True:
				if CurrentTile.AvailableForInvalidation(self) == True:
					CurrentTile.Valid = False
			self.SecondVisitation = False
		#SurroundingTiles[Direction].Visited = True
		CurrentTile.Visited = True
		CurrentTile.Visitations += 1
		self.Path.append(chr(CurrentTile.Identifier + 65))
		self.CurrentPosition = SurroundingTiles[Direction].Identifier
		self.Refresh(Available)
	def ReachedGoal(self):
		#Marks the current tile as the end of the maze
		CurrentTile = self.GetCurrentTile()
		CurrentTile.EndPoint = True
	def Reset(self):
		#Resets the maze for any subsequent runs
		self.FirstRun = False
		self.CurrentPosition = 0
		self.Path = []
		for Row in self.Matrix:
			for Tile in Row:
				if Tile.Visited == False:
					Tile.Valid = False
				Tile.Visited = False
				Tile.Visitations = 0
	def InvalidMaze(self):
		Invalid = True
		for Row in self.Matrix:
			for Tile in Row:
				if True in list(Tile.Available.values()) and None in list(Tile.Available.values()):
					Invalid = False
					break
		return Invalid
