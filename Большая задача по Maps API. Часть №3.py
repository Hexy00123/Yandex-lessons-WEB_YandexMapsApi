import sys
import shutil
import requests
from PyQt5 import QtCore, QtWidgets, QtGui, Qt


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.map_size = 17
        self.ll = [50.191374, 53.217203]

        self.get_image()
        self.initUI()
        self.update()

    def initUI(self):
        self.setGeometry(100, 100, 450, 450)
        self.setWindowTitle('Большая задача по яндекс картам')

        self.pixmap = QtGui.QPixmap()
        self.image = QtWidgets.QLabel(self)
        self.image.resize(450, 450)

    def get_image(self):
        response = requests.request(method='GET',
                                    url='https://static-maps.yandex.ru/1.x/',
                                    params={
                                        'll': f'{self.ll[0]},{self.ll[1]}',
                                        'z': f'{self.map_size}',
                                        'l': 'sat',
                                        'size': '450,450'
                                    })

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        return response.content

    def update(self):
        image = self.get_image()
        self.pixmap.loadFromData(image)

        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        move_value = 180 / (2 ** self.map_size)
        if event.key() == 16777238:  # pgup
            if self.map_size + 1 <= 17:
                self.map_size += 1
        elif event.key() == 16777239:  # pgdown
            if self.map_size - 1 >= 1:
                self.map_size -= 1

        elif event.key() == 16777235:  # up
            self.ll[1] += move_value
        elif event.key() == 16777237:  # down
            self.ll[1] -= move_value
        elif event.key() == 16777234:  # left
            self.ll[0] -= move_value
        elif event.key() == 16777236:  # right
            self.ll[0] += move_value

        self.update()
        event.accept()

    def closeEvent(self, event):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
