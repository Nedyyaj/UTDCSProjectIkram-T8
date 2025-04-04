import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)
from map import Map
from datapanel import DataPanel

def LDEBUG(message):
    print(f"[DEBUG]: {message}")

def LERROR(message):
    print(f"[ERROR]: {message}")



class Splitter(QWidget):

    def __init__(self, map, data_panel):
        super(Splitter, self).__init__()

        vbox = QVBoxLayout(self)
        
        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        lvbox = QVBoxLayout(left)
        lvbox.addWidget(data_panel)
        left.setLayout(lvbox)
        left.setMinimumWidth(250)

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)
        rhbox = QHBoxLayout(right)
        rhbox.addWidget(map)
        right.setLayout(rhbox)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)
        right.setMinimumWidth(700)

        vbox.addWidget(splitter)

        self.setLayout(vbox)
        splitter.setChildrenCollapsible(False)


class MainWindow(QMainWindow):
    def __init__(self, splitter):
        QMainWindow.__init__(self)
        self.setWindowTitle("4CASTX")
        self.setCentralWidget(splitter)
        
        self.back_click = QAction("Back", self)
        self.back_click.setShortcut('Q')

        self.toolbar = self.addToolBar("Back")
        self.toolbar.addAction(self.back_click)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Cleanlooks'))

    panel = DataPanel()
    map = Map()
    split = Splitter(map, panel)
    window = MainWindow(split)
    window.back_click.triggered.connect(panel.back_click)
    window.resize(1500, 900)
    window.show()

    sys.exit(app.exec())
