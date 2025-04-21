from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import geopandas
import fiona
import shapefile
from shapely.geometry import (Point, shape)
from datapanel import DataPanel

def LDEBUG(message):
    print(f"[DEBUG]: {message}")

class Map(QWidget):
    def __init__(self, canvas):
        super(Map, self).__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(canvas)

class MapCanvas(FigureCanvas):
    def __init__(self, datapanel):
        super(MapCanvas, self).__init__()

        self.datapanel = datapanel

        fig = Figure(dpi=100)
        self.figure = fig
        self.canvas = FigureCanvas(self.figure)
        self.axes=fig.add_subplot()
        self.axes.set_axis_off()
        self.counties = geopandas.read_file(r"map\Select Counties\selected.shp")
        self.counties['coords'] = self.counties['geometry'].apply(lambda x: x.representative_point().coords[:])
        self.counties['coords'] = [coords[0] for coords in self.counties['coords']]

        cmap = plt.cm.Pastel1
        plot = self.counties.plot(ax=self.axes, cmap=cmap)
        self.counties.apply(lambda x: plot.annotate(text=x['CNTY_NM'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)

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
                    print(name)
                    self.datapanel.on_county_selected(name)
