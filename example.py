import RPi.GPIO as GPIO
import time

RED = 14
GREEN = 15
BLUE = 18
buttonPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

click = 0
prev_input = GPIO.input(buttonPin)
lasttime = 0

def all_off():
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(BLUE, GPIO.HIGH)

try:
    print("1번 누름: off  / 2번: red  / 3번: green / 4번 : blue")

    while True:
        input = GPIO.input(buttonPin)
        curtime = time.time()

        if prev_input == GPIO.HIGH and input == GPIO.LOW:
            click += 1
            lasttime = curtime

        # 1초동안 입력없으면
        if click > 0 and (curtime - lasttime) > 1.0:
            print(f"총 클릭 수: {click}")

            if click == 2:
                GPIO.output(RED, GPIO.LOW)
                GPIO.output(GREEN, GPIO.HIGH)
                GPIO.output(BLUE, GPIO.HIGH)
            elif click == 3:
                GPIO.output(RED, GPIO.HIGH)
                GPIO.output(GREEN, GPIO.LOW)
                GPIO.output(BLUE, GPIO.HIGH)
            elif click == 4:
                GPIO.output(RED, GPIO.HIGH)
                GPIO.output(GREEN, GPIO.HIGH)
                GPIO.output(BLUE, GPIO.LOW)
            else:
            	GPIO.output(RED, GPIO.HIGH)
            	GPIO.output(GREEN, GPIO.HIGH)
            	GPIO.output(BLUE, GPIO.HIGH)


            click = 0

        prev_input = input
        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
