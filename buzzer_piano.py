import RPi.GPIO as GPIO
import time

piezoPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

sound = GPIO.PWM(piezoPin, 440)

note_freq = {
    '1': 261.63,
    '2': 293.66,
    '3': 329.63,
    '4': 349.23,
    '5': 392.00,
    '6': 440.00,
    '7': 493.88,
    '8': 523.25,
}

try:
    sound.start(0)
    while True:
        key = input("1~8 중에 누르고 enter, 종료시 Q/q\n").lower()
        if key == 'q':
            break
        if key in note_freq:
            freq = note_freq[key]
            sound.ChangeFrequency(freq)
            sound.ChangeDutyCycle(50)
            time.sleep(0.5)
            sound.ChangeDutyCycle(0)
        else:
            print("1~8 사이 값을 입력해주세요.\n")

except KeyboardInterrupt:
    print("end...")

finally:
    sound.stop()
    GPIO.cleanup()
