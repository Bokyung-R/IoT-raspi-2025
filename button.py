import RPi.GPIO as GPIO
import time

buttonPin = 17

GPIO.setmode(GPIO.BCM)

#GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 내부풀업 풀아둔 설정
GPIO.setup(buttonPin, GPIO.IN)

try:
	while True:
		if(GPIO.input(buttonPin)):
			print("button released")
		else:
			print("button pressed")
		time.sleep(0.5)
except KeyboardInterrupt:
	GPIO.cleanup()
