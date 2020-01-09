import RPi.GPIO as GPIO
from time import sleep
from hbridges import HBridge

class Motor():
    """Represents one motor, which is made up of two HBridges."""

    def __init__(self, identifier, pins_ac, pins_bd):
        """Initialize a motor with two component HBridges."""
        self.identifier = identifier
        self.hbridge_ac = HBridge(pins_ac[0], pins_ac[1])
        self.hbridge_bd = HBridge(pins_bd[0], pins_bd[1])
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

