import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap, QPainter
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout, QGraphicsGridLayout, QGraphicsProxyWidget, QGraphicsScene, QGraphicsWidget, QGraphicsView, QSizePolicy)
import pandas as pd
import pickle as pkl


def LDEBUG(message):
    print(f"[DEBUG]: {message}")


df = pd.read_csv("../backend/preprocessing/county_variables.csv")

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

        self.data = [None] * 30
        self.data[1]  = CountyData('Tarrant')
        self.data[2]  = CountyData('McLennan')
        self.data[3]  = CountyData('Montague')
        self.data[4]  = CountyData('Stephens')
        self.data[5]  = CountyData('Wise')
        self.data[6]  = CountyData('Johnson')
        self.data[7]  = CountyData('Comanche')
        self.data[8]  = CountyData('Navarro')
        self.data[9]  = CountyData('Dallas')
        self.data[10]  = CountyData('Denton')
        self.data[11] = CountyData('Cooke')
        self.data[12] = CountyData('Coryell')
        self.data[13] = CountyData('Young')
        self.data[14] = CountyData('Hood')
        self.data[15] = CountyData('Hunt')
        self.data[16] = CountyData('Hamilton')
        self.data[17] = CountyData('Hill')
        self.data[18] = CountyData('Collin')
        self.data[19] = CountyData('Palo Pinto')
        self.data[20] = CountyData('Grayson')
        self.data[21] = CountyData('Erath')
        self.data[22] = CountyData('Kaufman')
        self.data[23] = CountyData('Ellis')
        self.data[24] = CountyData('Eastland')
        self.data[25] = CountyData('Jack')
        self.data[26] = CountyData('Parker')
        self.data[27] = CountyData('Rockwall')
        self.data[28] = CountyData('Somervell')
        self.data[29] = CountyData('Bosque')

        self.county = 'None'
        self.temp = 0.0
        self.precip = 0.0
        self.snow = 0.0
        self.wind= 0.0

       # Initialize the windows required for the GUI
        self.main_Window = QWidget(self)
        main_Window_Grid = QGridLayout()
        county_Window = QWidget()
        self.grid = QGridLayout()
        
        #--------------------------------------------------
        # Prep the VBOX and Grid Layout for the main window view
        #--------------------------------------------------

        # Edit Label
        label = QLabel("Select a County")
        label.setAlignment(Qt.AlignCenter)
        label.setMaximumHeight(30)
        label.setStyleSheet("font-size: 25px; font-weight: bold;")
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Combining everything into vBox layout so it is stacked vertically
        main_Window_Grid.addWidget(label)

        self.mainWindow_vBox = QVBoxLayout()
        self.mainWindow_vBox.addWidget(label)
        self.mainWindow_vBox.setSpacing(0)

        
        # Create the grid layout for the county buttons under main_Window_Grid to add to the vbox layout
        counter = 0
        column = 0
        row = 2
        for county in county_stations:
            button = QPushButton(county)
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            button.sizeIncrement()
            main_Window_Grid.addWidget(button, row, column)
            row += 1
            counter += 1
            if counter == 15:
                row = 2
                column += 1

        # Add grid to the vbox layout
        self.mainWindow_vBox.addLayout(main_Window_Grid)

        # Creates the grid layout for the county data #
        #--------------------------------------------------
        #         Place Holder for real data view
        #--------------------------------------------------
        self.county_value   = QLabel(str(self.county), margin=5)
        self.temp_value     = QLabel(str(self.temp))
        self.precip_value   = QLabel(str(self.precip))
        self.snow_value     = QLabel(str(self.snow))
        self.wind_value     = QLabel(str(self.wind))

        self.county_label   = QLabel('County:')
        self.temp_label     = QLabel('Temperature:')
        self.precip_label   = QLabel('Precipitation:')
        self.snow_label     = QLabel('Snow:')
        self.wind_label     = QLabel('Wind:')

        self.grid.addWidget(self.county_value,   0, 1, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.temp_value,     1, 1, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.precip_value,   2, 1, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.snow_value,     3, 1, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.wind_value,     4, 1, alignment=Qt.AlignCenter)

        self.grid.addWidget(self.county_label,   0, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.temp_label,     1, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.precip_label,   2, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.snow_label,     3, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.wind_label,     4, 0, alignment=Qt.AlignCenter)
        
        #--------------------------------------------------
        #      End of Place Holder for real data view
        #--------------------------------------------------

        #Adds the grid layout to the vbox layout
        self.main_Window = self.mainWindow_vBox
        self.hide_data()
        self.setLayout(self.main_Window)
        #self.setLayout(county_Window)  
        

        #when the button is clicked, call the on_click method
        for i in range(1, 30):
            button = main_Window_Grid.itemAt(i).widget()
            name = button.clicked.connect(lambda _, b = button: self.on_click(b))
            


    def on_county_selected(self, county):
        self.county_value.setText   (str(self.data[county_dict[county]].name))
        self.temp_value.setText     (str(self.data[county_dict[county]].temp))
        self.precip_value.setText   (str(self.data[county_dict[county]].precip))
        self.snow_value.setText     (str(self.data[county_dict[county]].snow))
        self.wind_value.setText     (str(self.data[county_dict[county]].wind))


        #self.main_Window.addLayout(self.grid)

    #--------------------------------#
    # DEFINES THE USE OF THE BUTTONS
    #--------------------------------#
    def on_click(self, button):

        # Get the name of the button that was clicked
        name = button.text()
        LDEBUG(f"Button clicked: {name}")

        self.county_value.setText   (str(self.data[county_dict[name]].name))
        self.temp_value.setText     (str(self.data[county_dict[name]].temp))
        self.precip_value.setText   (str(self.data[county_dict[name]].precip))
        self.snow_value.setText     (str(self.data[county_dict[name]].snow))
        self.wind_value.setText     (str(self.data[county_dict[name]].wind))

        
        LDEBUG(f"County is: {self.county_value.text()}")
        LDEBUG(f"Temperature is: {self.temp_value.text()}")
        LDEBUG(f"Precipitation is: {self.precip_value.text()}")
        LDEBUG(f"Snow is: {self.snow_value.text()}")
        LDEBUG(f"Wind is: {self.wind_value.text()}")

        self.show_data()
        self.hide_buttons()

    #--------------------------------#
    # Defines the viewing and hiding of the data grid
    #--------------------------------#
    def show_data(self):
        self.main_Window.addLayout(self.grid)
        LDEBUG("Data grid shown")

    def hide_data(self):
        self.main_Window.removeItem(self.grid)
        LDEBUG("Data grid hidden")
    #--------------------------------#
    # End of the button click method
    #--------------------------------#

    #--------------------------------#
    # Defines the viewing and hiding of the vBoxButton grid
    #--------------------------------#
    def show_buttons(self):
        self.main_Window.addLayout(self.mainWindow_vBox)
        LDEBUG("Button grid shown")

    def hide_buttons(self):
        self.main_Window.removeItem(self.main_Window)
        LDEBUG("Button grid hidden")
    #--------------------------------#
    # End of the button click method
    #--------------------------------#