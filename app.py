from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QPushButton, QTextBrowser
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication)
import numpy as np
from tensorflow import keras


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "recognition cyrillic letter"
        top = 200
        left = 200
        width = 540
        height = 340

        self.drawing = False
        self.brushSize = 8
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        self.image = QImage(278, 278, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('RES:')
        self.line = QLineEdit(self)

        self.line.move(360, 168)
        self.line.resize(80, 33)
        self.nameLabel.move(290, 170)

        prediction_button = QPushButton('RECOGNITION', self)
        prediction_button.move(290, 30)
        prediction_button.resize(230, 33)
        prediction_button.clicked.connect(self.save)
        prediction_button.clicked.connect(self.predicting)

        clean_button = QPushButton('CLEAN', self)
        clean_button.move(290, 100)
        clean_button.resize(230, 33)
        clean_button.clicked.connect(self.clear)

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

    def print_letter(self, result):
        if result == 1:
            self.line.setText('А')
            return 'А'

        elif result == 2:
            self.line.setText('Б')
            return 'Б'

        elif result == 3:
            self.line.setText('В')
            return 'В'

        elif result == 4:
            self.line.setText('Г')
            return 'Г'

        elif result == 5:
            self.line.setText('Д')
            return 'Д'

        elif result == 6:
            self.line.setText('Е')
            return 'Е'

        elif result == 7:
            self.line.setText('Ж')
            return 'Ж'

        elif result == 0:
            self.line.setText('Ё')
            return 'Ё'

        elif result == 8:
            self.line.setText('З')
            return 'З'

        elif result == 9:
            self.line.setText('И')
            return 'И'

        elif result == 10:
            self.line.setText('Й')
            return 'Й'

        elif result == 11:
            self.line.setText('К')
            return 'К'

        elif result == 12:
            self.line.setText('Л')
            return 'Л'

        elif result == 13:
            self.line.setText('М')
            return 'М'

        elif result == 14:
            self.line.setText('Н')
            return 'Н'

        elif result == 15:
            self.line.setText('О')
            return 'О'

        elif result == 16:
            self.line.setText('П')
            return 'П'

        elif result == 17:
            self.line.setText('Р')
            return 'Р'

        elif result == 18:
            self.line.setText('С')
            return 'С'

        elif result == 19:
            self.line.setText('Т')
            return 'Т'

        elif result == 20:
            self.line.setText('У')
            return 'У'

        elif result == 21:
            self.line.setText('Ф')
            return 'Ф'

        elif result == 22:
            self.line.setText('Х')
            return 'Х'

        elif result == 23:
            self.line.setText('Ц')
            return 'Ц'

        elif result == 24:
            self.line.setText('Ч')
            return 'Ч'

        elif result == 25:
            self.line.setText('Ш')
            return 'Ш'

        elif result == 26:
            self.line.setText('Щ')
            return 'Щ'

        elif result == 27:
            self.line.setText('Ъ')
            return 'Ъ'

        elif result == 28:
            self.line.setText('Ы')
            return 'Ы'

        elif result == 29:
            self.line.setText('Ь')
            return 'Ь'

        elif result == 30:
            self.line.setText('Э')
            return 'Э'

        elif result == 31:
            self.line.setText('Ю')
            return 'Ю'

        elif result == 32:
            self.line.setText('Я')
            return 'Я'

        else:
            print('ERROR!')

    def predicting(self):
        image = keras.preprocessing.image
        model = keras.models.load_model('model/cyrillic_model.h5')
        img = image.load_img('res.jpeg', target_size=(278, 278))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        classes = model.predict(images, batch_size=1)
        result = int(np.argmax(classes))
        self.print_letter(result)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(0, 0, self.image)

    def save(self):
        self.image.save('res.jpeg')

    def clear(self):
        self.image.fill(Qt.white)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
