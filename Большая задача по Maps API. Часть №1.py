import os
import sys
import shutil
import requests
from PyQt5 import QtCore, QtWidgets, QtGui



class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 450, 450)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QtGui.QPixmap(self.map_file)
        self.image = QtWidgets.QLabel(self)
        self.image.resize(450, 450)
        self.image.setPixmap(self.pixmap)

    def getImage(self):
        response = requests.request(method='GET',
                                    url='https://static-maps.yandex.ru/1.x/',
                                    params={
                                        'll': '50.191374,53.217203',
                                        'spn': '0.001500,0.001500',
                                        'l': 'sat',
                                        'size': '450,450'
                                    })

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        try:
            open('data/map.png')
        except:
            os.mkdir('data')

        self.map_file = "data/map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def closeEvent(self, event):
        shutil.rmtree('data')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())