# -*- coding: utf-8 -*-
# rpcontacts/model.py

"""This module provides a model to manage the radios table."""

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel


class RadiosModel:
    def __init__(self):
        self.model = self._create_model()

    @staticmethod
    def _create_model() -> QSqlTableModel:
        """
        Create and set up the model.
        """
        table_model = QSqlTableModel()
        table_model.setTable("radios")
        table_model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        table_model.select()

        # End users do not care about the primary key, hide it.
        table_model.removeColumns(0, 1)

        column_titles = {
            "name": "Name",
            "fleet_id": "Fleet ID",
            "device_id": "Device ID",
            "last_contact": "Last Contact",
            "last_coordinates": "Last Coordinates"
        }

        for key, value in column_titles.items():
            index = table_model.fieldIndex(key)
            table_model.setHeaderData(index, Qt.Orientation.Horizontal, value)

        return table_model

    def add_radio(self, data: list) -> bool:
        """
        Add a new row (radio) to the DB.

        :param data:
        :return: True if successful, False if not.
        """

        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column), field)

        if self.model.submitAll():
            self.model.select()
            return True
        else:
            print(self.model.lastError().text())
            print(self.model.query().executedQuery())
            return False

    def delete_radio(self, row: int) -> None:
        """
        Delete an entry from the radio table.

        :param row: The row to be removed.
        :return: None
        """

        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
