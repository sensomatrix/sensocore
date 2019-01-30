from .channels import Channels
from .info import Info
from .center import Center
from .console import Console
from .secondaryarea import SecondaryArea
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QSizePolicy


# connect pyqt signals to pyqt slots here
def init_connect_slots(MAIN):
        MAIN.datasets.signal_loaded_signal.connect(MAIN.center.scope.on_signal_loaded)
        MAIN.center.scope.cursor_moved_signal.connect(MAIN.center.chrono.on_cursor_moved)
        MAIN.datasets.signal_loaded_signal.connect(MAIN.channels.on_signal_loaded)
        MAIN.channels.channel_selected_signal.connect(MAIN.secondary_area.on_channel_selection_change)

def init_ui_widgets(MAIN):
    
    MAIN.console = Console(MAIN)
    MAIN.channels = Channels(MAIN)
    MAIN.center = Center(MAIN)
    MAIN.info = Info(MAIN)
    MAIN.secondary_area = SecondaryArea(MAIN)
    MAIN.setCentralWidget(MAIN.center)

    #list of dock widgets
    docks = [{'name': 'Information',
              'widget': MAIN.info,
              'main_area': Qt.LeftDockWidgetArea,
              },
             {'name': 'Channels',
              'widget': MAIN.channels,
              'main_area': Qt.LeftDockWidgetArea,
              },
             {'name': 'Secondary plotting',
              'widget': MAIN.secondary_area,
              'main_area': Qt.RightDockWidgetArea,
              'min_width': 250,
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
        if 'min_height' in dock:
            dockwidget.setMinimumHeight(dock['min_height'])
        if 'min_width' in dock:
            dockwidget.setMinimumWidth(dock['min_width'])

        MAIN.addDockWidget(dock['main_area'], dockwidget)

def init_ui_toolbar(MAIN):
    # create the toolbar
    actions = MAIN.datasets.actions
    toolbar = MAIN.addToolBar("file")
    toolbar.addAction(MAIN.datasets.actions['open_dataset'])

