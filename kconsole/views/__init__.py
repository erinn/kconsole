# -*- coding: utf-8 -*-

"""This module provides views to manage the radios table."""
import logging

# Resources looks unused, it isn't, and it needs to remain as long as there are icons.
import kconsole.ui.resources

from PySide6.QtCore import QIODevice, QPoint, QSettings, Qt
from PySide6.QtGui import QIcon
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStatusBar,
)
from ksync.ksync import KSync
from kconsole.logs import ConsoleWindowLogHandler
from kconsole.models import RadiosModel
from kconsole.views.add_dialog import AddDialog
from kconsole.ui.logging_dialog_ui import Ui_loggingDialog
from kconsole.ui.main_window_ui import Ui_MainWindow
from kconsole.views.query_location_dialog import QueryLocationDialog
from kconsole.views.settings_dialog import SettingsDialog
from kconsole.views.text_dialog import TextDialog

logger = logging.getLogger(__name__)


class Window(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.settings = self.load_settings()
        self.saved_settings = QSettings()
        self.setupUi(self)

        # Configure Console Logger, we do this as early as possible to capture as much as possible.
        self.console_handler = ConsoleWindowLogHandler()
        logging.getLogger().addHandler(self.console_handler)
        self._console_dialog = LoggingDialog(self)
        self.console_handler.bridge.sigLog.connect(
            self._console_dialog.loggingConsole.appendPlainText
        )
        logger.debug("Logging configured.")

        # Create the main DB interface.
        self.radiosModel = RadiosModel()
        self.radioTable.setModel(self.radiosModel.model)
        self.radioTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.radioTable.resizeColumnsToContents()
        self.radioTable.verticalHeader().hide()
        self.radioTable.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # Hide the primary key/ID as users don't care.
        self.radioTable.setColumnHidden(0, True)

        self.actionSettings.setIcon(QIcon(":/icons/settings"))
        self.actionLoggingConsole.setIcon(QIcon(":/icons/terminal"))
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
        self.actionQueryLocation.triggered.connect(self.open_query_location_dialog)
        self.actionLoggingConsole.triggered.connect(self.open_logging_dialog)
        self.actionSettings.triggered.connect(self.open_settings_dialog)
        self.actionTextRadio.triggered.connect(self.open_text_dialog)
        self.addButton.clicked.connect(self.open_add_dialog)
        self.broadcastButton.clicked.connect(self.open_broadcast_message_dialog)
        self.deleteButton.clicked.connect(self.delete_radio)
        self.radioTable.customContextMenuRequested.connect(
            self.radio_table_context_menu
        )
        self.serial_port.readyRead.connect(self.display_data_statusbar)

    def delete_radio(self) -> None:
        """
        Delete a row in the DB representing a device.

        :return: None
        """
        row = self.radioTable.currentIndex().row()
        if row < 0:
            return

        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected device?",
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

        dialog = TextDialog(self)
        dialog.broadcastCheckBox.setChecked(True)
        if dialog.exec() == QDialog.DialogCode.Accepted:

            if dialog.broadcast:
                self.ksync.send_text(message=dialog.message, broadcast=dialog.broadcast)
            else:
                self.ksync.send_text(
                    message=dialog.message,
                    fleet_id=dialog.fleet_id,
                    device_id=dialog.device_id,
                )

    def open_logging_dialog(self) -> None:
        """
        Open the logging 'Console' in a non modal QDialog.

        The QDialog is already initalized much further up but it is hidden.
        This method simply shows the hidden dialog.

        :return: None
        """

        self._console_dialog.show()

        logger.debug("Logging console called.")

    def open_query_location_dialog(self) -> None:
        """
        Open the query location dialog and populate with data if possible.

        :return: None
        """
        record = self.radiosModel.model.record(self.radioTable.currentIndex().row())

        dialog = QueryLocationDialog(
            self, fleet_id=record.value("fleet_id"), device_id=record.value("device_id")
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.poll_gnss(fleet_id=dialog.fleet_id, device_id=dialog.device_id)

    def open_settings_dialog(self) -> None:
        """
        Open the settings dialog.

        :return: None
        """

        dialog = SettingsDialog(self)
        dialog.exec()

    def open_text_dialog(self) -> None:
        """
        Open the text radio dialog.

        :return: None
        """
        record = self.radiosModel.model.record(self.radioTable.currentIndex().row())
        fleet_id = record.value("fleet_id")
        device_id = record.value("device_id")

        dialog = TextDialog(self, fleet_id=fleet_id, device_id=device_id)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.ksync.send_text(
                message=dialog.message,
                fleet_id=dialog.fleet_id,
                device_id=dialog.device_id,
            )

    def open_serial_port(self) -> None:
        """
        Open the QSerialport object for use in the program.
        """

        self.serial_port = QSerialPort(self.saved_settings.value("default_port"))
        self.serial_port.setBaudRate(self.settings["baud_rate"])
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
        context.addAction(self.actionTextRadio)
        context.exec(self.radioTable.mapToGlobal(position))


class LoggingDialog(QDialog, Ui_loggingDialog):
    """
    Logging Dialog
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
