# -*- coding: utf-8 -*-

"""This module provides views to manage the radios table."""
import os

from PyQt6.QtCore import QIODevice, QPoint, QSettings, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStatusBar,
)
from ksync.ksync import KSync
from kconsole.add_dialog_ui import Ui_AddDialog
from kconsole.broadcast_dialog_ui import Ui_BroadcastDialog
from kconsole.main_window_ui import Ui_MainWindow
from kconsole.models import RadiosModel
from kconsole.query_location_dialog_ui import Ui_QueryLocationDialog
from kconsole.settings_dialog_ui import Ui_SettingsDialog
from kconsole.text_dialog_ui import Ui_TextDialog


basedir = os.path.dirname(__file__)


class Window(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.settings = self.load_settings()
        self.saved_settings = QSettings()
        self.setupUi(self)
        self.radiosModel = RadiosModel()
        self.radioTable.setModel(self.radiosModel.model)
        self.radioTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.radioTable.resizeColumnsToContents()
        self.radioTable.verticalHeader().hide()
        self.radioTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.actionSettings.setIcon(
            QIcon(os.path.join(basedir, "ui/resources/gear.png"))
        )
        self.menuWindow.addAction(self.toolBar.toggleViewAction())
        self.setStatusBar(QStatusBar(self))

        if not self.saved_settings.contains("default_port"):
            self.open_settings_dialog()

        self.serial_port = None
        self.open_serial_port()
        self.ksync = KSync(self.serial_port)
        self.connect_signals_slots()

    def close_serial_port(self) -> None:
        """
        Close the serial port if it was open.

        :return: None
        """

        if self.serial_port.isOpen():
            self.serial_port.close()

    def connect_signals_slots(self) -> None:
        """
        Connect signals to slots.
        """

        self.actionExit.triggered.connect(self.close)
        self.actionSettings.triggered.connect(self.open_settings_dialog)
        self.actionactionTextRadio.triggered.connect(self.open_text_dialog)
        self.actionQueryLocation.triggered.connect(self.open_query_location_dialog)
        self.addButton.clicked.connect(self.open_add_dialog)
        self.broadcastButton.clicked.connect(self.open_broadcast_message_dialog)
        self.deleteButton.clicked.connect(self.delete_radio)
        self.radioTable.customContextMenuRequested.connect(self.radio_table_context_menu)
        self.serial_port.readyRead.connect(self.display_data_statusbar)

    def delete_radio(self) -> None:
        """
        Delete a row in the DB representing a radio.

        :return: None
        """
        row = self.radioTable.currentIndex().row()
        if row < 0:
            return

        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected radio?",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
        )

        if message_box == QMessageBox.StandardButton.Ok:
            self.radiosModel.delete_radio(row)

    def display_data_statusbar(self) -> None:
        """
        Display raw serial data on the status bar as it is received.

        :return: None
        """
        line = self.serial_port.readLine()
        self.statusBar().showMessage(bytes(line).decode())

    def load_settings(self) -> dict:
        """
        Load the current program settings.
        """

        dialog = SettingsDialog(self)
        return dialog.program_settings

    def open_add_dialog(self) -> None:
        """
        Open the add radio dialog.

        :return: None
        """

        dialog = AddDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.radiosModel.add_radio(dialog.data)
            self.radioTable.resizeColumnsToContents()

    def open_broadcast_message_dialog(self) -> None:
        """
        Open the Broadcast Message dialog.
        """

        dialog = BroadcastDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.send_text(dialog.message, broadcast=True)

    def open_query_location_dialog(self) -> None:
        """
        Open the query location dialog and populate with data if possible.

        :return: None
        """
        record = self.radiosModel.model.record(self.radioTable.currentIndex().row())

        dialog = QueryLocationDialog(self, fleet_id=record.value('fleet'), radio_id=record.value('device_id'))

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.poll_gnss(fleet=dialog.fleet_id, device=dialog.radio_id)

    def open_text_dialog(self) -> None:
        """
        Open the text radio dialog.

        :return: None
        """
        dialog = TextDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.send_text(message=dialog.message, fleet=dialog.fleet_id, device=dialog.radio_id)

    def open_settings_dialog(self) -> None:
        """
        Open the settings dialog.

        :return: None
        """

        dialog = SettingsDialog(self)
        dialog.exec()

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

    def radio_table_context_menu(self, position: QPoint) -> None:
        """
        Display context menu on right click of radio table.

        :param position:
        :return: None
        """

        context = QMenu(self)
        context.addAction(self.actionQueryLocation)
        context.addAction(self.actionactionTextRadio)
        context.exec(self.radioTable.mapToGlobal(position))


