import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap, QPainter, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout, QGraphicsGridLayout, QGraphicsProxyWidget, QGraphicsScene, QGraphicsWidget, QGraphicsView, QSizePolicy, QLineEdit, QFormLayout, QTableView, QStackedLayout, QTabWidget, QTableWidgetItem, QTableWidget, QComboBox, QCheckBox, QRadioButton, QTextEdit, QScrollArea, QFileDialog)
import pandas as pd
import pickle as pkl

# #with open(''../backend/deep learning/trained_forecaster.pkl', 'wb+') as f:
#     pickle.dump(forecast_model, f)


def LDEBUG(message):
    print(f"[DEBUG]: {message}")


df = pd.read_csv("../backend/preprocessing/county_variables.csv")
#pkl = 

county_stations = {
    'Tarrant', 'McLennan', 'Montague', 'Stephens', 'Wise', 'Johnson', 'Comanche', 'Navarro', 'Dallas', 'Denton', 'Cooke',
    'Coryell', 'Young', 'Hood', 'Hunt', 'Hamilton', 'Hill', 'Collin', 'Palo Pinto', 'Grayson', 'Erath', 'Kaufman',  'Ellis',
    'Eastland', 'Jack', 'Parker', 'Rockwall', 'Somervell', 'Bosque'
}

county_dict = {
    'Tarrant': 1, 
    'McLennan': 2, 
    'Montague': 3, 
    'Stephens': 4, 
    'Wise': 5, 
    'Johnson': 6, 
    'Comanche': 7, 
    'Navarro': 8, 
    'Dallas': 9, 
    'Denton': 10, 
    'Cooke': 11,
    'Coryell': 12, 
    'Young': 13, 
    'Hood': 14, 
    'Hunt': 15, 
    'Hamilton': 16, 
    'Hill': 17, 
    'Collin': 18, 
    'Palo Pinto': 19, 
    'Grayson': 20, 
    'Erath': 21, 
    'Kaufman': 22,  
    'Ellis': 23,
    'Eastland': 24, 
    'Jack': 25, 
    'Parker': 26, 
    'Rockwall': 27, 
    'Somervell': 28, 
    'Bosque': 29
}


class CountyData():
    def __init__(self, name):
        self.name = name
        self.temp = df.loc[0, name + "_temperature"]
        self.precip = df.loc[0, name + "_precipitation"]
        self.snow = df.loc[0, name + "_snow"]
        self.wind = df.loc[0, name + "_wind_speed"]

