#from robot import Robot
#import RPi.GPIO as GPIO
from pathfinder import Pathfinder

MANUAL = 0
RANDOM = 1
SENSOR = 2
FULL   = 3

def main():
    """Main method, initializes robot and solves maze."""

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)

    pathfinder = Pathfinder(MANUAL, (3, -3), 1)
    while True:
        x_start = int(input("X coordinate of starting node:"))
        y_start = int(input("Y coordinate of starting node:"))
        path = pathfinder.start((x_start, y_start), "mazes/maze1.txt");
        if path:
            print("Finished, path: " + str(path))
        else:
            print("Impossible maze")
    #GPIO.cleanup()

if __name__ == '__main__':
    main()
