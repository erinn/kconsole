# -*- coding: utf-8 -*-
# rpcontacts/model.py

"""This module provides a model to manage the contacts table."""

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlTableModel


class RadiosModel:
    def __init__(self):
        self.model = self._create_model()

    @staticmethod
    def _create_model():
        """Create and set up the model."""
        tableModel = QSqlTableModel()
        tableModel.setTable("radios")
        tableModel.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        tableModel.select()
        headers = ("ID", "Name", "Fleet ID", "Device ID")
        for columnIndex, header in enumerate(headers):
            tableModel.setHeaderData(columnIndex, Qt.Orientation.Horizontal, header)
        return tableModel
