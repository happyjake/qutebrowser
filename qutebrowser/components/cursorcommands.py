import time

from PyQt5.QtCore import QEvent, QObject, QTimer, Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication

from qutebrowser.api import apitypes, cmdutils, hook
from qutebrowser.misc import objects
from qutebrowser.utils import log

IDLE_HIDE_IN_SECOND = 5
IDLE_CHECK_INTERVAL_IN_MS = 1000


class CursorHide(QObject):
    hidden = False
    lastMoved = 0.0

    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_when_idle)
        self.timer.start(IDLE_CHECK_INTERVAL_IN_MS)

    @pyqtSlot()
    def hide_when_idle(self) -> None:
        if self.hidden:
            return
        now = time.time()
        if now - self.lastMoved > IDLE_HIDE_IN_SECOND:
            self.hide_cursor()

    def hide_cursor(self) -> None:
        log.mouse.info("hide cursor")
        QApplication.setOverrideCursor(Qt.BlankCursor)
        self.hidden = True

    def show_cursor(self) -> None:
        log.mouse.info("show cursor")
        QApplication.restoreOverrideCursor()
        self.hidden = False

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonPress:
            self.lastMoved = time.time()
            if self.hidden:
                self.show_cursor()
        return False


cursor_hide = CursorHide()


@cmdutils.register()
def hide_cursor() -> None:
    cursor_hide.hide_cursor()


@cmdutils.register()
def show_cursor() -> None:
    cursor_hide.show_cursor()


@hook.init()
def init(context: apitypes.InitContext) -> None:
    """hide cursor when scroll. show it when move mouse."""
    objects.qapp.installEventFilter(cursor_hide)
