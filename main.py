from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
import matplotlib
matplotlib.use('Agg')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap('sens2.PNG')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    from widgets.main_window import MainWindow

    window = MainWindow()
    window.showMaximized()
    splash.finish(window)
    sys.exit(app.exec_())