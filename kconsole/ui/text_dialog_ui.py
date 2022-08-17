# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'textDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QSpinBox, QWidget)

class Ui_TextDialog(object):
    def setupUi(self, TextDialog):
        if not TextDialog.objectName():
            TextDialog.setObjectName(u"TextDialog")
        TextDialog.resize(400, 253)
        self.formLayout = QFormLayout(TextDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.fleetIdLabel = QLabel(TextDialog)
        self.fleetIdLabel.setObjectName(u"fleetIdLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.fleetIdLabel)

        self.fleetIdSpinBox = QSpinBox(TextDialog)
        self.fleetIdSpinBox.setObjectName(u"fleetIdSpinBox")
        self.fleetIdSpinBox.setMinimum(100)
        self.fleetIdSpinBox.setMaximum(349)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.fleetIdSpinBox)

        self.deviceIdLabel = QLabel(TextDialog)
        self.deviceIdLabel.setObjectName(u"deviceIdLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.deviceIdLabel)

        self.deviceIdSpinBox = QSpinBox(TextDialog)
        self.deviceIdSpinBox.setObjectName(u"deviceIdSpinBox")
        self.deviceIdSpinBox.setMinimum(1000)
        self.deviceIdSpinBox.setMaximum(4999)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.deviceIdSpinBox)

        self.buttonBox = QDialogButtonBox(TextDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.buttonBox)

        self.messageLabel = QLabel(TextDialog)
        self.messageLabel.setObjectName(u"messageLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.messageLabel)

        self.radioMessage = QLineEdit(TextDialog)
        self.radioMessage.setObjectName(u"radioMessage")
        self.radioMessage.setMaxLength(4096)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.radioMessage)

        self.broadcastCheckBox = QCheckBox(TextDialog)
        self.broadcastCheckBox.setObjectName(u"broadcastCheckBox")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.broadcastCheckBox)


        self.retranslateUi(TextDialog)
        self.buttonBox.accepted.connect(TextDialog.accept)
        self.buttonBox.rejected.connect(TextDialog.reject)
        self.broadcastCheckBox.toggled.connect(self.fleetIdSpinBox.setDisabled)
        self.broadcastCheckBox.toggled.connect(self.deviceIdSpinBox.setDisabled)

        QMetaObject.connectSlotsByName(TextDialog)
    # setupUi

    def retranslateUi(self, TextDialog):
        TextDialog.setWindowTitle(QCoreApplication.translate("TextDialog", u"Text Radio", None))
        self.fleetIdLabel.setText(QCoreApplication.translate("TextDialog", u"Fleet ID:", None))
        self.deviceIdLabel.setText(QCoreApplication.translate("TextDialog", u"Device ID:", None))
        self.messageLabel.setText(QCoreApplication.translate("TextDialog", u"Message:", None))
#if QT_CONFIG(tooltip)
        self.broadcastCheckBox.setToolTip(QCoreApplication.translate("TextDialog", u"When checked Fleet ID and Device ID are disabled.", None))
#endif // QT_CONFIG(tooltip)
        self.broadcastCheckBox.setText(QCoreApplication.translate("TextDialog", u"Broadcast", None))
    # retranslateUi

