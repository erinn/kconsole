from PySide6.QtCore import QSettings
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import QDialog

from kconsole.ui.settings_dialog_ui import Ui_SettingsDialog


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
