# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'queryLocationDialog.ui'
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
    QFormLayout, QLabel, QSizePolicy, QSpinBox,
    QWidget)

class Ui_QueryLocationDialog(object):
    def setupUi(self, QueryLocationDialog):
        if not QueryLocationDialog.objectName():
            QueryLocationDialog.setObjectName(u"QueryLocationDialog")
        QueryLocationDialog.resize(400, 147)
        self.formLayout = QFormLayout(QueryLocationDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.buttonBox = QDialogButtonBox(QueryLocationDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.buttonBox)

        self.label_2 = QLabel(QueryLocationDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.label = QLabel(QueryLocationDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.fleetIdSpinBox = QSpinBox(QueryLocationDialog)
        self.fleetIdSpinBox.setObjectName(u"fleetIdSpinBox")
        self.fleetIdSpinBox.setMinimum(100)
        self.fleetIdSpinBox.setMaximum(349)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.fleetIdSpinBox)

        self.deviceIdSpinBox = QSpinBox(QueryLocationDialog)
        self.deviceIdSpinBox.setObjectName(u"deviceIdSpinBox")
        self.deviceIdSpinBox.setMinimum(1000)
        self.deviceIdSpinBox.setMaximum(4999)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.deviceIdSpinBox)


        self.retranslateUi(QueryLocationDialog)
        self.buttonBox.accepted.connect(QueryLocationDialog.accept)
        self.buttonBox.rejected.connect(QueryLocationDialog.reject)

        QMetaObject.connectSlotsByName(QueryLocationDialog)
    # setupUi

    def retranslateUi(self, QueryLocationDialog):
        QueryLocationDialog.setWindowTitle(QCoreApplication.translate("QueryLocationDialog", u"Query Radio Location", None))
        self.label_2.setText(QCoreApplication.translate("QueryLocationDialog", u"Fleet ID:", None))
        self.label.setText(QCoreApplication.translate("QueryLocationDialog", u"Device ID:", None))
    # retranslateUi