class AddDialog(QDialog, Ui_AddDialog):
    """
    Add entries to DB dialog.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.data = []

    def accept(self) -> None:
        """
        Perform validation on data before sending accept up the stack.

        :return: None
        """

        if len(self.fleetIdField.text()) != 3:
            QMessageBox.critical(self, "Error", "Fleet ID must be three characters.")
            return

        if len(self.deviceIdField.text()) != 4:
            QMessageBox.critical(self, "Error", "Device ID must be four characters.")
            return

        for field in (self.nameField, self.fleetIdField, self.deviceIdField):
            if not field.text():
                QMessageBox.critical(
                    self, "Error", f"You must provide {field.objectName()}."
                )
                return

            self.data.append(field.text())

        super().accept()


class SettingsDialog(QDialog, Ui_SettingsDialog):
    """
    Build the settings dialog.
    """

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.setupUi(self)
        self.saved_settings = QSettings()
        self.program_settings = {}
        self.fill_ports_info()
        self.fill_baud_options()
        self.fill_data_bits_options()
        self.fill_parity_bits_options()
        self.fill_stop_bits_options()
        self.fill_flow_control_options()

        # If Default_Port is defined set the settings to that and display the port info.
        if self.saved_settings.value("default_port"):
            self.serialPortInfoListBox.setCurrentText(
                self.saved_settings.value("default_port")
            )
            self.show_port_info(self.serialPortInfoListBox.currentIndex())
            self.saved_settings.beginGroup(self.serialPortInfoListBox.currentText())
            self.baudRateBox.setCurrentText(self.saved_settings.value("baud_rate"))
            self.dataBitsBox.setCurrentText(self.saved_settings.value("data_bits"))
            self.parityBox.setCurrentText(self.saved_settings.value("parity_bits"))
            self.stopBitsBox.setCurrentText(self.saved_settings.value("stop_bits"))
            self.flowControlBox.setCurrentText(
                self.saved_settings.value("flow_control")
            )
            self.saved_settings.endGroup()
        else:
            self.show_port_info(self.serialPortInfoListBox.currentIndex())

        self.update_program_settings()
        self.connect_signal_slots()

    def connect_signal_slots(self) -> None:
        """
        Connect the signals to the slots.
        """

        self.serialPortInfoListBox.currentIndexChanged.connect(self.show_port_info)
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

    def fill_data_bits_options(self) -> None:
        """
        Fill in the data bits options
        """

        self.dataBitsBox.addItem("8", QSerialPort.DataBits.Data8)
        self.dataBitsBox.addItem("7", QSerialPort.DataBits.Data7)
        self.dataBitsBox.addItem("6", QSerialPort.DataBits.Data6)
        self.dataBitsBox.addItem("5", QSerialPort.DataBits.Data5)

    def fill_flow_control_options(self) -> None:
        """
        Fill in the flow control options.
        """

        self.flowControlBox.addItem("None", QSerialPort.FlowControl.NoFlowControl)
        self.flowControlBox.addItem("RTS/CTS", QSerialPort.FlowControl.HardwareControl)
        self.flowControlBox.addItem("XON/XOFF", QSerialPort.FlowControl.SoftwareControl)

    def fill_parity_bits_options(self) -> None:
        """
        Fill in the data bits options.
        """

        self.parityBox.addItem("None", QSerialPort.Parity.NoParity)
        self.parityBox.addItem("Even", QSerialPort.Parity.EvenParity)
        self.parityBox.addItem("Odd", QSerialPort.Parity.OddParity)
        self.parityBox.addItem("Mark", QSerialPort.Parity.MarkParity)
        self.parityBox.addItem("Space", QSerialPort.Parity.SpaceParity)

    def fill_stop_bits_options(self) -> None:
        """
        Fill in the stop bits options.
        """

        self.stopBitsBox.addItem("1", QSerialPort.StopBits.OneStop)
        self.stopBitsBox.addItem("1.5", QSerialPort.StopBits.OneAndHalfStop)
        self.stopBitsBox.addItem("2", QSerialPort.StopBits.TwoStop)

    def fill_ports_info(self) -> None:
        """
        Fill in the serial port combo box from the available ports on the system
        and provide extended information to be displayed in the settings dialog.
        """

        for port in QSerialPortInfo.availablePorts():
            port_info = {
                "portName": port.portName(),
                "description": port.description(),
                "manufacturer": port.manufacturer(),
                "serialNumber": port.serialNumber(),
                "systemLocation": port.systemLocation(),
                "vendorIdentifier": port.vendorIdentifier(),
                "productIdentifier": port.productIdentifier(),
            }

            self.serialPortInfoListBox.addItem(port_info["portName"], port_info)

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

    def show_port_info(self, index: int) -> None:
        """
        Display serial port information on changes or display.
        """

        if index != -1:
            port_info = self.serialPortInfoListBox.itemData(index)
            self.locationLabel.setText(f'Location: {port_info["systemLocation"]}')
            self.descriptionLabel.setText(f'Description: {port_info["description"]}')
            self.manufacturerLabel.setText(f'Manufacturer: {port_info["manufacturer"]}')
            self.serialNumberLabel.setText(
                f'Serial number: {port_info["serialNumber"]}'
            )
            self.vidLabel.setText(f'Vendor ID: {str(port_info["vendorIdentifier"])}')
            self.pidLabel.setText(f'Product ID: {str(port_info["productIdentifier"])}')

    def update_program_settings(self) -> None:
        """
        Update the program settings. These are the actual objects that hold
        the setting state. QSettings can not handle objects so it is mapped
        through the combo boxes.
        """

        self.program_settings["baud_rate"] = self.baudRateBox.currentData()
        self.program_settings["data_bits"] = self.dataBitsBox.currentData()
        self.program_settings["parity"] = self.parityBox.currentData()
        self.program_settings["stop_bits"] = self.stopBitsBox.currentData()
        self.program_settings["flow_control"] = self.flowControlBox.currentData()


class BroadcastDialog(QDialog, Ui_BroadcastDialog):
    """Broadcast dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.message = ""
        self.setupUi(self)
        self.connect_signal_slots()

    def accept(self) -> None:
        """Accept the message provided through the dialog."""
        self.message = self.broadcastMessage.text()

        if len(self.message) > 4096:
            QMessageBox.critical(
                self,
                "Error!",
                "Message size must not exceed 4096 characters.",
            )

        if not self.message:
            return

        super().accept()

    def connect_signal_slots(self) -> None:
        """
        Connect signals to slots.

        :return: None
        """
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


