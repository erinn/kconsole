from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
)
from kconsole.ui.add_dialog_ui import Ui_AddDialog


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

        if len(self.fleetIdspinBox.text()) != 3:
            QMessageBox.critical(self, "Error", "Fleet ID must be three characters.")
            return

        if len(self.deviceIdspinBox.text()) != 4:
            QMessageBox.critical(self, "Error", "Device ID must be four characters.")
            return

        for field in (self.nameField, self.fleetIdspinBox, self.deviceIdspinBox):
            if not field.text():
                QMessageBox.critical(
                    self, "Error", f"You must provide {field.objectName()}."
                )
                return

            self.data.append(field.text())

        super().accept()
