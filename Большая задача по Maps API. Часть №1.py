import os
import sys
import requests
from PyQt5 import QtCore, QtWidgets, QtGui


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('Example')

        self.label = QtWidgets.QLabel('', self)
        self.counter = 0

    def keyPressEvent(self, event):
        print(event.key())

        if event.key() == QtCore.Qt.Key_Q:
            self.counter += 1
            self.label.setText(f'Клавиша Q нажата {str(self.counter)} раз')
            print(self.counter)
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())
