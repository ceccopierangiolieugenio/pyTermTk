
#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2026 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Requires: PySide6 (or adapt imports to PyQt5)
import sys
from PySide6.QtCore import Qt, QModelIndex, QPoint
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication, QTreeView, QWidget, QToolButton,
    QHBoxLayout, QStyle, QVBoxLayout
)

class HoverActionBar(QWidget):
    """A small right-aligned bar with action buttons that floats over the view."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.setObjectName("HoverActionBar")

        # Layout & buttons
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(6)

        self.runBtn = QToolButton(self)
        self.runBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.runBtn.setToolTip("Run test")
        self.runBtn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.debugBtn = QToolButton(self)
        self.debugBtn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_CommandLink))
        self.debugBtn.setToolTip("Debug test")
        self.debugBtn.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(self.runBtn)
        layout.addWidget(self.debugBtn)

        # Optional: light styling
        self.setStyleSheet("""
            #HoverActionBar {
                background: rgba(240, 240, 240, 0.95);
                border: 1px solid rgba(0,0,0,0.08);
                border-radius: 6px;
            }
            QToolButton { border: none; padding: 2px; }
            QToolButton::hover { background: rgba(0,0,0,0.06); border-radius: 4px; }
        """)

        self._index = QModelIndex()

    def setIndex(self, index: QModelIndex):
        self._index = index

    def index(self):
        return self._index


class HoverTree(QTreeView):
    """QTreeView that shows an action bar aligned to the right side of the hovered row."""
    def __init__(self, parent=None):
        self._bar = None
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self._hovered = QModelIndex()

        self._bar = HoverActionBar(self.viewport())
        self._bar.hide()

        # Wire buttons to actions
        self._bar.runBtn.clicked.connect(self._onRunClicked)
        self._bar.debugBtn.clicked.connect(self._onDebugClicked)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._hovered = QModelIndex()
        self._bar.hide()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos = event.position().toPoint() if hasattr(event, 'position') else event.pos()
        idx = self.indexAt(pos)
        if idx != self._hovered:
            self._hovered = idx
            self._updateBarGeometry()

    def viewportEvent(self, event):
        """Keep bar positioned if the view scrolls or resizes."""
        res = super().viewportEvent(event)
        # Reposition on paint/scroll/resize
        if self._bar and self._bar.isVisible() and self._hovered.isValid():
            self._updateBarGeometry()
        return res

    def _updateBarGeometry(self):
        if not self._hovered.isValid():
            self._bar.hide()
            return

        rect = self.visualRect(self._hovered)
        if not rect.isValid() or not self.viewport().rect().intersects(rect):
            self._bar.hide()
            return

        # Size the bar to content
        self._bar.adjustSize()
        bar_w = self._bar.width()
        bar_h = self._bar.height()

        # Right-align inside the row rect, with a small right margin
        right_margin = 6
        x = rect.right() - bar_w - right_margin
        y = rect.top() + (rect.height() - bar_h) // 2

        # Ensure it doesn’t overlap the text too aggressively (optional)
        min_left = rect.left() + 120  # tweak depending on your content/indentation
        x = max(x, min_left)

        self._bar.setIndex(self._hovered)
        self._bar.move(QPoint(x, y))
        self._bar.show()

    # Example slots that use the current index
    def _onRunClicked(self):
        idx = self._bar.index()
        if idx.isValid():
            print(f"Run: {idx.data()}")

    def _onDebugClicked(self):
        idx = self._bar.index()
        if idx.isValid():
            print(f"Debug: {idx.data()}")


def build_model():
    model = QStandardItemModel()
    root = model.invisibleRootItem()

    for suite in range(3):
        suite_item = QStandardItem(f"Suite {suite+1}")
        suite_item.setEditable(False)
        for case in range(4):
            case_item = QStandardItem(f"Test {suite+1}.{case+1}")
            case_item.setEditable(False)
            suite_item.appendRow(case_item)
        root.appendRow(suite_item)

    return model


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = HoverTree()
    view.setModel(build_model())
    view.expandAll()
    view.resize(420, 300)
    view.show()
    sys.exit(app.exec())
