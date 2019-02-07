from widgets.Plotter import Plotter

class CrossCorrelation(Plotter):
    def __init__(self):
        super().__init__()
        self.p = self.graphLayout.addPlot()
        self.p.setLabel('bottom', text="Time", units="sec")
        self.p.setLabel('left', text="Magnitude", units="")
        self.p.showGrid(x=True,y=True)

    def plot_data(self, time, samples, **kwargs):
            self.p.plot(time, samples, clear=True, pen='r')
            if 'title' in kwargs:
                self.p.setTitle(kwargs.get('title'))
