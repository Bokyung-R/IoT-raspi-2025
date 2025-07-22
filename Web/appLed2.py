from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

RED = 14
BLUE = 18
GREEN = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

@app.route('/')
def ledFlask():
	return "LED Control Web"

@app.route('/led/<state>')
def led(state):
	if state == 'red':
		GPIO.output(RED, GPIO.LOW)
		GPIO.output(BLUE,GPIO.HIGH)
		GPIO.output(GREEN,GPIO.HIGH)
	elif state== 'blue':
		GPIO.output(RED,GPIO.HIGH)
		GPIO.output(BLUE, GPIO.LOW)
		GPIO.output(GREEN, GPIO.HIGH)
	elif state == 'green':
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.HIGH)
		GPIO.output(GREEN, GPIO.LOW)
	elif state == 'off':
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.HIGH)
		GPIO.output(GREEN,GPIO.HIGH)
	return "LED" + state

@app.route('/led/clean')
def gpiocleanup():
	GPIO.cleanup()
	return "<h1> GPIO CLEANUP </h1>"

if __name__=="__main__":
	app.run(host='0.0.0.0')
