from PyQt6.QtWidgets import (
    QWidget,
    QScrollArea,
)
from PyQt6.QtCore import Qt


class ScrollWidget(QScrollArea):
    def __init__(self, layout, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        widget = QWidget()
        self.setWidget(widget)
        widget.setLayout(layout)
