# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""
import os

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

from kconsole.main_window_ui import Ui_MainWindow
from kconsole.settings_dialog import Ui_SettingsDialog

from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo

basedir = os.path.dirname(__file__)


class Window(QMainWindow, Ui_MainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.threadpool = QThreadPool()
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.broadcastButton.clicked.connect(self.openBroadcastMessageDialog)
        self.settingsButton.clicked.connect(self.openSettingsDialog)

    def openBroadcastMessageDialog(self):
        """Open the Broadcast Message dialog."""
        dialog = BroadcastDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            #k.send_text(dialog.message, broadcast=True)
            worker = KSyncWorker(dialog.message, port="tnt0")
            self.threadpool.start(worker)

    def openSettingsDialog(self):
        dialog = SettingsDialog(self)
        dialog.exec()


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


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setupUi(self)
        self.fillPortsInfo()
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.serialPortInfoListBox.currentIndexChanged.connect(self.showPortInfo)

    def fillPortsInfo(self):
        for port in QSerialPortInfo.availablePorts():
            port_info = {'portName': port.portName(),
                         'description': port.description(),
                         'manufacturer': port.manufacturer(),
                         'serialNumber': port.serialNumber(),
                         'systemLocation': port.systemLocation(),
                         'vendorIdentifier': port.vendorIdentifier(),
                         'productIdentifier': port.productIdentifier()}

            self.serialPortInfoListBox.addItem(port_info['portName'], port_info)

    def showPortInfo(self, index: int):
        port_info = self.serialPortInfoListBox.itemData(index)
        self.locationLabel.setText(port_info['systemLocation'])


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
