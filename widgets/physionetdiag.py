from PyQt5.QtWidgets import QPushButton, QDialog, QDialogButtonBox, QGroupBox, QLabel, QLineEdit, QFormLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from .errormessages import ErrorMessage
from physionet import import_from_physio

class PhysionetDiag(QDialog):
    def __init__(self, parent):
        super(PhysionetDiag, self).__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.create()

    def create(self):
        self.database_label = QLabel("PhysioBank <a href=\"https://physionet.org/physiobank/database/\">DB URL</a>:")
        self.database_label.setTextFormat(Qt.RichText)
        self.database_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.database_label.setOpenExternalLinks(True);
        self.database_lineedit = QLineEdit()
        self.database_lineedit.setToolTip("URL to PhysioBank database: https://physionet.org/physiobank/database/xxxxx")
        self.databaseexample_label = QLabel("e.g.: https://physionet.org/physiobank/database/eegmat/")


        self.recordname_label = QLabel("Record name:")
        self.recordname_lineedit = QLineEdit()
        self.recordname_lineedit.setToolTip("Name of the record without the extension")
        self.recordnameexample_label = QLabel("gay")

        formlayout = QFormLayout()
        formlayout.addRow(self.database_label, self.database_lineedit)
        formlayout.addRow(self.databaseexample_label)
        formlayout.addRow(self.recordname_label, self.recordname_lineedit)
        formlayout.addRow(self.recordnameexample_label)

        gb = QGroupBox()
        gb.setLayout(formlayout)

        # button box
        self.buttonbox = QDialogButtonBox()
        self.downloaddata_button = QPushButton("Import dataset")
        self.buttonbox.addButton(self.downloaddata_button, QDialogButtonBox.ActionRole)
        self.downloaddata_button.clicked.connect(self.download_dataset)

        vlayout = QVBoxLayout()
        vlayout.addWidget(gb)
        vlayout.addWidget(self.buttonbox)
        self.setLayout(vlayout)
        self.setWindowTitle("Import Physionet dataset")
        self.show()

    def download_dataset(self):
        db = self.database_lineedit.text()
        if db:
            if db[-1] == "/":
                db = db[:-1]
            db = db.rsplit('/', 1)[-1]
        else:
            error = ErrorMessage("Enter the database URL")
            return
        record = self.recordname_lineedit.text()
        if record:
            record = record.split(".")[0]
        else:
            error = ErrorMessage("Enter a record name")
            return
        try:
            siglist, comments = import_from_physio(record, db)
        except:
            error = ErrorMessage("Could not import the data.")
            return
        for sig in siglist:
            self.parent.datasets.addSignaltoDataset(sig)
        self.parent.console.write("Loaded " + record + " from " + db)
        for comment in comments:
            self.parent.console.write(comment)
        self.close()





