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
        self.line.resize(99, 42)
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

    def print_letter(self,result):
        letters = "ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.line.setText(letters[result])
        return letters[result]

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
