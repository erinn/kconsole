from PySide6.QtWidgets import QDialog

from kconsole.ui.query_location_dialog_ui import Ui_QueryLocationDialog


class QueryLocationDialog(QDialog, Ui_QueryLocationDialog):
    """
    Query Location Dialog
    """

    def __init__(
        self, parent: object = None, fleet_id: int = None, device_id: int = None
    ):
        """
        :param parent: parent object for cleanup and centering.
        :param fleet_id: The fleet ID of the device to query.
        :param device_id: The device ID (radio ID) of the device to query.
        """
        super().__init__(parent=parent)
        self.fleet_id = fleet_id
        self.device_id = device_id
        self.setupUi(self)

        # This dialog can either be called with known values or not.
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
        self.fleet_id = self.fleetIdSpinBox.text()
        self.device_id = self.deviceIdSpinBox.text()

        # TODO, simple validation.

        if not self.fleet_id or not self.device_id:
            return

        super().accept()

    def connect_signal_slots(self) -> None:
        """
        Connect signals to slots.

        :return: None
        """
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
