
import RPi.GPIO as GPIO
import time

swPin = 14
BLUE = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(swPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def printcallback(channel):
	print("pushed")
	GPIO.output(BLUE,GPIO.LOW)
	time.sleep(0.5)
	GPIO.output(BLUE, GPIO.HIGH)

GPIO.add_event_detect(swPin, GPIO.RISING, callback=printcallback)

try:
	while True:
		pass

except KeyboardInterrupt:
	GPIO.cleanup()
