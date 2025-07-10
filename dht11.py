#pip install adafruit-circuitpython-dht
# sudo api install libgpiod2

import RPi.GPIO as GPIO
import time
import adafruit_dht
import board

dhtPin = 23

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#GPIO.setup(dhtPin, GPIO.IN)

dht = adafruit_dht.DHT11(board.D23)

while True:
	try:
		temperature = dht.temperature
		humidity = dht.humidity
		print("Temp: ",temperature)
		print("Humi: ",humidity)
		time.sleep(1)

	except RuntimeError as error:
		print(error.args[0])

	except KeyboardInterrupt:
		#GPIO.cleanup()
		break

dhtPin.exit()
