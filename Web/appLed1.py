from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

ledPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

@app.route('/')
def helloflask():
    return "Hello Flask"

@app.route('/led/on')
def ledon():
    GPIO.output(ledPin, GPIO.LOW)
    return "<h1> LED ON </h1>"

@app.route('/led/off')
def ledoff():
    GPIO.output(ledPin, GPIO.HIGH)
    return "<h1> LED OFF </h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port ="5000")
