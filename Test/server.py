from flask import Flask, request, redirect
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

# GPIO 핀 설정
CAR_RED = 17
CAR_YELLOW = 27
CAR_GREEN = 22
PED_RED = 23
PED_GREEN = 24
BUTTON_PIN = 25

GPIO.setmode(GPIO.BCM)
pins = [CAR_RED, CAR_YELLOW, CAR_GREEN, PED_RED, PED_GREEN]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 신호등 시간 (초)
timings = {
    'green': 60,
    'yellow': 3,
    'red': 30
}

lock = threading.Lock()
pedestrian_requested = False

def signal_loop():
    global pedestrian_requested
    while True:
        with lock:
            green = timings['green']
            yellow = timings['yellow']
            red = timings['red']
        # 1. 자동차 초록불
        GPIO.output(CAR_GREEN, GPIO.HIGH)
        GPIO.output(CAR_YELLOW, GPIO.LOW)
        GPIO.output(CAR_RED, GPIO.LOW)
        GPIO.output(PED_RED, GPIO.HIGH)
        GPIO.output(PED_GREEN, GPIO.LOW)
        wait_with_button_check(green)

        # 2. 노랑불
        GPIO.output(CAR_GREEN, GPIO.LOW)
        GPIO.output(CAR_YELLOW, GPIO.HIGH)
        wait_with_button_check(yellow)

        # 3. 빨간불
        GPIO.output(CAR_YELLOW, GPIO.LOW)
        GPIO.output(CAR_RED, GPIO.HIGH)
        if pedestrian_requested:
            # 횡단보도 초록불로 5초 후 바꾸기
            time.sleep(5)
            GPIO.output(PED_RED, GPIO.LOW)
            GPIO.output(PED_GREEN, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(PED_GREEN, GPIO.LOW)
            GPIO.output(PED_RED, GPIO.HIGH)
            pedestrian_requested = False
        time.sleep(red)

def wait_with_button_check(duration):
    global pedestrian_requested
    start = time.time()
    while time.time() - start < duration:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            pedestrian_requested = True
        time.sleep(0.1)

threading.Thread(target=signal_loop, daemon=True).start()

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        green = int(request.form.get('green', 60))
        yellow = int(request.form.get('yellow', 3))
        red = int(request.form.get('red', 30))
        with lock:
            timings['green'] = green
            timings['yellow'] = yellow
            timings['red'] = red
        return redirect('/admin')
    
    with lock:
        green = timings['green']
        yellow = timings['yellow']
        red = timings['red']
    
    return f"""
    <h2>신호등 시간 설정 (Admin)</h2>
    <form method="post">
        자동차 초록불 시간 (초): <input type="number" name="green" value="{green}"><br><br>
        자동차 노랑불 시간 (초): <input type="number" name="yellow" value="{yellow}"><br><br>
        자동차 빨간불 시간 (초): <input type="number" name="red" value="{red}"><br><br>
        <button type="submit">설정 저장</button>
    </form>
    <br>
    <a href="/">홈으로</a>
    """

@app.route('/')
def home():
    return """
    <h2>신호등 제어 시스템</h2>
    <a href="/admin">관리자 페이지로 이동</a>
    """

@app.teardown_appcontext
def cleanup(exception=None):
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        GPIO.cleanup()
