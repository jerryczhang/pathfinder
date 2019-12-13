import RPi.GPIO as GPIO
from time import sleep
from hbridges import HBridge

GPIO.setmode(GPIO.BCM)
for pin in [6, 13, 19, 26]:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

class Motor():
    """Represents one motor, which is made up of two HBridges."""

    def __init__(self, identifier, pin_dict_ac, pin_dict_bd):
        """Initialize a motor with two component HBridges."""
        self.identifier = identifier
        self.hbridge_ac = HBridge(pin_dict_ac)
        self.hbridge_bd = HBridge(pin_dict_bd)
        self.steps_per_degree = 1 / 1.8
        self.current_step = 0

    def output(self, text):
        """Output a message from this motor."""
        print("[Motor " + str(self.identifier) + "]: " + str(text)) 

    def move(self, degrees, direction):
        """Move the motor degrees in direction (forward/backward)."""
        steps = int(degrees * steps_per_degree)
        if direction == 1:
            for step in range(1, steps + 1):
                if step % 4 == 1:
                    self.hbridge_ac.toggle(1)
                    self.hbridge_bd.toggle(1)
                elif step % 4 == 2:
                    self.hbridge_ac.toggle(-1)
                    self.hbridge_bd.toggle(1)
                elif step % 4 == 3:
                    self.hbridge_ac.toggle(-1)
                    self.hbridge_bd.toggle(-1)
                elif step % 4 == 0:
                    self.hbridge_ac.toggle(1)
                    self.hbridge_bd.toggle(-1)
                sleep(0.003)
        else:
            for step in range(1, steps + 1):
                if step % 4 == 1:
                    self.hbridge_ac.toggle(1)
                    self.hbridge_bd.toggle(-1)
                elif step % 4 == 2: 
                    self.hbridge_ac.toggle(-1)
                    self.hbridge_bd.toggle(-1)
                elif step % 4 == 3:
                    self.hbridge_ac.toggle(-1)
                    self.hbridge_bd.toggle(1)
                elif step % 4 == 0:
                    self.hbridge_ac.toggle(1)
                    self.hbridge_bd.toggle(1)
                sleep(0.003)

motor1 = Motor(1, {'In1': 6, 'In2': 13}, {'In1': 19, 'In2': 26})
motor2 = Motor(2, {'In1': 10, 'In2': 9}, {'In1': 11, 'In2': 5})
motor3 = Motor(3, {'In1': 4, 'In2': 17}, {'In1': 27, 'In2':22})
motor4 = Motor(4, {'In1': 25, 'In2': 8}, {'In1': 7, 'In2': 12})

GPIO.cleanup()
