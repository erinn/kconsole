# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt6.QtCore import Qt, QIODevice, QRunnable, QThreadPool, pyqtSlot
from PyQt6.QtWidgets import (
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
from ksync.ksync import KSync

from PyQt6.QtSerialPort import QSerialPort


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.threadpool = QThreadPool()

        self.setWindowTitle("KConsole")
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
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
        """Open the Broadcast Message dialog."""
        dialog = BroadcastDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            #k.send_text(dialog.message, broadcast=True)
            worker = KSyncWorker(dialog.message, port="tnt0")
            self.threadpool.start(worker)


class KSyncWorker(QRunnable):
    """
    Worker thread for ksync
    """
    def __init__(self, message: str, port: str):
        super().__init__()
        self.port = QSerialPort(port)
        self.port.open(QIODevice.OpenModeFlag.ReadWrite)
        self.k = KSync(self.port)
        self.message = message

    @pyqtSlot()
    def run(self):
        self.k.send_text(self.message, broadcast=True)


class BroadcastDialog(QDialog):
    """Broadcast dialog."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setWindowTitle("Broadcast Message")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None
        """Setup the Broadcast dialog's GUI."""
        # Create line edits for data fields
        self.messageField = QLineEdit()
        self.messageField.setObjectName("Message")
        self.messageField.setPlaceholderText("Message to Broadcast")
        # Lay out the data fields
        layout = QFormLayout()
        layout.addRow("Message:", self.messageField)
        self.layout.addLayout(layout)
        # Add standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the message provided through the dialog."""
        self.message = self.messageField.text()

        if len(self.message) > 4096:
            QMessageBox.critical(
                self,
                "Error!",
                f"Message size must not exceed 4096 characters.",
            )

        if not self.message:
            return

        super().accept()
