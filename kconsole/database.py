"""Database connection operations."""
import pathlib

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtSql import QSqlDatabase, QSqlQuery


def create_connection(database_name: str):
    """
    Create and open a database connection.

    :param database_name: The name of the SQLLite file to open as a DB.
    :return: None
    """
    data_directory = pathlib.Path(
        QStandardPaths.standardLocations(
            QStandardPaths.StandardLocation.AppLocalDataLocation
        )[0]
    )

    db_path = data_directory / database_name
    _create_path_location(db_path)

    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(str(db_path))

    if not connection.open():
        QMessageBox.warning(
            None,
            "KConsole",
            f"Database Error: {connection.lastError().text()}",
        )
        return False

    _create_radios_table()
    return True


def _create_path_location(path: pathlib.Path) -> None:
    """
    Ensure the data directory actually exists to write the DB file into. If it
    already exists no action is taken.

    :param path: A pathlib.Path object representing the full path including the
    filename.

    :return: None
    """

    if path.parent.exists():
        return None
    else:
        path.parent.mkdir(parents=True)
        return None


def _create_radios_table() -> bool:
    """
    Create the radio table in the database.
    :param db: The QSqlDatabase object representing the connection.

    :return: True if successful, false if not.
    """
    create_table_query = QSqlQuery()
    query_result = create_table_query.exec(
        """
        CREATE TABLE IF NOT EXISTS radios (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            name VARCHAR(40) NOT NULL,
            fleet VARCHAR(3),
            device_id VARCHAR(4) NOT NULL
        )
        """
    )

    if query_result:
        return query_result
    else:
        print(create_table_query.lastError())
        return query_result
