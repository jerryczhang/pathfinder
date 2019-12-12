import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class HBridge():
	def __init__(self, GPIO_dict):
		self.state = 0
		self.GPIO_dict = GPIODict
		for value in self.GPIO_dict.values():
			GPIO.setup(value, GPIO.OUT) 
	def Toggle(self, state):
		if state == 0:
			GPIO.output(self.GPIO_dict["In1"], False)
			GPIO.output(self.GPIO_dict["In2"], False)
		elif state == 1:
			GPIO.output(self.GPIO_dict["In1"], True)
			GPIO.output(self.GPIO_dict["In2"], False)
		elif state == -1:
			GPIO.output(self.GPIO_dict["In1"], False)
			GPIO.output(self.GPIO_dict["In2"], True)
