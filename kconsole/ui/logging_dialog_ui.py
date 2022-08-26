# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loggingDialog.ui'
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
    QPlainTextEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_loggingDialog(object):
    def setupUi(self, loggingDialog):
        if not loggingDialog.objectName():
            loggingDialog.setObjectName(u"loggingDialog")
        loggingDialog.resize(400, 300)
        loggingDialog.setModal(False)
        self.verticalLayout = QVBoxLayout(loggingDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.loggingConsole = QPlainTextEdit(loggingDialog)
        self.loggingConsole.setObjectName(u"loggingConsole")
        self.loggingConsole.setReadOnly(True)

        self.verticalLayout.addWidget(self.loggingConsole)

        self.buttonBox = QDialogButtonBox(loggingDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(loggingDialog)
        self.buttonBox.accepted.connect(loggingDialog.accept)
        self.buttonBox.rejected.connect(loggingDialog.reject)

        QMetaObject.connectSlotsByName(loggingDialog)
    # setupUi

    def retranslateUi(self, loggingDialog):
        loggingDialog.setWindowTitle(QCoreApplication.translate("loggingDialog", u"Log Console", None))
    # retranslateUi

