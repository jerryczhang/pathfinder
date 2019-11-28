def AddColor(Text, Color, Vibrant = False, Highlight = False):
	if Color == "Black":
		Value = "90"
	elif Color == "Red":
		Value = "91"
	elif Color == "Green":
		Value = "92"
	elif Color == "Yellow":
		Value = "93"
	elif Color == "Blue":
		Value = "94"
	elif Color == "Purple":
		Value = "95"
	elif Color == "Teal":
		Value = "96"
	elif Color == "White":
		Value = "97"
	else:
		return Text
	if Vibrant == True and Highlight == False:
		Value = str(int(Value) - 60)
	if Vibrant == False and Highlight == True:
		Value = str(int(Value) - 50)		
	return "\033[" + Value + "m" + Text + "\033[0m"
def ColorTable():
	for Color in range(1, 100):
		print("\033[" + str(Color) + "m Color " + str(Color) + " \033[0m")
