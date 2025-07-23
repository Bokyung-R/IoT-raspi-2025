from flask import Flask, request, redirect, render_template
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

# === GPIO 핀 설정 ===
CAR_GREEN = 18
CAR_YELLOW = 15
CAR_RED = 14

PED_RED = 23
PED_GREEN = 24

PED_BUTTON = 25
BUZZER = 26 

# === 타이머 기본값 (초 단위) ===
timers = {
    "car_green": 8,
    "car_yellow": 3,
    "car_red": 5
}

# === GPIO 초기 설정 ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in [CAR_GREEN, CAR_YELLOW, CAR_RED, PED_RED, PED_GREEN, BUZZER]:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(PED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# === 초기 LED 상태 설정 ===
GPIO.output(CAR_GREEN, GPIO.HIGH)
GPIO.output(CAR_YELLOW, GPIO.HIGH)
GPIO.output(CAR_RED, GPIO.HIGH)
GPIO.output(PED_RED, GPIO.LOW)
GPIO.output(PED_GREEN, GPIO.LOW)
GPIO.output(BUZZER, GPIO.LOW)

pedestrian_requested = False
lock = threading.Lock()
current_status = "초기화 중"

def button_pressed(channel):
    global pedestrian_requested
    with lock:
        if not pedestrian_requested:
            pedestrian_requested = True

GPIO.add_event_detect(PED_BUTTON, GPIO.RISING, callback=button_pressed, bouncetime=300)

# === 상태 함수 정의 ===
def car_green_ped_red():
    GPIO.output(CAR_GREEN, GPIO.HIGH)
    GPIO.output(CAR_YELLOW, GPIO.LOW)
    GPIO.output(CAR_RED, GPIO.LOW)
    GPIO.output(PED_RED, GPIO.LOW)
    GPIO.output(PED_GREEN, GPIO.HIGH)
    GPIO.output(BUZZER, GPIO.LOW)

def car_yellow_ped_red():
    GPIO.output(CAR_GREEN, GPIO.LOW)
    GPIO.output(CAR_YELLOW, GPIO.HIGH)
    GPIO.output(CAR_RED, GPIO.LOW)
    GPIO.output(PED_RED, GPIO.LOW)
    GPIO.output(PED_GREEN, GPIO.HIGH)
    GPIO.output(BUZZER, GPIO.LOW)

def car_red_ped_green():
    GPIO.output(CAR_GREEN, GPIO.LOW)
    GPIO.output(CAR_YELLOW, GPIO.LOW)
    GPIO.output(CAR_RED, GPIO.HIGH)
    GPIO.output(PED_RED, GPIO.HIGH)
    GPIO.output(PED_GREEN, GPIO.LOW)

    for _ in range(timers["car_red"] * 2):  
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(BUZZER, GPIO.LOW)
        time.sleep(0.3)

def pedestrian_sequence():
    global current_status

    current_status = "보행자 버튼 클릭됨 - 2초 후 차량 노란불"
    time.sleep(2)
    car_yellow_ped_red()
    time.sleep(timers["car_yellow"])

    current_status = "자동차 빨간불 / 도보 초록불 + 부저 울림"
    car_red_ped_green()

    current_status = "자동차 노란불 / 도보 빨간불"
    car_yellow_ped_red()
    time.sleep(timers["car_yellow"])

def run_traffic_loop():
    global pedestrian_requested, current_status

    while True:
        if pedestrian_requested:
            pedestrian_sequence()
            with lock:
                pedestrian_requested = False
        else:
            current_status = "자동차 초록불 / 도보 빨간불"
            car_green_ped_red()
            time.sleep(timers["car_green"])

            current_status = "자동차 노란불 / 도보 빨간불"
            car_yellow_ped_red()
            time.sleep(timers["car_yellow"])

            current_status = "자동차 빨간불 / 도보 초록불 + 부저 울림"
            car_red_ped_green()
            time.sleep(timers["car_red"])

            current_status = "자동차 노란불 / 도보 빨간불"
            car_yellow_ped_red()
            time.sleep(timers["car_yellow"])

# === 웹 라우팅 ===
@app.route('/')
def index():
    return render_template('admin.html', timers=timers, status=current_status)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global timers
    if request.method == 'POST':
        for key in ["car_green", "car_yellow", "car_red"]:
            if key in request.form:
                try:
                    timers[key] = int(request.form[key])
                except ValueError:
                    pass
        return redirect('/admin')
    return render_template('admin.html', timers=timers, status=current_status)

# === 앱 실행 ===
if __name__ == '__main__':
    t = threading.Thread(target=run_traffic_loop)
    t.daemon = True
    t.start()
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
