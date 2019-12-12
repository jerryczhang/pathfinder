import RPi.GPIO as GPIO
from time import sleep
def get_distance():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(16, GPIO.IN) #clock
	GPIO.setup(21, GPIO.OUT) #trigger
	GPIO.setup(20, GPIO.IN) #input
	GPIO.output(21, False)
	def receive_data():
		full_input = []
		for _ in range(0, 16):
			while GPIO.input(16) == False:
				continue
			if GPIO.input(20) == True:
				full_input.append("1")
			else:
				full_input.append("0")
			while GPIO.input(16) == True:
				continue
		full_input = "".join(FullInput)
		print("Data Stream: " + full_input)
		return int(full_input, 2)
	print("Sending Trigger Pulse...")
	GPIO.output(21, True)
	data = receive_data()
	GPIO.output(21, False)
	if data >= 3000:
		exit()
	print("Received Distance Data: " + str(data) + "cm")
get_distance()
