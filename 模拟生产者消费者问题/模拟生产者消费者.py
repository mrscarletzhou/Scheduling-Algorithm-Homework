import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton , QLabel
from PyQt5.QtCore import QBasicTimer, Qt


maxnum = 6

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.label_1 = QLabel(self)
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setPixmap(QPixmap("hamburger.jpg").scaled(60,60))
        self.label_1.move(410,3)
        self.label_1.setVisible(False)

        self.label_2 = QLabel(self)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setPixmap(QPixmap("hamburger.jpg").scaled(60,60))
        self.label_2.move(410, 66)
        self.label_2.setVisible(False)

        self.label_3 = QLabel(self)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setPixmap(QPixmap("hamburger.jpg").scaled(60,60))
        self.label_3.move(410, 129)
        self.label_3.setVisible(False)

        self.label_4 = QLabel(self)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setPixmap(QPixmap("hamburger.jpg").scaled(60,60))
        self.label_4.move(410, 192)
        self.label_4.setVisible(False)

        self.label_5 = QLabel(self)
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setPixmap(QPixmap("hamburger.jpg").scaled(60, 60))
        self.label_5.move(410, 255)
        self.label_5.setVisible(False)

        self.label_6 = QLabel(self)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.label_6.setPixmap(QPixmap("hamburger.jpg").scaled(60, 60))
        self.label_6.move(410, 318)
        self.label_6.setVisible(False)

        self.labels = [self.label_1,self.label_2, self.label_3, self.label_4, self.label_5, self.label_6]

        self.label2 = QLabel(self)
        self.label2.resize(200,30)
        self.label2.setText("仓库为空")
        self.label2.setFont(QFont("Timers", 12, QFont.Bold))
        self.label2.move(60, 340)


        self.initUI()

    def initUI(self):

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 50, 300, 40)

        self.btn = QPushButton('开始', self)
        self.btn.resize(100, 40)
        self.btn.move(30, 100)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.pbar2 = QProgressBar(self)
        self.pbar2.setGeometry(30, 200, 300, 40)

        self.btn2 = QPushButton('开始', self)
        self.btn2.resize(100, 40)
        self.btn2.move(30, 250)
        self.btn2.clicked.connect(self.doAction2)

        self.timer2 = QBasicTimer()
        self.step2 = 0

        self.count = 0

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('生产者消费者')
        self.show()

    def timerEvent(self, e):
        # print(e.timerId())
        if self.count == maxnum:
            self.timer.stop()
            self.label2.setText("仓库已满")
            self.btn.setText("不可用")
            self.btn2.setText("可用")
        elif self.count == 0:
            self.timer2.stop()
            self.label2.setText("仓库已空")
            self.btn2.setText("不可用")
            self.btn.setText("可用")
        elif maxnum > self.count > 0:
            self.label2.setText("仓库剩余商品"+str(self.count)+"件")
            self.btn.setText("可用")
            self.btn2.setText("不可用")
        if e.timerId() == self.timer.timerId():
            if self.step >= 100:
                self.count = self.count + 1
                self.step = 0
                self.labels[self.count-1].setVisible(True)
                return
            self.step = self.step + 1
            self.pbar.setValue(self.step)

        if e.timerId() == self.timer2.timerId():
            if self.step2 >= 100:
                self.step2 = 0
                self.count = self.count - 1
                self.labels[self.count-1].setVisible(False)
                return
            self.step2 = self.step2 + 1
            self.pbar2.setValue(self.step2)



    def doAction(self, value):

        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('开始')
        else:
            self.timer.start(10, self)
            self.btn.setText('停止')

    def doAction2(self, value):
        if self.timer2.isActive():
            self.timer2.stop()
            self.btn2.setText('开始')
        else:
            self.timer2.start(5, self)
            self.btn2.setText('停止')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())