# Form implementation generated from reading ui file 'ui/broadcastDialog.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_BroadcastDialog(object):
    def setupUi(self, BroadcastDialog):
        BroadcastDialog.setObjectName("BroadcastDialog")
        BroadcastDialog.resize(404, 90)
        self.formLayout = QtWidgets.QFormLayout(BroadcastDialog)
        self.formLayout.setObjectName("formLayout")
        self.broadcastMessage = QtWidgets.QLineEdit(BroadcastDialog)
        self.broadcastMessage.setText("")
        self.broadcastMessage.setObjectName("broadcastMessage")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.broadcastMessage)
        self.broadcastMessageLabel = QtWidgets.QLabel(BroadcastDialog)
        self.broadcastMessageLabel.setObjectName("broadcastMessageLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.broadcastMessageLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(BroadcastDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.buttonBox)

        self.retranslateUi(BroadcastDialog)
        self.buttonBox.accepted.connect(BroadcastDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(BroadcastDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(BroadcastDialog)

    def retranslateUi(self, BroadcastDialog):
        _translate = QtCore.QCoreApplication.translate
        BroadcastDialog.setWindowTitle(_translate("BroadcastDialog", "Dialog"))
        self.broadcastMessage.setPlaceholderText(_translate("BroadcastDialog", "Broadcast Message..."))
        self.broadcastMessageLabel.setText(_translate("BroadcastDialog", "Boradcast Message:"))
