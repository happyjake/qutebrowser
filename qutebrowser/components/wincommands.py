from typing import cast

from PyQt5.QtCore import Qt

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
