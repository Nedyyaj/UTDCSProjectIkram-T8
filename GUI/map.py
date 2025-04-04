from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import geopandas
import fiona
import shapefile
from shapely.geometry import (Point, shape)

def LDEBUG(message):
    print(f"[DEBUG]: {message}")

class Map(QWidget):
    def __init__(self, canvas):
        super(Map, self).__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(canvas)

class MapCanvas(FigureCanvas):
    def __init__(self):
        super(MapCanvas, self).__init__()

        fig = Figure(dpi=100)
        self.figure = fig
        self.canvas = FigureCanvas(self.figure)
        self.axes=fig.add_subplot()
        #self.axes.set_axis_off()
        self.counties = geopandas.read_file(r"map\Select Counties\selected.shp")
        self.counties = self.counties.to_crs("EPSG:3395")
        self.counties.boundary.plot(ax=self.axes)
        #self.axes.plot(counties)
        self.mpl_connect("button_press_event", self.on_click)
        self.draw()

    def on_click(self, event):

        min_distance = 3
        mouse_pos = Point(event.xdata, event.ydata)

        shp = shapefile.Reader(r"map\Select Counties\selected.shp")
        fields = shp.fields[1:]
        field_names = [field[0] for field in fields]

        with fiona.open(r"map\Select Counties\selected.shp") as shp:
            for rec in shp:
                boundary = shape(rec['geometry'])
                if boundary.distance(mouse_pos) < min_distance:
                    name = rec['properties']['CNTY_NM']
                    LDEBUG(f"selected region: {name}")



        
'''
        pixmap = QPixmap("images/map.png") 
        pixmap = pixmap.scaled(1000, 1000, Qt.KeepAspectRatio)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        lbl.setMinimumSize(10, 10)
        
        vbox.addWidget(lbl)
'''

    
