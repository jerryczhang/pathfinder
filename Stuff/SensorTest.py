import RPi.GPIO as GPIO
from time import sleep
def GetDistance():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(16, GPIO.IN) #clock
	GPIO.setup(21, GPIO.OUT) #trigger
	GPIO.setup(20, GPIO.IN) #input
	GPIO.output(21, False)
	def ReceiveData():
		FullInput = []
		for _ in range(0, 16):
			while GPIO.input(16) == False:
				continue
			if GPIO.input(20) == True:
				FullInput.append("1")
			else:
				FullInput.append("0")
			while GPIO.input(16) == True:
				continue
		FullInput = "".join(FullInput)
		print("Data Stream: " + FullInput)
		return int(FullInput, 2)
	print("Sending Trigger Pulse...")
	GPIO.output(21, True)
	Data = ReceiveData()
	GPIO.output(21, False)
	if Data >= 3000:
		exit()
	print("Received Distance Data: " + str(Data) + "cm")
GetDistance()
