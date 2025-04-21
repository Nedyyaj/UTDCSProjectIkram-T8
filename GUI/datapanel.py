import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)
import pandas as pd

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
        self.avg_temp = df.loc[0, name + "_avg_temp"]
        self.min_temp = df.loc[0, name + "_min_temp"]
        self.max_temp = df.loc[0, name + "_max_temp"]
        self.precip = df.loc[0, name + "_precip"]
        self.snow = df.loc[0, name + "_snow"]
        self.avg_wind = df.loc[0, name + "_avg_wind"]
        self.max_wind = df.loc[0, name + "_max_wind"]

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
        self.avg_temp = 0.0
        self.min_temp = 0.0
        self.max_temp = 0.0
        self.precip = 0.0
        self.snow = 0.0
        self.avg_wind= 0.0
        self.max_wind = 0.0

        grid = QGridLayout(self)
        self.county_value   = QLabel(str(self.county))
        self.avg_temp_value = QLabel(str(self.avg_temp))
        self.min_temp_value = QLabel(str(self.min_temp))
        self.max_temp_value = QLabel(str(self.max_temp))
        self.precip_value   = QLabel(str(self.precip))
        self.snow_value     = QLabel(str(self.snow))
        self.avg_wind_value = QLabel(str(self.avg_wind))
        self.max_wind_value = QLabel(str(self.max_wind))

        self.county_label   = QLabel('County:')
        self.avg_temp_label = QLabel('Average Temperature:')
        self.min_temp_label = QLabel('Minimum Temperature:')
        self.max_temp_label = QLabel('Maximum Temperature:')
        self.precip_label   = QLabel('Precipitation:')
        self.snow_label     = QLabel('Snow:')
        self.avg_wind_label = QLabel('Average Wind:')
        self.max_wind_label = QLabel('Maximum Wind:')

        grid.addWidget(self.county_value,   0, 1)
        grid.addWidget(self.avg_temp_value, 1, 1)
        grid.addWidget(self.min_temp_value, 2, 1)
        grid.addWidget(self.max_temp_value, 3, 1)
        grid.addWidget(self.precip_value,   4, 1)
        grid.addWidget(self.snow_value,     5, 1)
        grid.addWidget(self.avg_wind_value, 6, 1)
        grid.addWidget(self.max_wind_value, 7, 1)

        grid.addWidget(self.county_label,   0, 0)
        grid.addWidget(self.avg_temp_label, 1, 0)
        grid.addWidget(self.min_temp_label, 2, 0)
        grid.addWidget(self.max_temp_label, 3, 0)
        grid.addWidget(self.precip_label,   4, 0)
        grid.addWidget(self.snow_label,     5, 0)
        grid.addWidget(self.avg_wind_label, 6, 0)
        grid.addWidget(self.max_wind_label, 7, 0)
        self.setLayout(grid)

    def on_county_selected(self, county):
        self.county_value.setText   (str(self.data[county_dict[county]].name))
        self.avg_temp_value.setText (str(self.data[county_dict[county]].avg_temp))
        self.min_temp_value.setText (str(self.data[county_dict[county]].min_temp))
        self.max_temp_value.setText (str(self.data[county_dict[county]].max_temp))
        self.precip_value.setText   (str(self.data[county_dict[county]].precip))
        self.snow_value.setText     (str(self.data[county_dict[county]].snow))
        self.avg_wind_value.setText (str(self.data[county_dict[county]].avg_wind))
        self.max_wind_value.setText (str(self.data[county_dict[county]].max_wind))