class DataPanel(QWidget):
    def __init__(self):
        super(DataPanel, self).__init__()

        # Creates the stacked layout for the county data #
        self.stackedLayout = QStackedLayout()

        # ------------------------------------------------
        # Page 1 creation
        # ------------------------------------------------

        # Create all widgets for page 1
        self.page1 = QWidget()
        page1Layout = QVBoxLayout()
        titleLabel = QLabel('R.F')
        defaultTable = QTableView()
        inputForm = QFormLayout()

        # Title Label Editing
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setMaximumHeight(50)
        titleLabel.setStyleSheet("font-size: 25px; font-weight: bold;")
        page1Layout.addWidget(titleLabel)

        # default Table view setup
        model = QStandardItemModel()

        model.setRowCount(5)        # Date, temp, precip, snow, wind
        model.setColumnCount(2)     # label, value

        for row in range(5):
            for column in range(2):
                item = QStandardItem()    # Load data in here for now
                model.setItem(row, column, item)

        defaultTable.setModel(model)
        page1Layout.addWidget(defaultTable)

        # input Form setup
        formTitle = QLabel('Fill this in to begin forecasting')
        dateLabel = QLabel('Date (Format: 0000-00-00):')             # We need to input check this!!!!!    
        futureDayLabel = QLabel('Days into future:')
        dateInput = QLineEdit()
        futureDayInput = QLineEdit()

        inputForm.addRow(formTitle)
        inputForm.addRow(dateLabel, dateInput)
        inputForm.addRow(futureDayLabel, futureDayInput)
        inputForm.addRow(QPushButton('Generate'))

        page1Layout.addLayout(inputForm)

        # Add page 1 to stacked layout
        self.page1.setLayout(page1Layout)
        self.stackedLayout.addWidget(self.page1)

        # ------------------------------------------------
        # End of Page 1 creation
        # ------------------------------------------------        

        # ------------------------------------------------
        # Page 2 creation (Index 1)
        # ------------------------------------------------

        # Create all widgets for page 2
        self.page2 = QWidget()
        titleLabel2 = QLabel('R.F')
        page2Layout = QVBoxLayout()
        topTab = QHBoxLayout()        # Contains title and back button
        regionalStats = QTableView()

        # Top Tab setup ---------------------------------
        # We create a specific button which goes to page 1 so it can be reused

        titleLabel2.setAlignment(Qt.AlignCenter)
        titleLabel2.setMaximumHeight(50)
        titleLabel2.setStyleSheet("font-size: 25px; font-weight: bold;")
        titleLabel2.setMinimumWidth(600)        # Adjust later

        backButton = QPushButton('Back to Date Select')
        backButton.setMaximumWidth(200)          # Adjust later

        topTab.addWidget(titleLabel2)
        topTab.addWidget(backButton)

        page2Layout.addLayout(topTab)

        # End of Top Tab setup -------------------------

        # Setup regional stats
        model2 = QStandardItemModel()

        model2.setRowCount(5)        # Date, temp, precip, snow, wind
        model2.setColumnCount(2)     # label, value

        for row in range(5):
            for column in range(2):
                item = QStandardItem()    # Load data in here for now
                model2.setItem(row, column, item)

        regionalStats.setModel(model2)        

        page2Layout.addWidget(regionalStats)


        # Add page 2 to stacked layout
        self.page2.setLayout(page2Layout)
        self.stackedLayout.addWidget(self.page2)
        # ------------------------------------------------
        # End of Page 2 creation
        # ------------------------------------------------

        # ------------------------------------------------
        # Page 3 creation
        # ------------------------------------------------

        # Create all widgets for page 3
        self.page3 = QWidget()
        titleLabel3 = QLabel('R.F')
        page3Layout = QVBoxLayout()
        topTab2 = QHBoxLayout()        # Contains title and back button
        countyStats = QTableView()

        # Top Tab setup ---------------------------------
        # We create another specific button which goes to page 2

        titleLabel3.setAlignment(Qt.AlignCenter)
        titleLabel3.setMaximumHeight(50)
        titleLabel3.setStyleSheet("font-size: 25px; font-weight: bold;")
        titleLabel3.setMinimumWidth(600)        # Adjust later

        backButton2 = QPushButton('Back to County Select')
        backButton2.setMaximumWidth(200)          # Adjust later

        backButton3 = QPushButton('Back to Date Select')
        backButton3.setMaximumWidth(200)          # Adjust later

        topTab2.addWidget(titleLabel3)
        topTab2.addWidget(backButton3)
        topTab2.addWidget(backButton2)
        
        page3Layout.addLayout(topTab2)

        # End of Top Tab setup -------------------------

        # Setup regional stats
        model3 = QStandardItemModel()

        # Call a function to get the number of future days so we can add that to the row count
        numFutureDays = 1 #make function ts

        model3.setRowCount(5 + numFutureDays + 1)        # Date, temp, precip, snow, wind
        model3.setColumnCount(2)     # label, value

        for row in range(5):
            for column in range(2):
                item = QStandardItem()    # Load data in here for now
                model3.setItem(row, column, item)

        countyStats.setModel(model3)

        page3Layout.addWidget(countyStats)


        # Add page 3 to stacked layout
        self.page3.setLayout(page3Layout)
        self.stackedLayout.addWidget(self.page3)

        # ------------------------------------------------
        # End of Page 3 creation
        # ------------------------------------------------

        self.stackedLayout.setCurrentIndex(2)
        self.setLayout(self.stackedLayout)

