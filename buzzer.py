import RPi.GPIO as GPIO
import time
piezoPin = 18

Melody = [131, 146, 164,175,196,220,247,262]

GPIO.setmode(GPIO.BCM)

GPIO.setup(piezoPin, GPIO.OUT)

sound = GPIO.PWM(piezoPin, 440)


try:
	while True:
		sound.start(50)
		for i in range(0,len(Melody)):
			sound.ChangeFrequency(Melody[i])
			time.sleep(0.5)
		sound.stop()
		time.sleep(1)

except KeyboardInterrupt:
	print("end..")

finally:
	GPIO.cleanup()
