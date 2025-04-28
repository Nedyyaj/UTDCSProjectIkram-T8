import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap, QIcon
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)
from map import Map, MapCanvas
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


# --------------------------------------------------------------
# Color Palette for application
# --------------------------------------------------------------
# Primary Color: #3674B5
# Secondary Color: #578FCA
# Tertiary Color: #A1E3F9
# Background Color: #D1F8EF

# Extra Dark Colors
# Darker Blue: #003092

# Notes: 
# Black #000000
# White #FFFFFF
# --------------------------------------------------------------


class MainWindow(QMainWindow):
    def __init__(self, splitter):
        QMainWindow.__init__(self)
        self.setWindowTitle("4CASTX")
        
        self.setCentralWidget(splitter)
        
        # Color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #578FCA;  /* Background color */
                color: #000000;  /* Text color */
            }
            QWidget {
                background-color: #3674B5;  /* Background color */
                color: #000000;  /* Text color */
            }
            QSplitter{
                background-color: #578FCA;  /* Background color */
            }

            QMainWindow {
                background-color: #3674B5;  /* Background color */
                color: #000000;  /* Text color */
            }
            
            QLabel {
                background-color: #578FCA;  /* Label background color */
                color: #000000;  /* Label text color */
            }

            QPushButton {
                background-color: #578FCA;  /* Button color */
                color: #FFFFFF;  /* Button text color */
                border: 1px solid #000000;  /* Table border color */
            }
            QPushButton:hover {
                background-color: #A1E3F9;  /* Button hover color */ }
                color: #000000;  /* Button text color */
                border: 1px solid #000000;  /* Table border color */
            
            QTableView {
                background-color: #A1E3F9;  /* Table background color */
                color: #000000;  /* Table text color */
            }
            QTableView::item {
                background-color: #A1E3F9;  /* Table item background color */
                color: #000000;  /* Table item text color */
            }


        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Cleanlooks'))
    app.setWindowIcon(QIcon("images/4CASTX Logo.png"))          # This isn't working, need to fix it later
    panel = DataPanel()
    canvas = MapCanvas(panel)
    map = Map(canvas)
    split = Splitter(map, panel)
    window = MainWindow(split)
    window.resize(1500, 900)
    window.show()

    sys.exit(app.exec())
