import pyqtgraph as pg
import numpy as np
from timeutils import secondsToHHMMSSMMM


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        strings = []
        for v in values:
            vs = v * scale
            vstr = secondsToHHMMSSMMM(vs)
            strings.append(vstr)
        return strings
