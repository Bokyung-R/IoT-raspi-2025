from flask import Flask, request, render_template
import RPi.GPIO as GPIO

app= Flask(__name__)

ledPin = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/data', methods=['post'])
def data():
	data = request.form['led']
	if data=='on':
		GPIO.output(ledPin, GPIO.LOW)
	else:
		GPIO.output(ledPin, GPIO.HIGH)
	return render_template("index.html")

if __name__=="__main__":
	app.run(host='0.0.0.0')
