import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter)

class Map(QWidget):
    def __init__(self):
        super(Map, self).__init__()

        vbox = QVBoxLayout(self)

        pixmap = QPixmap("images/map.png") 
        pixmap = pixmap.scaled(1000, 1000, Qt.KeepAspectRatio)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        lbl.setMinimumSize(10, 10)
        
        vbox.addWidget(lbl)

        self.setLayout(vbox)

class Splitter(QWidget):

    def __init__(self, map):
        super(Splitter, self).__init__()

        vbox = QVBoxLayout(self)
        
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)

        hbox = QHBoxLayout(right)
        hbox.addWidget(map)
        right.setLayout(hbox)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        vbox.addWidget(splitter)

        self.setLayout(vbox)


class MainWindow(QMainWindow):
    def __init__(self, splitter):
        QMainWindow.__init__(self)
        self.setWindowTitle("4CASTX")
        self.setCentralWidget(splitter)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Cleanlooks'))

    map = Map()
    split = Splitter(map)
    window = MainWindow(split)
    window.setGeometry(300, 300, 1500, 900)
    window.show()

    sys.exit(app.exec())
