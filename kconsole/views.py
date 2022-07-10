# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""
import os

from PyQt6.QtCore import Qt, QIODevice, QSettings
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QVBoxLayout
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

        self.settings = self.load_settings()
        self.saved_settings = QSettings()
        self.setupUi(self)
        self.connect_signals_slots()

        if not self.saved_settings.contains('default_port'):
            self.open_settings_dialog()

        self.serial_port = None
        self.open_serial_port()
        self.ksync = KSync(self.serial_port)

    def connect_signals_slots(self):
        self.actionExit.triggered.connect(self.close)
        self.broadcastButton.clicked.connect(self.open_broadcast_message_dialog)
        self.settingsButton.clicked.connect(self.open_settings_dialog)

    def load_settings(self) -> dict:
        """
        Load the current program settings.
        """

        dialog = SettingsDialog(self)
        return dialog.program_settings

    def open_broadcast_message_dialog(self):
        """
        Open the Broadcast Message dialog.
        """

        dialog = BroadcastDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.send_text(dialog.message, broadcast=True)

    def open_settings_dialog(self) -> None:
        """
        Open the settings dialog.
        """

        dialog = SettingsDialog(self)
        dialog.exec()
        return None

    def open_serial_port(self) -> None:
        """
        Open the QSerialport object for use in the program.
        """

        self.serial_port = QSerialPort(self.saved_settings.value("default_port"))
        self.serial_port.setBaudRate(self.settings["baud_rate"].value)
        self.serial_port.setParity(self.settings["parity"])
        self.serial_port.setDataBits(self.settings["data_bits"])
        self.serial_port.setStopBits(self.settings["stop_bits"])
        self.serial_port.setFlowControl(self.settings["flow_control"])

        self.serial_port.open(QIODevice.OpenModeFlag.ReadWrite)

    def close_serial_port(self) -> None:
        """
        Close the serial port if it was open.
        """
        if self.serial_port.isOpen():
            self.serial_port.close()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setupUi(self)
        self.saved_settings = QSettings()
        self.program_settings = {}
        self.fillPortsInfo()
        self.fill_baud_options()
        self.fill_data_bits_options()
        self.fill_parity_bits_options()
        self.fill_stop_bits_options()
        self.fill_flow_control_options()

        # If Default_Port is defined set the settings to that and display the port info.
        if self.saved_settings.value("default_port"):
            self.serialPortInfoListBox.setCurrentText(self.saved_settings.value("default_port"))
            self.showPortInfo(self.serialPortInfoListBox.currentIndex())
            self.saved_settings.beginGroup(self.serialPortInfoListBox.currentText())
            self.baudRateBox.setCurrentText(self.saved_settings.value("baud_rate"))
            self.dataBitsBox.setCurrentText(self.saved_settings.value("data_bits"))
            self.parityBox.setCurrentText(self.saved_settings.value("parity_bits"))
            self.stopBitsBox.setCurrentText(self.saved_settings.value("stop_bits"))
            self.flowControlBox.setCurrentText(self.saved_settings.value("flow_control"))
            self.saved_settings.endGroup()
        else:
            self.showPortInfo(self.serialPortInfoListBox.currentIndex())

        self.update_program_settings()
        self.connect_signal_slots()

    def connect_signal_slots(self):
        """
        Connect the signals to the slots.
        """

        self.serialPortInfoListBox.currentIndexChanged.connect(self.showPortInfo)
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.accepted.connect(self.update_program_settings)

    def fill_baud_options(self) -> None:
        """
        Fill in the Baud rate info options for the serial port.
        Indications are that only 4800 and 9600 work with
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
        Fill in the serial port combo box from the available ports on the system
        and provide extended information to be displayed in the settings dialog.
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

    def showPortInfo(self, index: int) -> None:
        """
        Display serial port information on changes or display.
        """

        if index != -1:
            port_info = self.serialPortInfoListBox.itemData(index)
            self.locationLabel.setText(f'Location: {port_info["systemLocation"]}')
            self.descriptionLabel.setText(f'Description: {port_info["description"]}')
            self.manufacturerLabel.setText(f'Manufacturer: {port_info["manufacturer"]}')
            self.serialNumberLabel.setText(f'Serial number: {port_info["serialNumber"]}')
            self.vidLabel.setText(f'Vendor ID: {str(port_info["vendorIdentifier"])}')
            self.pidLabel.setText(f'Product ID: {str(port_info["productIdentifier"])}')

        return None

    def update_program_settings(self) -> None:
        """
        Update the program settings.
        """

        self.program_settings["baud_rate"] = self.baudRateBox.currentData()
        self.program_settings["data_bits"] = self.dataBitsBox.currentData()
        self.program_settings["parity"] = self.parityBox.currentData()
        self.program_settings["stop_bits"] = self.stopBitsBox.currentData()
        self.program_settings["flow_control"] = self.flowControlBox.currentData()

    def save_settings(self) -> None:
        """
        Save the settings in permanent storage.
        """

        port_name = self.serialPortInfoListBox.currentText()

        self.saved_settings.setValue("default_port", port_name)
        self.saved_settings.beginGroup(port_name)
        self.saved_settings.setValue("baud_rate", self.baudRateBox.currentText())
        self.saved_settings.setValue("data_bits", self.dataBitsBox.currentText())
        self.saved_settings.setValue("parity", self.parityBox.currentText())
        self.saved_settings.setValue("stop_bits", self.stopBitsBox.currentText())
        self.saved_settings.setValue("flow_control", self.flowControlBox.currentText())
        self.saved_settings.endGroup()
        # Flush to permanent storage
        self.saved_settings.sync()

        return None


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
