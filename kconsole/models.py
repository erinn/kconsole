# -*- coding: utf-8 -*-
# rpcontacts/model.py

"""This module provides a model to manage the radios table."""
import logging

from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlTableModel

logger = logging.getLogger(__name__)


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

        column_titles = {
            "name": "Name",
            "fleet_id": "Fleet ID",
            "device_id": "Device ID",
            "last_contact": "Last Contact",
            "last_coordinates": "Last Coordinates",
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
        logger.debug("Adding a device to the DB with data: %s.", data)

        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            # First column is the primary key automatically created.
            self.model.setData(self.model.index(rows, column + 1), field)

        if self.model.submitAll():
            self.model.select()
            logger.debug("Data successfully added to DB.")
            return True
        else:
            logger.info(
                "Unable to add device to DB, error: %s", self.model.lastError().text()
            )
            logger.info("Query executed: %s", self.model.query().executedQuery())
            return False

    def delete_radio(self, row: int) -> bool:
        """
        Delete an entry from the radio table.

        :param row: The row to be removed.
        :return: None
        """
        logger.debug("Removing device at row: %s from DB.")
        self.model.removeRow(row)
        if self.model.submitAll():
            self.model.select()
            logger.debug("Device successfully removed from DB.")
            return True
        else:
            logger.info(
                "Device deletion from DB created an error: %s",
                self.model.lastError().text(),
            )

            return False
