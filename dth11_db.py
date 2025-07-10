#pip install adafruit-circuitpython-dht
# sudo api install libgpiod2

import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import pymysql

dhtPin = 23

#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#GPIO.setup(dhtPin, GPIO.IN)

dht = adafruit_dht.DHT11(board.D23)

## db연결
conn = pymysql.connect(
	host = 'localhost',
	user = 'root',
	password='12345',
	database='test_db',
	charset = 'utf8'
)

try:
	with conn.cursor() as cur:
		sql = "insert into dht(temp, humid) values(%s, %s)"

		while True:
			try:
				temperature = dht.temperature
				humidity = dht.humidity

				print("Temp: ",temperature)
				print("Humi: ",humidity)

				cur.execute(sql, (temperature, humidity))
				conn.commit()

				time.sleep(1)

			except RuntimeError as error:
				print(error.args[0])

			except KeyboardInterrupt:
				#GPIO.cleanup()
				break
except KeyboardInterrupt:
	print("종료")
finally:
	conn.close()
	
dhtPin.exit()
