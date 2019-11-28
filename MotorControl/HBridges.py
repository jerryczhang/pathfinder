import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class HBridge(object):
	def __init__(self, GPIODict):
		self.State = 0
		self.GPIODict = GPIODict
		for value in self.GPIODict.values():
			GPIO.setup(value, GPIO.OUT) 
	def Toggle(self, State):
		if State == 0:
			GPIO.output(self.GPIODict["In1"], False)
			GPIO.output(self.GPIODict["In2"], False)
		elif State == 1:
			GPIO.output(self.GPIODict["In1"], True)
			GPIO.output(self.GPIODict["In2"], False)
		elif State == -1:
			GPIO.output(self.GPIODict["In1"], False)
			GPIO.output(self.GPIODict["In2"], True)
