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

    def add_radio(self, data: list) -> None:
        """
        Add a new row (radio) to the DB.

        :param data:
        :return: None
        """

        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def delete_radio(self, row: int) -> None:
        """
        Delete an entry from the radio table.

        :param row: The row to be removed.
        :return: None
        """

        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
