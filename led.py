import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RED = 14
GREEN = 15
BLUE = 18

GPIO.setup(RED,GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)

for i in range(5):
	GPIO.output(RED, GPIO.LOW)
	GPIO.output(GREEN, GPIO.HIGH)
	GPIO.output(BLUE, GPIO.HIGH)

	time.sleep(1)

	GPIO.output(RED, GPIO.HIGH)
	GPIO.output(GREEN, GPIO.LOW)
	GPIO.output(BLUE, GPIO.HIGH)

	time.sleep(1)

	GPIO.output(RED, GPIO.HIGH)
	GPIO.output(GREEN, GPIO.HIGH)
	GPIO.output(BLUE, GPIO.LOW)

	time.sleep(1)

GPIO.cleanup()
