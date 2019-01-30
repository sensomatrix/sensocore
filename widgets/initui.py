from .channels import Channels
from .info import Info
from .center import Center
from .console import Console
from .psddock import PSDDock
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget


# connect pyqt signals to pyqt slots here
def init_connect_slots(MAIN):
        MAIN.datasets.signal_loaded_signal.connect(MAIN.center.scope.on_signal_loaded)
        MAIN.center.scope.cursor_moved_signal.connect(MAIN.center.chrono.on_cursor_moved)
        MAIN.datasets.signal_loaded_signal.connect(MAIN.channels.on_signal_loaded)
        MAIN.channels.channel_selected_signal.connect(MAIN.psd.on_channel_selection_change)

def init_ui_widgets(MAIN):
    
    MAIN.console = Console(MAIN)
    MAIN.channels = Channels(MAIN)
    MAIN.center = Center(MAIN)
    MAIN.info = Info(MAIN)
    MAIN.psd = PSDDock(MAIN)
    MAIN.setCentralWidget(MAIN.center)

    #list of dock widgets
    docks = [{'name': 'Information',
              'widget': MAIN.info,
              'main_area': Qt.LeftDockWidgetArea,
              },
             {'name': 'Channels',
              'widget': MAIN.channels,
              'main_area': Qt.RightDockWidgetArea,
              },
             {'name': 'Power Spectral Density',
              'widget': MAIN.psd,
              'main_area': Qt.RightDockWidgetArea,
              'min_height': 100,
              'max_height': 300,
              'max_width': 250
              },
             {'name': 'Console',
              'widget': MAIN.console,
              'main_area': Qt.BottomDockWidgetArea,
              'max_height': 100,
              },
             ]
    #dock widgets
    for dock in docks:
        dockwidget = QDockWidget(dock['name'], MAIN)
        dockwidget.setWidget(dock['widget'])
        dockwidget.setAllowedAreas(dock['main_area'])
        dockwidget.setObjectName(dock['name'])
        if 'max_height' in dock:
            dockwidget.setMaximumHeight(dock['max_height'])
        MAIN.addDockWidget(dock['main_area'], dockwidget)
        if 'min_height' in dock:
            dockwidget.setMinimumHeight(dock['min_height'])
        MAIN.addDockWidget(dock['main_area'], dockwidget)
        if 'max_width' in dock:
            dockwidget.setMaximumWidth(dock['max_width'])
        MAIN.addDockWidget(dock['main_area'], dockwidget)

def init_ui_toolbar(MAIN):
    # create the toolbar
    actions = MAIN.datasets.actions
    toolbar = MAIN.addToolBar("file")
    toolbar.addAction(MAIN.datasets.actions['open_dataset'])

