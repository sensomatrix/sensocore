from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QLabel, QWidget, QFormLayout, QVBoxLayout, QGroupBox

class Info(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.create()

    def create(self):
        dataset_info_group = QGroupBox('Dataset')
        form = QFormLayout()
        dataset_info_group.setLayout(form)

        self.idx_s_freq = QLabel('')
        self.opened_filename_label = QLabel('')
        form.addRow('Filename:', self.opened_filename_label)
        #nothing here for now:
        form.addRow('Subject ID: ', QLabel(''))
        form.addRow('Experiment:', QLabel(''))

        layout = QVBoxLayout()
        layout.addWidget(dataset_info_group)
        self.setLayout(layout)
        
    def set_opened_filename(self, filename):
        self.opened_filename_label.setText(filename)