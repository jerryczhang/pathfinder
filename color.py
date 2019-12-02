def add_color(text, color, vibrant = False, highlight = False):
    """Add color, vibrancy, or highlight to a string."""
    if color == "Black":
        value = "90"
    elif color == "Red":
        value = "91"
    elif color == "Green":
        value = "92"
    elif color == "Yellow":
        value = "93"
    elif color == "Blue":
        value = "94"
    elif color == "Purple":
        value = "95"
    elif color == "Teal":
        value = "96"
    elif color == "White":
        value = "97"
    else:
        return Text
    if vibrant == True and highlight == False:
        value = str(int(value) - 60)
    if vibrant == False and highlight == True:
        value = str(int(value) - 50)        
    return "\033[" + value + "m" + text + "\033[0m"

def color_table():
    """Print out all possible color options."""
    for color in range(1, 100):
        print("\033[" + str(color) + "m Color " + str(color) + " \033[0m")
