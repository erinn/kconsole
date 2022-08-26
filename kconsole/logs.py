import logging
from functools import cached_property
from PySide6.QtCore import QObject, Signal


class Bridge(QObject):
    """
    This is a PySide specific workaround for this issue (PyQT appears to just work):
    https://bugreports.qt.io/browse/PYSIDE-167
    With a lot more details here:
    https://pointermath.wordpress.com/2013/05/29/python-pyside-logging-headache/
    And finally the sort of solution from here:
    https://stackoverflow.com/questions/66664542/conflicting-names-between-logging-emit-function-and-qt-emit-signal/66664679#66664679
    """
    sigLog = Signal(str)


class ConsoleWindowLogHandler(logging.Handler):
    """
    Override the logging handler to emit a signal so this can be used in
    a threaded app safely.
    """

    @cached_property
    def bridge(self) -> object:
        """
        A hack to work around multiple inheritance search issues.

        :return: Object
        """
        return Bridge()

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, logRecord):
        """
        Override the log handler emit method to instead emit a signal.

        :param logRecord:
        :return:
        """
        message = str(logRecord.getMessage())
        self.bridge.sigLog.emit(message)
