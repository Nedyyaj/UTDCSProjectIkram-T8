import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

import geopandas

def LDEBUG(message):
    print(f"[DEBUG]: {message}")

def LERROR(message):
    print(f"[ERROR]: {message}")

class Map(FigureCanvas):
    def __init__(self):
        super(Map, self).__init__()

        fig = Figure(dpi=100)
        self.figure = fig
        self.canvas = FigureCanvas(self.figure)
        self.axes=fig.add_subplot()
        counties = geopandas.read_file(r"map\Select Counties\selected.shp")
        counties = counties.to_crs("EPSG:3395")
        counties.boundary.plot(ax=self.axes)
        #self.axes.plot(counties)
        self.draw()

        
'''
        pixmap = QPixmap("images/map.png") 
        pixmap = pixmap.scaled(1000, 1000, Qt.KeepAspectRatio)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        lbl.setMinimumSize(10, 10)
        
        vbox.addWidget(lbl)
'''



class DataPanel(QWidget):
    def __init__(self):
        super(DataPanel, self).__init__()

        self.state = "regions"
        self.region = 0
        self.city = 0
        self.rows, self.cols = (6, 5)

        grid = QGridLayout(self)

        self.data = QLabel("data goes here")
        
        self.b_list = [[0 for i in range(self.cols)] for j in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                if i == 0:
                    self.b_list[i][j] = QPushButton(f"Region {j+1}")
                else:
                    self.b_list[i][j] = QPushButton(f"Region {i}, City {j+1}")

                self.b_list[i][j].setFixedSize(200, 40)
                self.b_list[i][j].clicked.connect(lambda state, i=i, j=j:self.button_click(i, j))
                if i != 0:
                    self.b_list[i][j].hide()
                grid.addWidget(self.b_list[i][j], j, 0, alignment=Qt.AlignTop | Qt.AlignLeft)

        for k in range(10):
            grid.addWidget(QLabel(""))        
        
        grid.addWidget(self.data, 0, 0)
        self.data.hide()
        self.setLayout(grid)

    @Slot()
    def button_click(self, row, col):
        LDEBUG(f"button_click: row={row}, col={col}")
        if row == 0:
            self.state = "cities"
            self.region = col+1


        else:
            self.state = "data"
            self.city = col+1

        self.config_panel()
        LDEBUG(f"status: {self.state}, region: {self.region}, city: {self.city}")


    @Slot()
    def back_click(self):
        if self.state == "cities":
            self.region = 0
            self.state = "regions"
        if self.state == "data":
            self.state = "cities"
            self.city = 0

        self.config_panel()
        LDEBUG(f"status: {self.state}, region: {self.region}, city: {self.city}")


    def config_panel(self):
        if self.state == "regions":
            for i in range(self.rows):
                for j in range(self.cols):
                    if i == 0:
                        self.b_list[i][j].show()
                    else:
                        self.b_list[i][j].hide()

            self.data.hide()

        if self.state == "cities":
            for i in range(self.rows):
                for j in range(self.cols):
                    if i == self.region:
                        self.b_list[i][j].show()
                    else:
                        self.b_list[i][j].hide()

            self.data.hide()

        if self.state == "data":
            for i in range(self.rows):
                for j in range(self.cols):
                    self.b_list[i][j].hide()

            self.data.show()


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