class QueryLocationDialog(QDialog, Ui_QueryLocationDialog):
    """
    Query Location Dialog
    """
    def __init__(self, parent: object = None, fleet_id: str = None, radio_id: str =None):
        """

        :param parent:
        :param fleet_id:
        :param radio_id:
        """
        super().__init__(parent=parent)
        self.fleet_id = fleet_id
        self.radio_id = radio_id
        self.setupUi(self)

        if self.fleet_id:
            self.fleetId.setText(self.fleet_id)

        if self.radio_id:
            self.radioId.setText(self.radio_id)

        self.connect_signal_slots()

    def accept(self) -> None:
        """
        Accept the message provided through the dialog.

        :return: None
        """
        self.fleet_id = self.fleetId.text()
        self.radio_id = self.radioId.text()

        # TODO, simple validation.

        if not self.fleet_id or not self.radio_id:
            return

        super().accept()

    def connect_signal_slots(self) -> None:
        """
        Connect signals to slots.

        :return: None
        """
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


class TextDialog(QDialog, Ui_TextDialog):
    """Text Radio Dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent=parent)
        self.fleet_id = ""
        self.radio_id = ""
        self.message = ""
        self.setupUi(self)
        self.connect_signal_slots()

    def accept(self) -> None:
        """
        Accept the message provided through the dialog.

        :return: None
        """
        self.radio_id = self.deviceIdSpinBox.text()
        self.fleet_id = self.fleetIdSpinBox.text()
        self.message = self.radioMessage.text()

        # TODO: Smaller message inside window instead?
        if len(self.message) > 4096:
            QMessageBox.critical(
                self,
                "Error!",
                "Message size must not exceed 4096 characters.",
            )

        if not self.message:
            return

        super().accept()

    def connect_signal_slots(self) -> None:
        """
        Connect signals to slots.

        :return: None
        """
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
