import RPi.GPIO as GPIO
from time import sleep
import threading
from time import time
import threading
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN) #CLOCK
GPIO.setup(20, GPIO.OUT) #TRIGGER
GPIO.setup(21, GPIO.IN) #INPUT
def Scan(Directions, Available):
	Data = str(GetDistance())	
	DataMarker = 0
	for Direction in Directions:
		Distance = int(Data[DataMarker:DataMarker + 16], 2)
		if Distance <= 5:
			Available[Direction] = False
		elif 5 < Distance <= 30:
			Available[Direction] = True
		DataMarker += 16
	return Available	
def MotorFunction(Direction):
	global KillMotor
	while KillMotor == False:
		#Run Motors
		print('Motors Engaging')
def MoveRobot(Direction):
	global KillMotor
	KillMotor = False
	Distance = 0
	EngageMotors = threading.Thread(target = MotorFunction(Direction))
	#Data = str(GetDistance())
	if Direction == "North":
		DataMarker = 0
	elif Direction == "East":
		DataMarker = 16
	elif Direction == "South":
		DataMarker = 32
	elif Direction == "West":
		DataMarker = 48
	StartDistance = int(Data[Datamarker:DataMarker + 16], 2)
	EngageMotors.start()
	while StartDistance - Distance != 24:
		Data = str(GetDistance())
		Distance = (Data[Datamarker:DataMarker + 16], 2)
	KillMotor = True
def GetDistance():
	GPIO.output(20, False)
	def ReceiveData():
		FullInput = []
		for _ in range(0, 16):
			while GPIO.input(16) == False:
				continue
			if GPIO.input(21) == True:
				FullInput.append("1")
			else:
				FullInput.append("0")
			while GPIO.input(16) == True:
				continue
		FullInput = "".join(FullInput)
		print("Data Stream: " + FullInput)
		return int(FullInput, 2)
	print("Sending Trigger Pulse...")
	GPIO.output(20, True)
	Data = ReceiveData()
	GPIO.output(20, False)
	print("Received Distance Data: " + str(Data) + "cm")
	if Data >= 3000:
		print("Invalid distance, retrying")
		Data = GetDistance()
	return Data
