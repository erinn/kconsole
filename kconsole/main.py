# -*- coding: utf-8 -*-
# rpcontacts/kconsole.py

"""This module provides RP Contacts application."""

import sys

from PyQt6.QtWidgets import QApplication
from .database import create_connection

from kconsole.views import Window


def main():
    """RP Contacts main function."""
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("KConsole")
    app.setApplicationName("KConsole")
    app.setOrganizationName("SARStats")
    app.setOrganizationDomain("sarstats.com")
    # Connect to the database before creating any window
    if not create_connection("KConsole.sqlite"):
        sys.exit(1)
    # Create the main window
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())
