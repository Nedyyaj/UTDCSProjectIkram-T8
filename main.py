import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame)

#window

#widgets? for map panel and navigation panel
#navigation panel
#leave map panel blank for now
#back button to go back to previous menu

class Widget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        #TODO: put all these buttons into arrays or smn idk how python works
        self.r1 = QPushButton("Region 1")
        self.r2 = QPushButton("Region 2")
        self.r3 = QPushButton("Region 3")

        self.r1c1 = QPushButton("Region 1: City 1")
        self.r1c2 = QPushButton("Region 1: City 2")
        self.r1c3 = QPushButton("Region 1: City 3")
        self.r2c1 = QPushButton("Region 2: City 1")
        self.r2c2 = QPushButton("Region 2: City 2")
        self.r2c3 = QPushButton("Region 2: City 3")
        self.r3c1 = QPushButton("Region 3: City 1")
        self.r3c2 = QPushButton("Region 3: City 2")
        self.r3c3 = QPushButton("Region 3: City 3")

        self.info_region = QLabel("Select region:")
        self.info_region.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.info_city = QLabel("Select city:")
        self.info_city.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.info_data11 = QLabel("Region 1 City 1 data here")
        self.info_data12 = QLabel("Region 1 City 2 data here")
        self.info_data13 = QLabel("Region 1 City 3 data here")
        self.info_data21 = QLabel("Region 2 City 1 data here")
        self.info_data22 = QLabel("Region 2 City 2 data here")
        self.info_data23 = QLabel("Region 2 City 3 data here")
        self.info_data31 = QLabel("Region 3 City 1 data here")
        self.info_data32 = QLabel("Region 3 City 2 data here")
        self.info_data33 = QLabel("Region 3 City 3 data here")

        self.map = QLabel("Map goes here")
        self.map.setAlignment(Qt.AlignCenter)
        self.map.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        self.left = QVBoxLayout()
        self.left.addWidget(self.info_region, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.left.addWidget(self.r1, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.left.addWidget(self.r2, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.left.addWidget(self.r3, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.layout = QHBoxLayout(self)
        self.layout.addLayout(self.left)
        self.layout.addWidget(self.map)

        self.r1.clicked.connect(lambda x: self.show_cities(1))
        self.r2.clicked.connect(lambda x: self.show_cities(2))
        self.r3.clicked.connect(lambda x: self.show_cities(3))

        self.r1c1.clicked.connect(lambda x: self.show_data(1, 1))
        self.r1c2.clicked.connect(lambda x: self.show_data(1, 2))
        self.r1c3.clicked.connect(lambda x: self.show_data(1, 3))

        self.r2c1.clicked.connect(lambda x: self.show_data(2, 1))
        self.r2c2.clicked.connect(lambda x: self.show_data(2, 2))
        self.r2c3.clicked.connect(lambda x: self.show_data(2, 3))

        self.r3c1.clicked.connect(lambda x: self.show_data(3, 1))
        self.r3c2.clicked.connect(lambda x: self.show_data(3, 2))
        self.r3c3.clicked.connect(lambda x: self.show_data(3, 3))

    @Slot()
    def show_cities(self, region_id):
        self.left.removeWidget(self.info_region)
        self.left.removeWidget(self.r1)
        self.left.removeWidget(self.r2)
        self.left.removeWidget(self.r3)
        self.info_region.hide()
        self.r1.hide()
        self.r2.hide()
        self.r3.hide()
        if(region_id == 1):
            self.left.addWidget(self.info_city, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r1c1, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r1c2, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r1c3, alignment=Qt.AlignLeft | Qt.AlignTop)
        if(region_id == 2):
            self.left.addWidget(self.info_city, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r2c1, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r2c2, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r2c3, alignment=Qt.AlignLeft | Qt.AlignTop)
        if(region_id == 3):
            self.left.addWidget(self.info_city, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r3c1, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r3c2, alignment=Qt.AlignLeft | Qt.AlignTop)
            self.left.addWidget(self.r3c3, alignment=Qt.AlignLeft | Qt.AlignTop)

    @Slot()
    def show_data(self, region_id, city_id):
        self.left.removeWidget(self.info_city)
        self.info_city.hide()
        if(region_id == 1):
            self.left.removeWidget(self.r1c1)
            self.left.removeWidget(self.r1c2)
            self.left.removeWidget(self.r1c3)
            self.r1c1.hide()
            self.r1c2.hide()
            self.r1c3.hide()
            if(city_id == 1):
                self.left.addWidget(self.info_data11)
            if(city_id == 2):
                self.left.addWidget(self.info_data12)
            if(city_id == 3):
                self.left.addWidget(self.info_data13)
        if(region_id == 2):
            self.left.removeWidget(self.r2c1)
            self.left.removeWidget(self.r2c2)
            self.left.removeWidget(self.r2c3)
            self.r2c1.hide()
            self.r2c2.hide()
            self.r2c3.hide()
            if(city_id == 1):
                self.left.addWidget(self.info_data21)
            if(city_id == 2):
                self.left.addWidget(self.info_data22)
            if(city_id == 3):
                self.left.addWidget(self.info_data23)
        if(region_id == 3):
            self.left.removeWidget(self.r3c1)
            self.left.removeWidget(self.r3c2)
            self.left.removeWidget(self.r3c3)
            self.r3c1.hide()
            self.r3c2.hide()
            self.r3c3.hide()
            if(city_id == 1):
                self.left.addWidget(self.info_data31)
            if(city_id == 2):
                self.left.addWidget(self.info_data32)
            if(city_id == 3):
                self.left.addWidget(self.info_data33)






class MainWindow(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("4CASTX")

        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = Widget()
    window = MainWindow(widget)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
