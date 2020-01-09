import RPi.GPIO as GPIO
from time import sleep
from time import time
import threading

class Robot:
    """Represents the motors and sensors of the robot."""

    def __init__(self):

        GPIO.setup(16, GPIO.IN) # clock
        GPIO.setup(20, GPIO.OUT) # trigger
        GPIO.setup(21, GPIO.IN) # input
        for pin in [6, 13, 19, 26]:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        motor1 = Motor(1, [6, 13], [19, 26])
        motor2 = Motor(2, [10, 9], [11, 5])
        motor3 = Motor(3, [4, 17], [27, 22])
        motor4 = Motor(4, [25, 8], [7, 12])

    def run_motors(direction):
        """Run the motors as a thread."""
        global kill_motor
        while kill_motor == False:
            print('Motors Engaging')

    def move_robot(direction):
        """Move the robot in direction by running motor threads."""
        global kill_motor
        kill_motor = False
        distance = 0
        engage_motors = threading.Thread(target = run_motors(direction))
        #data = str(get_distance())
        if direction == "North":
            data_marker = 0
        elif direction == "East":
            data_marker = 16
        elif direction == "South":
            data_marker = 32
        elif direction == "West":
            data_marker = 48
        start_distance = int(data[datamarker:data_marker + 16], 2)
        engage_motors.start()
        while start_distance - distance != 24:
            data = str(get_distance())
            distance = (data[datamarker:data_marker + 16], 2)
        kill_motor = True

    def get_distance(direction):
        """Get the distance from ultrasonics in a direction."""
        GPIO.output(20, True)
        data = []
        for _ in range(16):
            while GPIO.input(16) == False:
                continue
            if GPIO.input(21) == True:
                data.append("1")
            else:
                data.append("0")
            while GPIO.input(16) == True:
                continue
        data = "".join(data)
        GPIO.output(20, False)
        if data >= 3000:
            data = get_distance()
        return data
