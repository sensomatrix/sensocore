import pyqtgraph as pg
import numpy as np
from timeutils import secondsToHHMMSSMMM


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        places = max(0, np.ceil(-np.log10(spacing * scale)))
        strings = []
        for v in values:
            vs = v * scale
            if abs(vs) < .001 or abs(vs) >= 10000:
                vstr = secondsToHHMMSSMMM(vs)
            else:
                vstr = secondsToHHMMSSMMM(vs)
            strings.append(vstr)
        return strings
