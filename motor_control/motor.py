import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for pin in [6, 13, 19, 26]:
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, False)
from time import sleep
from hbridges import HBridge
class Motor():
	def __init__(self, identifier, pin_dict_ac, pin_dict_bd):
		self.identifier = identifier
		self.current_step = 0	#Increment current step after each step
		self.hbridge_ac = HBridge(pin_dict_ac)
		self.hbridge_bd = HBridge(pin_dict_bd)
	def output(self, text):
		print("[Motor " + str(self.identifier) + "]: " + str(text)) 
	def move(self, degrees, direction):
		steps = int(degrees/1.8)
		if direction == 1:
			for step in range(1, steps + 1):
				sleep(0.5)
				if step % 4 == 1:
					self.output("step 1")
					self.hbridge_ac.toggle(1)
					self.hbridge_bd.toggle(1)
				elif step % 4 == 2:
					self.output("step 2")
					self.hbridge_ac.toggle(-1)
					self.hbridge_bd.toggle(1)
				elif step % 4 == 3:
					self.output("step 3")
					self.hbridge_ac.toggle(-1)
					self.hbridge_bd.toggle(-1)
				elif step % 4 == 0:
					self.output("step 4")
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
#Motor2 = Motor(2, {'In1': 10, 'In2': 9}, {'In1': 11, 'In2': 5})
#Motor3 = Motor(3, {'In1': 4, 'In2': 17}, {'In1': 27, 'In2':22})
#Motor4 = Motor(4, {'In1': 25, 'In2': 8}, {'In1': 7, 'In2': 12})
while True:
        xmotor = motor1
	#for XMotor in [Motor1, Motor2, Motor3, Motor4]:
	xmotor.move(180, 1)
	sleep(0.003)
	xmotor.move(180, -1)
	sleep(0.003)
	break
for pin in [6, 13, 19, 26]:
	GPIO.output(pin, False)
GPIO.cleanup()
