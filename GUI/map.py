from PySide6.QtWidgets import (QWidget, QPushButton, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QStyleFactory, QSplitter, QGridLayout)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import geopandas
import fiona
import shapefile
from shapely.geometry import (Point, shape)
from datapanel import DataPanel
import time

start_time = ''
end_time = ''
shp = fiona.open(r"map\Select Counties\selected.shp")

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

        self.figure = Figure()
        self.axes=self.figure.add_subplot()
        self.axes.set_axis_off()
        self.counties = geopandas.read_file(r"map\Select Counties\selected.shp")
        self.counties['coords'] = self.counties['geometry'].apply(lambda x: x.representative_point().coords[:])
        self.counties['coords'] = [coords[0] for coords in self.counties['coords']]
        self.last_patch = ''
        self.selected_patch = ''

        cmap = plt.cm.Pastel1
        plot = self.counties.plot(ax=self.axes, cmap=cmap)
        self.counties.apply(lambda x: plot.annotate(text=x['CNTY_NM'], xy=x.geometry.centroid.coords[0], ha='center'), axis=1)

        self.mpl_connect("button_press_event", self.on_click)
        self.mpl_connect("motion_notify_event", self.on_hover)
        self.draw()

    def on_click(self, event):
        if self.datapanel.stackedLayout.currentIndex() == 0:
            return

        min_distance = 3
        if event.xdata != None: 
            if event.ydata != None:
                mouse_pos = Point(event.xdata, event.ydata)
            else:
                return
        else:
            return

        for rec in shp:
            boundary = shape(rec['geometry'])
            if boundary.distance(mouse_pos) < min_distance:
                name = rec['properties']['CNTY_NM']
                patch = plt.Polygon(list(boundary.exterior.coords), closed=True, facecolor='green')
                if self.selected_patch != '':
                    self.selected_patch.remove()
                self.axes.add_patch(patch)
                self.selected_patch = patch
                self.draw()
                self.datapanel.set_panel(3)
                self.datapanel.fill_county_data(name)
                #TODO: call datapanel.set_county or smn

    def on_hover(self, event):
        if self.datapanel.stackedLayout.currentIndex() == 0:
            return

        start_time = time.process_time()

        min_distance = 3 
        if event.xdata != None: 
            if event.ydata != None:
                mouse_pos = Point(event.xdata, event.ydata)
            else:
                return
        else:
            return

        for rec in shp:
            boundary = shape(rec['geometry'])
            if boundary.distance(mouse_pos) < min_distance:
                name = rec['properties']['CNTY_NM']
                patch = plt.Polygon(list(boundary.exterior.coords), closed=True, facecolor='gray')
                if self.last_patch != '':
                    self.last_patch.remove()
                self.axes.add_patch(patch)
                self.last_patch = patch
                self.draw()
