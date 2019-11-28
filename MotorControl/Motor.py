import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for Pin in [6, 13, 19, 26]:
	GPIO.setup(Pin, GPIO.OUT)
	GPIO.output(Pin, False)
from time import sleep
from HBridges import HBridge
class Motor(object):
	def __init__(self, Identifier, PinDictAC, PinDictBD):
		self.Identifier = Identifier
		self.CurrentStep = 0	#Increment current step after each step
		self.HBridgeAC = HBridge(PinDictAC)
		self.HBridgeBD = HBridge(PinDictBD)
	def Output(self, Text):
		print("[Motor " + str(self.Identifier) + "]: " + str(Text)) 
	def Move(self, Degrees, Direction):
		Steps = int(Degrees/1.8)
		if Direction == 1:
			for Step in range(1, Steps + 1):
				sleep(0.5)
				if Step % 4 == 1:
					self.Output("Step 1")
					self.HBridgeAC.Toggle(1)
					self.HBridgeBD.Toggle(1)
				elif Step % 4 == 2:
					self.Output("Step 2")
					self.HBridgeAC.Toggle(-1)
					self.HBridgeBD.Toggle(1)
				elif Step % 4 == 3:
					self.Output("Step 3")
					self.HBridgeAC.Toggle(-1)
					self.HBridgeBD.Toggle(-1)
				elif Step % 4 == 0:
					self.Output("Step 4")
					self.HBridgeAC.Toggle(1)
					self.HBridgeBD.Toggle(-1)
				sleep(0.003)
		else:
			for Step in range(1, Steps + 1):
				if Step % 4 == 1:
					self.HBridgeAC.Toggle(1)
					self.HBridgeBD.Toggle(-1)
				elif Step % 4 == 2: 
					self.HBridgeAC.Toggle(-1)
					self.HBridgeBD.Toggle(-1)
				elif Step % 4 == 3:
					self.HBridgeAC.Toggle(-1)
					self.HBridgeBD.Toggle(1)
				elif Step % 4 == 0:
					self.HBridgeAC.Toggle(1)
					self.HBridgeBD.Toggle(1)
				sleep(0.003)

Motor1 = Motor(1, {'In1': 6, 'In2': 13}, {'In1': 19, 'In2': 26})
#Motor2 = Motor(2, {'In1': 10, 'In2': 9}, {'In1': 11, 'In2': 5})
#Motor3 = Motor(3, {'In1': 4, 'In2': 17}, {'In1': 27, 'In2':22})
#Motor4 = Motor(4, {'In1': 25, 'In2': 8}, {'In1': 7, 'In2': 12})
print("Attempting to do Alex's Mom")
while True:
	XMotor = Motor1
	#for XMotor in [Motor1, Motor2, Motor3, Motor4]:
	XMotor.Move(180, 1)
	sleep(0.003)
	XMotor.Move(180, -1)
	sleep(0.003)
	break
for Pin in [6, 13, 19, 26]:
	GPIO.output(Pin, False)
GPIO.cleanup()
