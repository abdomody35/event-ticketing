from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt
from ...models.event import Event
from ..components.event import EventWidget
from ..components.scroll import ScrollWidget


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Sets up the main page UI"""
        layout = QVBoxLayout()

        self.welcome_label = QLabel("Welcome to Ticket Marketplace")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; margin: 25px;")

        self.events_container = QWidget()
        self.events_layout = QVBoxLayout()
        self.events_container.setLayout(self.events_layout)

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.events_container)

        self.setLayout(layout)
        self.load_events()

    def load_events(self):
        """Loads and displays upcoming events with purchase option in a 3-column grid"""
        for i in reversed(range(self.events_layout.count())):
            self.events_layout.itemAt(i).widget().setParent(None)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)
        grid_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        events = Event.get_upcoming_events()
        widget_count = self.parent.width() / 650
        if widget_count > 2.92:
            widget_count = 3
        else:
            widget_count = int(widget_count)
        self.num_columns = max(1, widget_count)

        for index, event in enumerate(events):
            row = index // self.num_columns
            col = index % self.num_columns
            event_widget = EventWidget(event, mode="view", parent=self)
            grid_layout.addWidget(event_widget, row, col)

        events_scroll_Widget = ScrollWidget(grid_layout, self)
        self.events_layout.addWidget(events_scroll_Widget)
