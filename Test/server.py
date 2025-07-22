from flask import Flask, request, redirect, render_template
import threading
import time
import RPi.GPIO as GPIO

app = Flask(__name__)

# 자동차 신호 LED (빨강, 노랑, 초록)
CAR_GREEN = 14
CAR_YELLOW = 15
CAR_RED = 18

# 횡단보도 RGB LED 3핀
PED_RED = 23
PED_GREEN = 24

PED_BUTTON = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(CAR_GREEN, GPIO.OUT)
GPIO.setup(CAR_YELLOW, GPIO.OUT)
GPIO.setup(CAR_RED, GPIO.OUT)
GPIO.setup(PED_GREEN, GPIO.OUT)
GPIO.setup(PED_RED, GPIO.OUT)
GPIO.setup(PED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

timers = {
    "car_green": 5,
    "car_yellow": 1,
    "car_red": 2,
    "ped_green": 2,
    "ped_red": 6
}

signal_state = {
    "car": "green",
    "ped": "red",
    "override": False
}

def set_car_light(color):
    GPIO.output(CAR_GREEN, color == "green")
    GPIO.output(CAR_YELLOW, color == "yellow")
    GPIO.output(CAR_RED, color == "red")

def set_ped_light(color):
    GPIO.output(PED_GREEN, color == "green")
    GPIO.output(PED_RED, color == "red")
def traffic_light_cycle():
    while True:
        if not signal_state["override"]:
            signal_state["car"] = "green"
            signal_state["ped"] = "red"
            set_car_light("green")
            set_ped_light("red")
            for _ in range(timers["car_green"]):
                if signal_state["override"]:
                    break
                time.sleep(1)
            if signal_state["override"]:
                continue
\
            signal_state["car"] = "yellow"
            signal_state["ped"] = "red"
            set_car_light("yellow")
            set_ped_light("red")
            for _ in range(timers["car_yellow"]):
                if signal_state["override"]:
                    break
                time.sleep(1)
            if signal_state["override"]:
                continue
            
            signal_state["car"] = "red"
            signal_state["ped"] = "green"
            set_car_light("red")
            set_ped_light("green")
            for _ in range(timers["car_red"]):
                if signal_state["override"]:
                    break
                time.sleep(1)
            if signal_state["override"]:
                continue

            signal_state["car"] = "red"
            signal_state["ped"] = "red"
            set_car_light("red")
            set_ped_light("red")
            for _ in range(timers["ped_red"]):
                if signal_state["override"]:
                    break
                time.sleep(1)
        else:
            time.sleep(5)
            signal_state["override"] = True
            signal_state["car"] = "red"
            signal_state["ped"] = "green"
            set_car_light("red")
            set_ped_light("green")
            for _ in range(timers["ped_green"]):
                time.sleep(1)
            signal_state["car"] = "red"
            signal_state["ped"] = "red"
            set_car_light("red")
            set_ped_light("red")
            for _ in range(timers["ped_red"]):
                time.sleep(1)
            signal_state["override"] = False


def button_listener():
    while True:
        input_state = GPIO.input(PED_BUTTON)
        if input_state == False:
            if not signal_state["override"]:
                print("횡단보도 버튼 눌림!")
                signal_state["override"] = True
            time.sleep(0.5)
        time.sleep(0.1)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        try:
            timers["car_green"] = int(request.form.get("car_green", timers["car_green"]))
            timers["car_yellow"] = int(request.form.get("car_yellow", timers["car_yellow"]))
            timers["car_red"] = int(request.form.get("car_red", timers["car_red"]))
            timers["ped_green"] = int(request.form.get("ped_green", timers["ped_green"]))
            timers["ped_red"] = int(request.form.get("ped_red", timers["ped_red"]))
        except ValueError:
            pass
        return redirect('/admin')

    return render_template('admin.html', timers=timers, signal_state=signal_state)

if __name__ == '__main__':
    try:
        set_car_light("green")
        set_ped_light("red")

        thread_traffic = threading.Thread(target=traffic_light_cycle, daemon=True)
        thread_traffic.start()

        thread_button = threading.Thread(target=button_listener, daemon=True)
        thread_button.start()

        app.run(host='0.0.0.0', port=5000)

    finally:
        GPIO.cleanup()
