#from robot import Robot
#import RPi.GPIO as GPIO
from pathfinder import Pathfinder
from time import time

MANUAL = 0
RANDOM = 1
SENSOR = 2
FULL   = 3

def main():
    """Main method, initializes robot and solves maze."""

    #GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)

    pathfinder = Pathfinder(MANUAL, (3, -3), 0)
    while True:
        x_start = int(input("X coordinate of starting node:"))
        y_start = int(input("Y coordinate of starting node:"))
        time0 = time()
        path = pathfinder.start((x_start, y_start), "mazes/maze1.txt")
        if path:
            print("Finished, path: " + str(path))
        else:
            print("Impossible maze")
        time1 = time()
        print("Time: " + str(time1 - time0))
    #GPIO.cleanup()

if __name__ == '__main__':
    main()
