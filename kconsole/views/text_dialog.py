from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStatusBar,
)

from kconsole.ui.text_dialog_ui import Ui_TextDialog


class TextDialog(QDialog, Ui_TextDialog):
    """Text Radio Dialog."""

    def __init__(self, parent=None, fleet_id: int = None, device_id: int = None):
        """Initializer."""
        super().__init__(parent=parent)
        self.broadcast = False
        self.fleet_id = fleet_id
        self.device_id = device_id
        self.message = ""
        self.setupUi(self)

        if self.fleet_id:
            self.fleetIdSpinBox.setValue(self.fleet_id)

        if self.device_id:
            self.deviceIdSpinBox.setValue(self.device_id)

        self.connect_signal_slots()

    def accept(self) -> None:
        """
        Accept the message provided through the dialog.

        :return: None
        """
        self.broadcast = self.broadcastCheckBox.isChecked()
        self.device_id = self.deviceIdSpinBox.text()
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
