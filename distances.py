import RPi.GPIO as GPIO
from time import sleep
from time import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN) #CLOCK
GPIO.setup(20, GPIO.OUT) #TRIGGER
GPIO.setup(21, GPIO.IN) #INPUT

def scan(direction, available):
    """Get the distance from ultrasonics in a particular direction."""
    data = str(get_distance())      
    distance = int(data[data_marker:data_marker + 16], 2)
    if distance <= 5:
        available[direction] = False
    elif 5 < distance <= 30:
        available[direction] = True
    return available        

def motor_function(direction):
    """Run the motors as a thread."""
    global kill_motor
    while kill_motor == False:
        print('Motors Engaging')

def move_robot(direction):
    """Move the robot in direction by running motor threads."""
    global kill_motor
    kill_motor = False
    distance = 0
    engage_motors = threading.Thread(target = motor_function(direction))
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

def get_distance():
    """Get the distance from ultrasonics in all surrounding directions."""
    GPIO.output(20, False)
    def receive_data():
        full_input = []
        for _ in range(0, 16):
            while GPIO.input(16) == False:
                continue
            if GPIO.input(21) == True:
                full_input.append("1")
            else:
                full_input.append("0")
            while GPIO.input(16) == True:
                continue
        full_input = "".join(FullInput)
        print("Data Stream: " + full_input)
        return int(full_input, 2)
    print("Sending Trigger Pulse...")
    GPIO.output(20, True)
    data = receive_data()
    GPIO.output(20, False)
    print("Received distance data: " + str(data) + "cm")
    if data >= 3000:
        print("Invalid distance, retrying")
        data = get_distance()
    return data
