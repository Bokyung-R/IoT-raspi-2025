import sys
from PyQt5.QtWidgets import QApplication, QWidget

class MyApp(QWidget):
	def __init__(self):
		super().__init__()
		self.initUi()

	def initUi(self):
		self.setWindowTitle("My First Application")
		self.move(300,300)			# 위젯이동
		self.resize(400,200)			# 위젯크기
		self.show()						# 위젯 뷰

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = MyApp()
	sys.exit(app.exec_())
