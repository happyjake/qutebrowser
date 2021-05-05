from typing import cast

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

from qutebrowser.api import cmdutils
from qutebrowser.utils import objreg
from qutebrowser.utils import log


@cmdutils.register()
def window_pin() -> None:
    """pin window to stay always on top."""
    log.misc.info("window pin on top")
    win = objreg.last_visible_window()
    win.setWindowFlags(
        cast(
            Qt.WindowFlags,
            win.windowFlags() | Qt.WindowStaysOnTopHint,
        )
    )
    win.show()


@cmdutils.register()
def window_unpin() -> None:
    """unpin window."""
    log.misc.info("window unpin")
    win = objreg.last_visible_window()
    win.setWindowFlags(
        cast(
            Qt.WindowFlags,
            win.windowFlags() & ~Qt.WindowStaysOnTopHint,
        )
    )
    win.show()


@cmdutils.register()
def window_pip() -> None:
    """move window to PIP position."""
    log.misc.info("window move")
    win = objreg.last_visible_window()
    screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
    point = screenSize.bottomRight()
    point.setX(point.x() - 10)
    point.setY(point.y() - 10)

    geo = win.geometry()
    height = 256
    width = 382
    geo.setHeight(height)
    geo.setWidth(width)

    geo.moveBottomRight(point)

    win.setGeometry(geo)
