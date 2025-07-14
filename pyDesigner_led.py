import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED = 14
GREEN = 15
BLUE = 18

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)


class WindowClass(QDialog):
	def __init__(self, parent=None):
		super().__init__()
		self.ui = uic.loadUi("designer_led.ui", self)
		self.ui.show()

	def slot1(self):
		GPIO.output(RED, GPIO.LOW)
		GPIO.output(GREEN, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.HIGH)

	def slot2(self):
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(GREEN, GPIO.LOW)
		GPIO.output(BLUE, GPIO.HIGH)

	def slot3(self):
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(GREEN, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.LOW)

	def slot4(self):
		GPIO.output(RED, GPIO.HIGH)
		GPIO.output(GREEN, GPIO.HIGH)
		GPIO.output(BLUE, GPIO.HIGH)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = WindowClass()
	app.exec_()
	
