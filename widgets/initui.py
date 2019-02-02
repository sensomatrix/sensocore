from .channels import Channels
from .info import Info
from .center import Center
from .console import Console
from .secondaryarea import SecondaryArea
from .simulation_button import SimulateButton
from .spectrumview import SpectrumView
from .firdesignerdiag import FIRDesignerDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDockWidget, QAction


# connect pyqt signals to pyqt slots here
def init_connect_slots(MAIN):
        MAIN.datasets.signal_loaded_signal.connect(MAIN.center.scope.on_signal_loaded)
        MAIN.center.scope.cursor_moved_signal.connect(MAIN.center.chrono.on_cursor_moved)
        MAIN.datasets.signal_loaded_signal.connect(MAIN.channels.on_signal_loaded)
        MAIN.center.scope.plot_specview.connect(MAIN.specview.plot_selection)

def init_ui_widgets(MAIN):
    
    MAIN.console = Console(MAIN)
    MAIN.channels = Channels(MAIN)
    MAIN.center = Center(MAIN)
    MAIN.info = Info(MAIN)
    MAIN.secondary_area = SecondaryArea(MAIN)
    MAIN.specview = SpectrumView(MAIN)
    MAIN.setCentralWidget(MAIN.center)

    #list of dock widgets
    docks = [{'name': 'Information',
              'widget': MAIN.info,
              'main_area': Qt.LeftDockWidgetArea,
              },
             {'name': 'Channels',
              'widget': MAIN.channels,
              'main_area': Qt.LeftDockWidgetArea,
              'max_width': 200,
              },
             {'name': 'Secondary plotting',
              'widget': MAIN.secondary_area,
              'main_area': Qt.RightDockWidgetArea,
              'min_width': 250,
              },
             {'name': 'Spectrum View',
              'widget': MAIN.specview,
              'main_area': Qt.BottomDockWidgetArea,
              'max_height': 200,
              'min_width' : 500,
              },
             {'name': 'Output',
              'widget': MAIN.console,
              'main_area': Qt.BottomDockWidgetArea,
              'max_height': 150,
              },
             ]
    #dock widgets
    MAIN.dock_names = {}
    for dock in docks:
        dockwidget = QDockWidget(dock['name'], MAIN)
        dockwidget.setWidget(dock['widget'])
        dockwidget.setAllowedAreas(dock['main_area'])
        dockwidget.setObjectName(dock['name'])
        MAIN.dock_names[dock['name']] = dockwidget
        if 'max_height' in dock:
            dockwidget.setMaximumHeight(dock['max_height'])
        if 'min_height' in dock:
            dockwidget.setMinimumHeight(dock['min_height'])
        if 'min_width' in dock:
            dockwidget.setMinimumWidth(dock['min_width'])
        if 'max_width' in dock:
            dockwidget.setMaximumWidth(dock['max_width'])

        MAIN.addDockWidget(dock['main_area'], dockwidget)

    MAIN.tabifyDockWidget(MAIN.dock_names['Output'], MAIN.dock_names['Spectrum View'])
    MAIN.dock_names['Output'].raise_()

def init_ui_toolbar(MAIN):
    # create the toolbar
    toolbar = MAIN.addToolBar("file")
    toolbar.addAction(MAIN.datasets.actions['open_dataset'])
    simulate_button = SimulateButton(MAIN)
    toolbar.addWidget(simulate_button)

def init_ui_menubar(MAIN):
    menuBar = MAIN.menuBar()

    file_menu = menuBar.addMenu('File')

    # filtering submenu
    filtering_menu = menuBar.addMenu('Filtering')

    firfilterdesign_action = QAction("FIR Filter Design", MAIN)
    firfilterdesign_action.triggered.connect(lambda: fir_filter_design_open(MAIN))
    filtering_menu.addAction(firfilterdesign_action)


def fir_filter_design_open(parent):
    fir_designer_diag = FIRDesignerDialog(parent)
    fir_designer_diag.exec_()