# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""
import os

from PyQt6.QtCore import Qt, QIODevice, QRunnable, QThreadPool, pyqtSlot, QSettings
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

        self.settings = QSettings()
        self.threadpool = QThreadPool()
        self.setupUi(self)
        self.connectSignalsSlots()
        self.settings = QSettings()

        if not self.settings.contains('default_port'):
            self.openSettingsDialog()

        self.serial_port = None
        self.open_serial_port()
        self.ksync = KSync(self.serial_port)

    def connectSignalsSlots(self):
        self.actionExit.triggered.connect(self.close)
        self.broadcastButton.clicked.connect(self.openBroadcastMessageDialog)
        self.settingsButton.clicked.connect(self.openSettingsDialog)

    def openBroadcastMessageDialog(self):
        """Open the Broadcast Message dialog."""
        dialog = BroadcastDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.send_text(dialog.message, broadcast=True)

    def openSettingsDialog(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def open_serial_port(self) -> object:
        """
        Open the QSerialport object for use in the program.
        """
        self.serial_port = QSerialPort(self.settings.value('default_port'))
        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)

class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setupUi(self)
        self.settings = parent.settings
        self.fillPortsInfo()
        self.fillBaudOptions()
        self.fill_data_bits_options()
        self.fill_parity_bits_options()
        self.fill_stop_bits_options()
        self.fill_flow_control_options()

        # If Default_Port is defined set the settings to that and display the port info.
        if self.settings.value("default_port"):
            self.showPortInfo(self.settings.value("default_port"))
            self.serialPortInfoListBox.setCurrentText(self.settings.value("Default_Port"))
            self.settings.beginGroup(self.settings.value("Default_Port"))
            self.baudRateBox.setCurrentText(self.settings.value("baud_rate"))
            self.dataBitsBox.setCurrentText(self.settings.value("data_bits"))
            self.parityBox.setCurrentText(self.settings.value("parity_bits"))
            self.stopBitsBox.setCurrentText(self.settings.value("stop_bits"))
            self.flowControlBox.setCurrentText(self.settings.value("flow_control"))
            self.settings.endGroup()
        else:
            self.showPortInfo(self.serialPortInfoListBox.currentText())

        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.serialPortInfoListBox.currentTextChanged.connect(self.showPortInfo)
        self.buttonBox.accepted.connect(self.update_settings)

    def fillBaudOptions(self) -> None:
        """
        Fill in the Baud rate info options for the serial port. Indications are that only 4800 and 9600 work with
        Kenwood Radios. Need more info to confirm.
        """

        self.baudRateBox.addItem("9600", QSerialPort.BaudRate.Baud9600)
        self.baudRateBox.addItem("4800", QSerialPort.BaudRate.Baud4800)


        return None

    def fill_data_bits_options(self) -> None:
        """
        Fill in the data bits options
        """
        self.dataBitsBox.addItem("8", QSerialPort.DataBits.Data8)
        self.dataBitsBox.addItem("7", QSerialPort.DataBits.Data7)
        self.dataBitsBox.addItem("6", QSerialPort.DataBits.Data6)
        self.dataBitsBox.addItem("5", QSerialPort.DataBits.Data5)

        return None

    def fill_flow_control_options(self) -> None:
        """
        Fill in the flow control options.
        """
        self.flowControlBox.addItem("None", QSerialPort.FlowControl.NoFlowControl)
        self.flowControlBox.addItem("RTS/CTS", QSerialPort.FlowControl.HardwareControl)
        self.flowControlBox.addItem("XON/XOFF", QSerialPort.FlowControl.SoftwareControl)

        return None

    def fill_parity_bits_options(self) -> None:
        """
        Fill in the data bits options
        """
        self.parityBox.addItem("None", QSerialPort.Parity.NoParity)
        self.parityBox.addItem("Even", QSerialPort.Parity.EvenParity)
        self.parityBox.addItem("Odd", QSerialPort.Parity.OddParity)
        self.parityBox.addItem("Mark", QSerialPort.Parity.MarkParity)
        self.parityBox.addItem("Space", QSerialPort.Parity.SpaceParity)

        return None

    def fill_stop_bits_options(self) -> None:
        """
        Fill in the stop bits options
        """
        self.stopBitsBox.addItem("1", QSerialPort.StopBits.OneStop)
        self.stopBitsBox.addItem("1.5", QSerialPort.StopBits.OneAndHalfStop)
        self.stopBitsBox.addItem("2", QSerialPort.StopBits.TwoStop)

        return None

    def fillPortsInfo(self) -> None:
        """
        Fill in the serial port combo box from the available ports on the system and provide extended information
        to be displayed in the settings dialog.
        """
        for port in QSerialPortInfo.availablePorts():
            port_info = {'portName': port.portName(),
                         'description': port.description(),
                         'manufacturer': port.manufacturer(),
                         'serialNumber': port.serialNumber(),
                         'systemLocation': port.systemLocation(),
                         'vendorIdentifier': port.vendorIdentifier(),
                         'productIdentifier': port.productIdentifier()}

            self.serialPortInfoListBox.addItem(port_info['portName'], port_info)

        return None

    def showPortInfo(self, port_name: str) -> None:
        """
        Display serial port information on changes or display.
        """
        index = self.serialPortInfoListBox.findText(port_name)
        port_info = self.serialPortInfoListBox.itemData(index)
        self.locationLabel.setText(f'Location: {port_info["systemLocation"]}')
        self.descriptionLabel.setText(f'Description: {port_info["description"]}')
        self.manufacturerLabel.setText(f'Manufacturer: {port_info["manufacturer"]}')
        self.serialNumberLabel.setText(f'Serial number: {port_info["serialNumber"]}')
        self.vidLabel.setText(f'Vendor ID: {str(port_info["vendorIdentifier"])}')
        self.pidLabel.setText(f'Product ID: {str(port_info["productIdentifier"])}')

    def update_settings(self) -> None:
        """
        Update the settings in permanent storage.
        """
        port_name = self.serialPortInfoListBox.currentText()
        self.settings.setValue("default_port", port_name)
        self.settings.beginGroup(port_name)
        self.settings.setValue("baud_rate", self.baudRateBox.currentText())
        self.settings.setValue("data_bits", self.dataBitsBox.currentText())
        self.settings.setValue("parity", self.parityBox.currentText())
        self.settings.setValue("stop_bits", self.stopBitsBox.currentText())
        self.settings.setValue("flow_control", self.flowControlBox.currentText())
        self.settings.endGroup()
        # Flush to permanent storage
        self.settings.sync()

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
