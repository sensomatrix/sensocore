from widgets.Plotter import Plotter

class CrossCorrelation(Plotter):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.p = self.graphLayout.addPlot()
        self.p.setLabel('bottom', text="Time", units="sec")
        self.p.setLabel('left', text="Magnitude", units="")
        self.plotslist = []
        self.p.showGrid(x=True,y=True)

    def plot_data(self, data):
            self.plotslist.clear()
            self.plotslist.append(self.p.plot(data, clear=True, pen='r'))
