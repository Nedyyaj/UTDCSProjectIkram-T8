import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QKeySequence, Qt, QPixmap, QPainter, QStandardItemModel, QStandardItem, QPalette, QColor
from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout,
 QGraphicsGridLayout, QGraphicsProxyWidget, QGraphicsScene, QGraphicsWidget, QGraphicsView, QSizePolicy, QLineEdit, QFormLayout, QTableView, QStackedLayout, QTabWidget, 
 QTableWidgetItem, QTableWidget, QComboBox, QCheckBox, QRadioButton, QTextEdit, QScrollArea, QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QStyleOption, 
 QStyle, QTableWidgetItem, QHeaderView, QStyledItemDelegate)
import pandas as pd
import pickle
from forecast import Forecaster

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.temp_ax = fig.add_subplot(221)
        self.prcp_ax = fig.add_subplot(222)
        self.snow_ax = fig.add_subplot(223)
        self.wind_ax = fig.add_subplot(224)
        super().__init__(fig)


def LDEBUG(message):
    print(f"[DEBUG]: {message}")

df = pd.read_csv("../backend/preprocessing/county_variables.csv")
#forecast file
ff = ''

with open('../backend/deep learning/trained_forecaster.pkl', 'rb') as f:
    LDEBUG("pickle dump")
    best_forecaster = pickle.load(f)

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
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(54, 116, 181))  # Background color

        # Creates the stacked layout for the county data #
        delegate = ReadOnlyDelegate(self)
        self.stackedLayout = QStackedLayout()

        # ------------------------------------------------
        # Page 1 creationb (Index 0)
        # ------------------------------------------------

        # Create all widgets for page 1
        self.page1 = QWidget()
        page1Layout = QVBoxLayout()
        titleLabel = QLabel('4CASTX Weather Forecasting')
        defaultTable = QTableView()
        inputForm = QFormLayout()

        # Title Label Editing
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setMaximumHeight(50)
        titleLabel.setStyleSheet("font-size: 25px; font-weight: bold;")
        page1Layout.addWidget(titleLabel)

        # default Table view setup
        #model = QStandardItemModel()

        #model.setRowCount(5)        # Date, temp, precip, snow, wind
        #model.setColumnCount(2)     # label, value

        #for row in range(5):
        #    for column in range(2):
        #        item = QStandardItem()    # Load data in here for now
        #        model.setItem(row, column, item)

        #defaultTable.setItemDelegate(delegate)

        #defaultTable.setModel(model)
        #page1Layout.addWidget(defaultTable)

        # input Form setup
        formTitle = QLabel('Fill this in to begin forecasting')
        dateLabel = QLabel('Starting Date (YYYY-MM-dd, up to 2025-03-01):')             # We need to input check this!!!!!    
        #futureDayLabel = QLabel('Days into future to forecast (< 6):')
        self.dateInput = QLineEdit()
        #self.futureDayInput = QLineEdit()

        inputForm.addRow(formTitle)
        inputForm.addRow(dateLabel, self.dateInput)
        #inputForm.addRow(futureDayLabel, self.futureDayInput)
        generate_button = QPushButton('Generate Forecast')
        generate_button.clicked.connect(lambda x:self.set_panel(2))
        generate_button.clicked.connect(lambda x:self.generate(self.dateInput.text()))
        inputForm.addRow(generate_button)

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
        self.titleLabel2 = QLabel(f"Forecasted Regional Averages")
        page2Layout = QVBoxLayout()
        topTab = QHBoxLayout()        # Contains title and back button
        regionalStats = QTableView()

        # Top Tab setup ---------------------------------
        # We create a specific button which goes to page 1 so it can be reused

        self.titleLabel2.setAlignment(Qt.AlignCenter)
        self.titleLabel2.setMaximumHeight(50)
        self.titleLabel2.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.titleLabel2.setMinimumWidth(500)        # Adjust later

        backButton = QPushButton('Back to Date Select')
        backButton.setMaximumWidth(200)          # Adjust later
        backButton.clicked.connect(lambda x:self.set_panel(1))

        topTab.addWidget(self.titleLabel2)
        topTab.addWidget(backButton)

        page2Layout.addLayout(topTab)

        # End of Top Tab setup -------------------------

        # Setup regional stats
        self.model2 = QStandardItemModel()

        self.model2.setRowCount(5)        # Date, temp, precip, snow, wind
        self.model2.setColumnCount(5)     # label, value

        for row in range(5):
            for column in range(5):
                item = QStandardItem()    # Load data in here for now
                self.model2.setItem(row, column, item)

        regionalStats.setModel(self.model2)        
        regionalStats.verticalHeader().hide()
        regionalStats.horizontalHeader().hide()
        regionalStats.setItemDelegate(delegate)

        page2Layout.addWidget(regionalStats)

        self.regionCanvas = MplCanvas(self, width=5, height=4, dpi=100)
        #self.regionCanvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        page2Layout.addWidget(self.regionCanvas)

        # Add page 2 to stacked layout
        self.page2.setLayout(page2Layout)
        self.stackedLayout.addWidget(self.page2)
        # ------------------------------------------------
        # End of Page 2 creation
        # ------------------------------------------------

        # ------------------------------------------------
        # Page 3 creation (Index 2)
        # ------------------------------------------------

        # Create all widgets for page 3
        self.page3 = QWidget()
        self.titleLabel3 = QLabel('R.F')
        page3Layout = QVBoxLayout()
        topTab2 = QHBoxLayout()        # Contains title and back button
        countyStats = QTableView()
        buttonBox = QVBoxLayout()

        # Top Tab setup ---------------------------------
        # We create another specific button which goes to page 2

        self.titleLabel3.setAlignment(Qt.AlignCenter)
        self.titleLabel3.setMaximumHeight(50)
        self.titleLabel3.setStyleSheet("font-size: 25px; font-weight: bold;")
        self.titleLabel3.setMinimumWidth(500)        # Adjust later

        backButton2 = QPushButton('Back to Regional Data')
        backButton2.setMaximumWidth(200)          # Adjust later
        backButton2.clicked.connect(lambda x:self.set_panel(2))

        backButton3 = QPushButton('Back to Date Select')
        backButton3.setMaximumWidth(200)          # Adjust later
        backButton3.clicked.connect(lambda x:self.set_panel(1))

        topTab2.addWidget(self.titleLabel3)
        buttonBox.addWidget(backButton2)
        buttonBox.addWidget(backButton3)
        topTab2.addLayout(buttonBox)
        
        page3Layout.addLayout(topTab2)

        # End of Top Tab setup -------------------------

        # Setup regional stats
        self.model3 = QStandardItemModel()

        # Call a function to get the number of future days so we can add that to the row count
        numFutureDays = 0 #make function ts

        self.model3.setRowCount(5 + numFutureDays + 1)        # Date, temp, precip, snow, wind
        self.model3.setColumnCount(2)     # label, value

        for row in range(5):
            for column in range(2):
                item = QStandardItem()    # Load data in here for now
                self.model3.setItem(row, column, item)

        countyStats.setModel(self.model3)
        countyStats.verticalHeader().hide()
        countyStats.horizontalHeader().hide()
        countyStats.setItemDelegate(delegate)

        page3Layout.addWidget(countyStats)

        self.countyCanvas = MplCanvas(self, width=5, height=4, dpi=100)
        #self.countyCanvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        page3Layout.addWidget(self.countyCanvas)

        # Add page 3 to stacked layout
        self.page3.setLayout(page3Layout)
        self.stackedLayout.addWidget(self.page3)

        # ------------------------------------------------
        # End of Page 3 creation
        # ------------------------------------------------

        self.stackedLayout.setCurrentIndex(0)
        self.setLayout(self.stackedLayout)

    @Slot()
    def set_panel(self, page):
        self.stackedLayout.setCurrentIndex(page-1)

    @Slot()
    def generate(self, date):
        #TODO: sanitize input <- notify user if not valid
        good = True
        if len(date) != 10:
            good = False
        else:
            # for char in self.futureDayInput.text():
            #     if char not in '0123456789':
            #         good = False
            # if int(self.futureDayInput.text()) < 1 or int(self.futureDayInput.text()) > 5:
            #     good = False

            year =  date[0:4]    #year
            month = date[5:7]    #month
            day =   date[8:10]   #day
            LDEBUG(f"year: {year}, month: {month}, day: {day}")

            for char in year:
                if char not in '0123456789':
                    good = False
            for char in month:
                if char not in '0123456789':
                    good = False
            for char in day:
                if char not in '0123456789':
                    good = False

        if good == False:
            LDEBUG("wrong input")
            self.set_panel(1)
            self.wrong_input_error()
            
        else:
            future_days = 5
            actual_date = f"{year}-{month}-{day}"   
            best_forecaster.generate(date, future_days, obs_path='../backend/preprocessing/county_variables.csv', forecast_path='forecast.csv')
            self.fill_regional_data(future_days)
            self.titleLabel2.setText(f"Forecasted Regional Averages")
            LDEBUG("generated data")


    def fill_regional_data(self, num_days):

        # Reads the forcast file
        ff = pd.read_csv("forecast.csv")

        total_temp = 0
        total_precip = 0
        total_snow = 0
        total_wind = 0

        # Set labels
        self.model2.setItem(0, 1, QStandardItem("Temperature"))
        self.model2.setItem(0, 2, QStandardItem("Precipitation"))
        self.model2.setItem(0, 3, QStandardItem("Snow"))
        self.model2.setItem(0, 4, QStandardItem("Wind Speed"))

        dates = []
        temps = []
        prcps = []
        snows = []
        winds = []

        # Iterates through and adds the totals up before averaging them and plugging them into the table iterating through how many days into future desired
        for i in range(num_days):
            self.model2.setItem(i+1, 0, QStandardItem(f"{ff.loc[4*i, 'Date']}"))

            specific_Date = ff.loc[4*i, "Date"]
            dates.append(specific_Date)

            # Does one row of the table at a time
            for region in county_stations:
                for j in range(4):
                    if ff.loc[(j + 4*i), "Date"] == specific_Date:
                        total_temp    += ff.loc[(j + 4*i), region + "_temperature"]
                        total_precip  += ff.loc[(j + 4*i), region + "_precipitation"]
                        total_snow    += ff.loc[(j + 4*i), region + "_snow"]
                        total_wind    += ff.loc[(j + 4*i), region + "_wind_speed"]
            average_temp   = QStandardItem(f'{(total_temp / (29 * 4)):.2f}') #TODO: 29 hardcoded, fix
            total_precip2 = QStandardItem(f'{(total_precip):.2f}')
            total_snow2   = QStandardItem(f'{(total_snow):.2f}')
            average_wind   = QStandardItem(f'{(total_wind / (29 * 4)):.2f}')

            temps.append((total_temp / (29 * 4)))
            prcps.append(total_precip)
            snows.append(total_snow)
            winds.append((total_wind / (29 * 4)))

            # Resets each day
            total_temp = 0
            total_precip = 0
            total_snow = 0
            total_wind = 0

            # Setting values in that row
            self.model2.setItem(i+1, 1, average_temp)
            self.model2.setItem(i+1, 2, total_precip2)   # use total instead of average because rain is cumulative
            self.model2.setItem(i+1, 3, total_snow2)
            self.model2.setItem(i+1, 4, average_wind)
        
        # clear existing figures
        self.regionCanvas.temp_ax.cla()
        self.regionCanvas.prcp_ax.cla()
        self.regionCanvas.snow_ax.cla()
        self.regionCanvas.wind_ax.cla()

        # set titles
        self.regionCanvas.temp_ax.set_title('Average Temperature')
        self.regionCanvas.prcp_ax.set_title('Total Precipitation')
        self.regionCanvas.snow_ax.set_title('Total Snowfall')
        self.regionCanvas.wind_ax.set_title('Average Wind Speed')

        # plot data
        print(temps)
        self.regionCanvas.temp_ax.plot(range(1, len(temps) + 1), temps)
        print(prcps)
        self.regionCanvas.prcp_ax.plot(range(1, len(prcps) + 1), prcps)
        print(snows)
        self.regionCanvas.snow_ax.plot(range(1, len(snows) + 1), snows)
        print(winds)
        self.regionCanvas.wind_ax.plot(range(1, len(winds) + 1), winds)

        self.regionCanvas.draw()
        #average data
        #fill table

    def wrong_input_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Invalid Input")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def fill_county_data(self, county):

        self.titleLabel3.setText(f"Forecast for {county} County")
        # Reads the forcast file
        ff = pd.read_csv("forecast.csv")

        county_total_temp = 0
        county_total_precip = 0
        county_total_snow = 0
        county_total_wind = 0

        # Set labels
        self.model3.setItem(0, 1, QStandardItem("Temperature"))
        self.model3.setItem(0, 2, QStandardItem("Precipitation"))
        self.model3.setItem(0, 3, QStandardItem("Snow"))
        self.model3.setItem(0, 4, QStandardItem("Wind Speed"))

        temps = []
        prcps = []
        snows = []
        winds = []

        # Iterates through and adds the totals up before averaging them and plugging them into the table iterating through how many days into future desired
        for i in range(5):
            self.model3.setItem(i+1, 0, QStandardItem(f"{ff.loc[4*i, 'Date']}"))

            specific_Date = ff.loc[4*i, "Date"]
            for j in range(4):

                if ff.loc[(j + 4*i), "Date"] == specific_Date:
                    county_total_temp    += ff.loc[(j + 4*i), county + "_temperature"]
                    county_total_precip  += ff.loc[(j + 4*i), county + "_precipitation"]
                    county_total_snow    += ff.loc[(j + 4*i), county + "_snow"]
                    county_total_wind    += ff.loc[(j + 4*i), county + "_wind_speed"]
            
            county_average_temp   = QStandardItem(f'{(county_total_temp / 4):.2f}') #TODO: 4 hardcoded, fix
            county_total_precip2 = QStandardItem(f'{(county_total_precip):.2f}')
            county_total_snow2   = QStandardItem(f'{(county_total_snow):.2f}')
            county_average_wind   = QStandardItem(f'{(county_total_wind / 4):.2f}')

            temps.append((county_total_temp / 4))
            prcps.append(county_total_precip)
            snows.append(county_total_snow)
            winds.append((county_total_wind / 4))

            # Resets each day
            county_total_temp = 0
            county_total_precip = 0
            county_total_snow = 0
            county_total_wind = 0

            # Setting values in that row
            self.model3.setItem(i+1, 1, county_average_temp)
            self.model3.setItem(i+1, 2, county_total_precip2)
            self.model3.setItem(i+1, 3, county_total_snow2)
            self.model3.setItem(i+1, 4, county_average_wind)

        # clear existing figures
        self.countyCanvas.temp_ax.cla()
        self.countyCanvas.prcp_ax.cla()
        self.countyCanvas.snow_ax.cla()
        self.countyCanvas.wind_ax.cla()

        # set titles
        self.countyCanvas.temp_ax.set_title('Average Daily Temperature')
        self.countyCanvas.prcp_ax.set_title('Total Daily Precipitation')
        self.countyCanvas.snow_ax.set_title('Total Daily Snowfall')
        self.countyCanvas.wind_ax.set_title('Average Daily Wind Speed')

        # plot data
        print(temps)
        self.countyCanvas.temp_ax.plot(range(1, len(temps) + 1), temps)
        print(prcps)
        self.countyCanvas.prcp_ax.plot(range(1, len(prcps) + 1), prcps)
        print(snows)
        self.countyCanvas.snow_ax.plot(range(1, len(snows) + 1), snows)
        print(winds)
        self.countyCanvas.wind_ax.plot(range(1, len(winds) + 1), winds)

        self.countyCanvas.draw()

    
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return None

    def setEditorData(self, editor, index):
        pass

    def setModelData(self, editor, model, index):
        pass

