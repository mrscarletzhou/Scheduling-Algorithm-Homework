from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QFileDialog, QMessageBox, QTableWidgetItem, QLabel, \
	QAbstractItemView
from PyQt5.QtCore import pyqtSignal, pyqtSlot,QSize, Qt
from PyQt5.QtGui import QMovie, QFont
from PyQt5 import QtCore

from threading import Thread,Event
import time
import sys


gif_path = 'car2.gif'


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		loadUi('MainWindow.ui', self)
		self.retranslateUi()
		self.binding()

		self.track_width = 600
		self.cpu_res = 1  # 模拟只有一个处理器情况
		self.active_thread_num = 3  # 设置线程数3

		self.thread1 = Thread(target=self.move, args=(self.label_a,))
		self.thread2 = Thread(target=self.move, args=(self.label_b,))
		self.thread3 = Thread(target=self.move, args=(self.label_c,))

		self.thread1.setDaemon(True)  # 设置主线程为守护线程
		self.thread2.setDaemon(True)
		self.thread3.setDaemon(True)

		self.thread1.start()
		self.thread2.start()
		self.thread3.start()
		self.threads=[self.thread1,self.thread2,self.thread3]

	def retranslateUi(self):
		self.gif_a = QMovie(gif_path)
		self.gif_b = QMovie(gif_path)
		self.gif_c = QMovie(gif_path)

		self.gif_a.setScaledSize(QSize(200,150))
		self.gif_b.setScaledSize(QSize(200,150))
		self.gif_c.setScaledSize(QSize(200,150))

		self.label_a.resize(200,150)
		self.label_b.resize(200,150)
		self.label_c.resize(200,150)

		self.label_a.setMovie(self.gif_a)
		self.label_b.setMovie(self.gif_b)
		self.label_c.setMovie(self.gif_c)

		self.gif_a.start()
		self.gif_b.start()
		self.gif_c.start()

		self.labeli_3 = QLabel(self)

		# qle = QLineEdit(self)

		self.labels = [self.label_a, self.label_b, self.label_c]


		for label in self.labels:
			label.suspended=Event()
			label.suspended.set()

		# self.label_name.setText(sys.argv[1])
	# 		# self.label_sid.setText(sys.argv[2])

	def binding(self):
		self.pushButton_a_suspend.clicked.connect(self.pushButton_a_suspendClicked)  # 暂停按钮
		self.pushButton_b_suspend.clicked.connect(self.pushButton_b_suspendClicked)
		self.pushButton_c_suspend.clicked.connect(self.pushButton_c_suspendClicked)

		self.pushButton_a_resume.clicked.connect(self.pushButton_a_resumeClicked)  # 恢复按钮
		self.pushButton_b_resume.clicked.connect(self.pushButton_b_resumeClicked)
		self.pushButton_c_resume.clicked.connect(self.pushButton_c_resumeClicked)

	def get(self):
		print(self.cpu_res / self.active_thread_num)
		return self.cpu_res / self.active_thread_num

	def printV(self,speed):
		self.labeli_3.setText("当前最大速度为="+speed[:4])
		self.labeli_3.setFixedWidth(400)
		self.labeli_3.setAlignment(Qt.AlignCenter)
		self.labeli_3.move(300, 500)
		self.labeli_3.setFont(QFont("Timers", 14, QFont.Bold))

	def move(self, label):
		while True:
			label.suspended.wait()
			#print(f'{label.suspended.is_set()}')
			try:
				x = label.geometry().x()
				speed = self.get()
				# print(speed)
				x += speed * 100
				if x > 450:
					x = 0
				label.movie().setSpeed(speed*100)
				label.move(x, 0)
				self.printV(str(speed))
				# labeli[0].setText("V=" + speed)
				# print(x)
				time.sleep(1)
			except BaseException as e:
				print(e)

	def suspend(self,index):
		label = self.labels[index]
		if not label.suspended.is_set():
			return
		self.active_thread_num -= 1
		self.labels[index].suspended.clear()

	def pushButton_a_suspendClicked(self):
		self.suspend(0)

	def pushButton_b_suspendClicked(self):
		self.suspend(1)
	def pushButton_c_suspendClicked(self):
		self.suspend(2)

	def resume(self,index):
		label=self.labels[index]
		if label.suspended.is_set():
			return
		self.active_thread_num+=1
		self.labels[index].suspended.set()

	def pushButton_a_resumeClicked(self):
		self.resume(0)
	def pushButton_b_resumeClicked(self):
		self.resume(1)
	def pushButton_c_resumeClicked(self):
		self.resume(2)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainwindow = MainWindow()
	# mainwindow.resize(1000, 600)
	mainwindow.show()
	app.exec()
