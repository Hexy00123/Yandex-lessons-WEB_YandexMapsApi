import math
import sys
import requests
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.map_size = 17
        self.ll = [50.191374, 53.217203]
        self.l = 'sat'
        self.pt = []
        self.setMouseTracking(True)
        self.get_image()
        self.initUI()
        self.update()
        self.center = [224, 273]

    def initUI(self):
        self.setGeometry(100, 100, 450, 550)
        self.setWindowTitle('Большая задача по яндекс картам')

        self.pixmap = QtGui.QPixmap()
        self.image = QtWidgets.QLabel(self)
        self.image.move(0, 50)
        self.image.resize(450, 450)

        self.rad_buttons = []
        for num, text in enumerate(['Спутник', 'Карта', 'Гибрид']):
            button = QtWidgets.QRadioButton(self)
            if num == 0:
                button.setChecked(True)
            button.setText(text)
            button.move(350, num * 15)
            button.released.connect(self.update_type_of_map)
            button.setFocusPolicy(QtCore.Qt.NoFocus)
            self.rad_buttons.append(button)

        self.line_edit = QtWidgets.QLineEdit(self)
        self.line_edit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.line_edit.setGeometry(5, 5, 150, 40)
        self.line_edit.setText('москва петровки 38')

        self.button_search = QtWidgets.QPushButton(self, text='Искать')
        self.button_search.setGeometry(160, 5, 60, 40)
        self.button_search.clicked.connect(self.search)

        self.button_delete = QtWidgets.QPushButton(self, text='Сброс ')
        self.button_delete.setGeometry(225, 5, 60, 40)
        self.button_delete.clicked.connect(self.delete)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(5, 500, 400, 50)

        # self.is_index = QtWidgets.QCheckBox(self, text='Отображение почтового\n индекса')
        # self.is_index.move(300, 515)
        # self.is_index.clicked.connect(self.search)

    def get_image(self):
        response = requests.request(method='GET',
                                    url='https://static-maps.yandex.ru/1.x/',
                                    params={
                                        'll': f'{self.ll[0]},{self.ll[1]}',
                                        'z': f'{self.map_size}',
                                        'l': f'{self.l}',
                                        'size': '450,450',
                                        'pt': ''.join(self.pt)
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

    def update_type_of_map(self):
        if self.sender().underMouse():
            text = self.sender().text()
            if text == 'Спутник':
                self.l = 'sat'
            elif text == 'Гибрид':
                self.l = 'map'
            elif text == 'Карта':
                self.l = 'skl'
            self.update()

    def search(self):
        self.delete()
        if self.line_edit.text():
            response = requests.request(method='GET',
                                        url='https://geocode-maps.yandex.ru/1.x',
                                        params={
                                            'geocode': self.line_edit.text(),
                                            'format': 'json',
                                            'apikey': self.apikey,

                                        })
            if response.status_code == 200:
                result = response.json()['response']['GeoObjectCollection']['featureMember'][0][
                    'GeoObject']
                coords = list(map(float, result['Point']['pos'].split()))
                addres = result['metaDataProperty']['GeocoderMetaData']['text']
                self.ll = coords
                self.label.setText(f'Адрес: {addres}')
                if f'{coords[0]},{coords[1]},round' not in self.pt:
                    self.pt = []
                    self.pt.append(f'{coords[0]},{coords[1]},round')
                self.update()

    def delete(self):
        if self.line_edit.text():
            response = requests.request(method='GET',
                                        url='https://geocode-maps.yandex.ru/1.x',
                                        params={
                                            'geocode': self.line_edit.text(),
                                            'format': 'json',
                                            'apikey': self.apikey,

                                        })

            if response.status_code == 200:
                self.label.setText('')
                coords = list(map(float, response.json()['response']['GeoObjectCollection'][
                    'featureMember'][0][
                    'GeoObject']['Point']['pos'].split()))
                self.ll = coords
                if f'{coords[0]},{coords[1]},round' in self.pt:
                    self.pt.remove(f'{coords[0]},{coords[1]},round')
                    self.update()

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

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.line_edit.clearFocus()
        self.button_search.clearFocus()
        self.button_delete.clearFocus()
        self.clickOnMap(a0)

    def clickOnMap(self, a0):
        if a0.button() == Qt.LeftButton:
            l_x = (a0.x() - self.center[0]) / 100000
            l_y = (a0.y() - self.center[1]) / 150000
            self.pt = [f'{self.ll[0] + l_x},{self.ll[1] - l_y},round']
            response = requests.request(method='GET',
                                        url='https://static-maps.yandex.ru/1.x/',
                                        params={
                                            'll': f'{self.ll[0]},{self.ll[1]}',
                                            'z': f'{self.map_size}',
                                            'l': f'{self.l}',
                                            'size': '450,450',
                                            'pt': ''.join(self.pt)
                                        })
            req = requests.request(method='GET',
                                   url='https://geocode-maps.yandex.ru/1.x',
                                   params={
                                       'geocode': ','.join([str(self.ll[0] + l_x), str(self.ll[1] - l_y)]),
                                       'format': 'json',
                                       'apikey': self.apikey,

                                   })
            if req.status_code == 200:
                addres = \
                    req.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                        'GeocoderMetaData']['text']
                self.label.setText(f'Адрес: {addres.replace(",", "")}')
                self.line_edit.setText(addres.replace(",", ""))
            image = response.content
            self.pixmap.loadFromData(image)
            self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Window()
    form.show()
    sys.exit(app.exec())
