# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableView, QToolBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(988, 686)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionSettings.setIconVisibleInMenu(False)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionToolbar = QAction(MainWindow)
        self.actionToolbar.setObjectName(u"actionToolbar")
        self.actionToolbar.setCheckable(True)
        self.actionQueryLocation = QAction(MainWindow)
        self.actionQueryLocation.setObjectName(u"actionQueryLocation")
        self.actionTextRadio = QAction(MainWindow)
        self.actionTextRadio.setObjectName(u"actionTextRadio")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioTable = QTableView(self.widget)
        self.radioTable.setObjectName(u"radioTable")

        self.verticalLayout.addWidget(self.radioTable)


        self.horizontalLayout.addWidget(self.widget)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout_2.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.centralwidget)
        self.deleteButton.setObjectName(u"deleteButton")

        self.verticalLayout_2.addWidget(self.deleteButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.broadcastButton = QPushButton(self.centralwidget)
        self.broadcastButton.setObjectName(u"broadcastButton")

        self.verticalLayout_2.addWidget(self.broadcastButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 988, 36))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"KConsole", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings...", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionToolbar.setText(QCoreApplication.translate("MainWindow", u"Toolbar", None))
#if QT_CONFIG(tooltip)
        self.actionToolbar.setToolTip(QCoreApplication.translate("MainWindow", u"Show/Hide Toolbar", None))
#endif // QT_CONFIG(tooltip)
        self.actionQueryLocation.setText(QCoreApplication.translate("MainWindow", u"Query Location", None))
#if QT_CONFIG(tooltip)
        self.actionQueryLocation.setToolTip(QCoreApplication.translate("MainWindow", u"Query the radio's location", None))
#endif // QT_CONFIG(tooltip)
        self.actionTextRadio.setText(QCoreApplication.translate("MainWindow", u"Text Radio", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.broadcastButton.setText(QCoreApplication.translate("MainWindow", u"Broadcast", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", u"Window", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tool Bar", None))
    # retranslateUi

