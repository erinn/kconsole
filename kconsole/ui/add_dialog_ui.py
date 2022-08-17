# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QSpinBox, QWidget)

class Ui_AddDialog(object):
    def setupUi(self, AddDialog):
        if not AddDialog.objectName():
            AddDialog.setObjectName(u"AddDialog")
        AddDialog.resize(389, 174)
        self.formLayout = QFormLayout(AddDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.nameLabel = QLabel(AddDialog)
        self.nameLabel.setObjectName(u"nameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

        self.nameField = QLineEdit(AddDialog)
        self.nameField.setObjectName(u"nameField")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nameField)

        self.fleetIdLabel = QLabel(AddDialog)
        self.fleetIdLabel.setObjectName(u"fleetIdLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.fleetIdLabel)

        self.deviceIdLabel = QLabel(AddDialog)
        self.deviceIdLabel.setObjectName(u"deviceIdLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.deviceIdLabel)

        self.buttonBox = QDialogButtonBox(AddDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.buttonBox)

        self.fleetIdspinBox = QSpinBox(AddDialog)
        self.fleetIdspinBox.setObjectName(u"fleetIdspinBox")
        self.fleetIdspinBox.setMinimum(100)
        self.fleetIdspinBox.setMaximum(349)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fleetIdspinBox)

        self.deviceIdspinBox = QSpinBox(AddDialog)
        self.deviceIdspinBox.setObjectName(u"deviceIdspinBox")
        self.deviceIdspinBox.setMinimum(1000)
        self.deviceIdspinBox.setMaximum(4999)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.deviceIdspinBox)


        self.retranslateUi(AddDialog)
        self.buttonBox.accepted.connect(AddDialog.accept)
        self.buttonBox.rejected.connect(AddDialog.reject)

        QMetaObject.connectSlotsByName(AddDialog)
    # setupUi

    def retranslateUi(self, AddDialog):
        AddDialog.setWindowTitle(QCoreApplication.translate("AddDialog", u"Add Radio", None))
        self.nameLabel.setText(QCoreApplication.translate("AddDialog", u"Name:", None))
#if QT_CONFIG(statustip)
        self.nameField.setStatusTip(QCoreApplication.translate("AddDialog", u"An informal name for the radio, i.e. 'Truck Radio'.", None))
#endif // QT_CONFIG(statustip)
        self.fleetIdLabel.setText(QCoreApplication.translate("AddDialog", u"Fleet ID:", None))
        self.deviceIdLabel.setText(QCoreApplication.translate("AddDialog", u"Device ID:", None))
    # retranslateUi

