# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ../ksync import KSync

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("KCsonole")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.setupUI()

    def setupUI(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        # Create buttons
        self.broadcastMessageButton = QPushButton("Broadcast Message")
        self.broadcastMessageButton.clicked.connect(self.openBroadcastMessageDialog)
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.broadcastMessageButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

        def openBroadcastMessageDialog(self):
            """Open the Add Contact dialog."""
            dialog = BroadcastDialog(self)
            if dialog.exec() == QDialog.Accepted:
                self.contactsModel.addContact(dialog.data)
                self.table.resizeColumnsToContents()


class BroadcastDialog(QDialog):
    """Broadcast dialog."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Broadcast Message")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()

    def setupUI(self):
        """Setup the Add Contact dialog's GUI."""
        # Create line edits for data fields
        self.messageField = QLineEdit()
        self.messageField.setObjectName("Message")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Message:", self.messageField)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the message provided through the dialog."""
        self.message = self.messageField

        if len(self.message) > 4096:
            QMessageBox.critical(
                self,
                "Error!",
                f"Message size must not exceed 4096 characters.",
            )
        if not self.message:
            return

        super().accept()
