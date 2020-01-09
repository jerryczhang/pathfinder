import RPi.GPIO as GPIO

class HBridge():
    """Represents an HBridge motor controller."""

    def __init__(self, pin1, pin2):
        """Initialize the current state to 0, and set up GPIO pins."""
        self.state = 0
        self.pin1 = in1
        self.pin2 = in2
        GPIO.setup(self.pin1, GPIO.OUT) 
        GPIO.setup(self.pin2, GPIO.OUT) 

    def toggle(self, state):
        """Set the output of the HBridge."""
        if state == 0:
                GPIO.output(self.pin1, False)
                GPIO.output(self.pin2, False)
        elif state == 1:
                GPIO.output(self.pin1, True)
                GPIO.output(self.pin2, False)
        elif state == -1:
                GPIO.output(pin1, False)
                GPIO.output(pin2, True)
