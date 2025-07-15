import RPi.GPIO as GPIO
import time

RED = 14
BLUE = 15
buttonPin = 17
piezoPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(piezoPin, GPIO.OUT)

sound = GPIO.PWM(piezoPin, 440)

click = 0
prev_input = GPIO.input(buttonPin)
lasttime = time.time()

is_siren_on = False

try:
	print("1번 누름: 사이렌 정지, 2번 누름: 사이렌 시작")
	while True:
		input_state = GPIO.input(buttonPin)
		curtime = time.time()

		if prev_input == GPIO.HIGH and input_state == GPIO.LOW:
			click += 1
			lasttime = curtime
			time.sleep(0.2)

		if click > 0 and (curtime - lasttime) > 0.5:
			print(f"{click} 클릭")

			if click == 1:
				is_siren_on = False
				sound.stop()
				GPIO.output(RED, GPIO.HIGH)
				GPIO.output(BLUE, GPIO.HIGH)
				print("사이렌 정지")

			elif click == 2:
				is_siren_on = True
				sound.start(50)
				print("사이렌 실행")

			click = 0

		if is_siren_on:
			sound.ChangeFrequency(880)
			GPIO.output(RED, GPIO.LOW)
			GPIO.output(BLUE, GPIO.HIGH)

			time.sleep(0.3)

			sound.ChangeFrequency(440)
			GPIO.output(RED, GPIO.HIGH)
			GPIO.output(BLUE, GPIO.LOW)

			time.sleep(0.3)

			prev_input = input_state
			time.sleep(0.01)

except KeyboardInterrupt:
    print("프로그램 종료")

finally:
    sound.stop()
    GPIO.cleanup()
