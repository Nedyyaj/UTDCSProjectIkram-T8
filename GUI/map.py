from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
import geopandas

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
