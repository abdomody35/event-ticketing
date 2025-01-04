from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QDialog,
    QPushButton,
)
from PyQt6.QtCore import Qt, QDate, QTime
from ...models.event import Event
from ...models.category import Category
from ...models.venue import Venue
from ..components.event import EventWidget
from ..components.scroll import ScrollWidget
from ..dialogs.filter import FilterDialog


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_filters = {}
        self.setup_ui()

    def setup_ui(self):
        """Sets up the main page UI"""
        layout = QVBoxLayout()

        self.welcome_label = QLabel("Welcome to Ticket Marketplace")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; margin: 25px;")
        layout.addWidget(self.welcome_label)

        filter_buttons_container = QWidget()
        filter_buttons_layout = QHBoxLayout()
        filter_buttons_layout.setSpacing(10)
        
        self.filter_button = QPushButton("Filter Events")
        self.filter_button.setMinimumWidth(120)
        self.filter_button.clicked.connect(self.show_filter_dialog)
        
        self.remove_filters_button = QPushButton("Remove Filters")
        self.remove_filters_button.setMinimumWidth(120)
        self.remove_filters_button.clicked.connect(self.remove_filters)
        self.remove_filters_button.setVisible(False)
        
        filter_buttons_layout.addWidget(self.filter_button)
        filter_buttons_layout.addWidget(self.remove_filters_button)
        filter_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filter_buttons_container.setLayout(filter_buttons_layout)
        layout.addWidget(filter_buttons_container)

        self.active_filters_label = QLabel()
        self.active_filters_label.setWordWrap(True)
        self.active_filters_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.active_filters_label.setStyleSheet("color: #666666; margin: 10px 0;")
        layout.addWidget(self.active_filters_label)

        self.events_container = QWidget()
        self.events_layout = QVBoxLayout()
        self.events_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.events_container.setLayout(self.events_layout)
        layout.addWidget(self.events_container)

        self.setLayout(layout)
        self.update_active_filters_label()
        self.load_events()

    def remove_filters(self):
        """Removes all active filters"""
        self.current_filters = {}
        self.remove_filters_button.setVisible(False)
        self.update_active_filters_label()
        self.load_events()

    def update_active_filters_label(self):
        """Updates the label showing active filters"""
        if not self.current_filters:
            self.active_filters_label.setText("")
            self.remove_filters_button.setVisible(False)
            return

        active_filters = []
        if self.current_filters.get("category_id"):
            category = Category.get(self.current_filters.get("category_id"))["name"]
            if category:
                active_filters.append(f"Category: {category}")

        if self.current_filters.get("venue_id"):
            venue = Venue.get(self.current_filters.get("venue_id"))["name"]
            if venue:
                active_filters.append(f"Venue: {venue}")

        if self.current_filters.get("start_date"):
            date_range = f"Date: {self.current_filters['start_date'].toString('dd/MM/yyyy')}"
            if self.current_filters.get("end_date"):
                date_range += f" - {self.current_filters['end_date'].toString('dd/MM/yyyy')}"
            active_filters.append(date_range)

        if self.current_filters.get("start_time"):
            time_range = ""
            if not self.current_filters.get("start_time").toString('HH:mm') == "00:00":
                time_range = f"Time: {self.current_filters['start_time'].toString('HH:mm')}"
            if self.current_filters.get("end_time"):
                if time_range:
                    time_range += f" - {self.current_filters['end_time'].toString('HH:mm')}"
                elif not self.current_filters.get("end_time").toString('HH:mm') == "23:59":
                    time_range = f"Time: 00:00 - {self.current_filters['end_time'].toString('HH:mm')}"
            active_filters.append(time_range) if time_range else ()

        if self.current_filters.get("min_price") is not None or self.current_filters.get("max_price") is not None:
            price_range = "Price: "
            if self.current_filters.get("min_price") is not None:
                price_range += f"${self.current_filters['min_price']}"
            price_range += " - "
            if self.current_filters.get("max_price") is not None:
                price_range += f"${self.current_filters['max_price']}"
            active_filters.append(price_range)

        self.active_filters_label.setText("Active Filters: " + " | ".join(active_filters))
        self.remove_filters_button.setVisible(True)

    def show_filter_dialog(self):
        """Shows the filter dialog and updates events if filters change"""
        dialog = FilterDialog(self)

        if self.current_filters:
            dialog.category_combobox.setCurrentIndex(
                dialog.category_combobox.findData(
                    self.current_filters.get("category_id")
                )
            )
            dialog.venue_combobox.setCurrentIndex(
                dialog.venue_combobox.findData(self.current_filters.get("venue_id"))
            )
            if self.current_filters.get("start_date"):
                dialog.start_date.setDate(self.current_filters["start_date"])
            if self.current_filters.get("end_date"):
                dialog.end_date.setDate(self.current_filters["end_date"])
            if self.current_filters.get("start_time"):
                dialog.start_time.setTime(self.current_filters["start_time"])
            if self.current_filters.get("end_time"):
                dialog.end_time.setTime(self.current_filters["end_time"])
            if self.current_filters.get("min_price") is not None:
                dialog.min_price.setText(str(self.current_filters["min_price"]))
            if self.current_filters.get("max_price") is not None:
                dialog.max_price.setText(str(self.current_filters["max_price"]))

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_filters = dialog.get_filters()
            self.update_active_filters_label()
            self.load_events()

    def load_events(self):
        """Loads and displays filtered upcoming events with purchase option in a 3-column grid"""
        for i in reversed(range(self.events_layout.count())):
            self.events_layout.itemAt(i).widget().setParent(None)

        events = Event.get_upcoming_events()
        filtered_events = []

        for event in events:
            if (
                self.current_filters.get("category_id")
                and event["category_id"] != self.current_filters["category_id"]
            ):
                continue

            if (
                self.current_filters.get("venue_id")
                and event["venue_id"] != self.current_filters["venue_id"]
            ):
                continue

            event_date = QDate.fromString(str(event["date"]), "yyyy-MM-dd")
            if (
                self.current_filters.get("start_date")
                and event_date < self.current_filters["start_date"]
            ):
                continue
            if (
                self.current_filters.get("end_date")
                and event_date > self.current_filters["end_date"]
            ):
                continue

            event_time = QTime.fromString(str(event["start_time"]), "HH:mm:ss")
            if (
                self.current_filters.get("start_time")
                and event_time < self.current_filters["start_time"]
            ):
                continue
            if (
                self.current_filters.get("end_time")
                and event_time > self.current_filters["end_time"]
            ):
                continue

            if (
                self.current_filters.get("min_price") is not None
                and event["price"] < self.current_filters["min_price"]
            ):
                continue
            if (
                self.current_filters.get("max_price") is not None
                and event["price"] > self.current_filters["max_price"]
            ):
                continue

            filtered_events.append(event)

        if not filtered_events:
            self.events_layout.addWidget(
                QLabel("No events found"), alignment=Qt.AlignmentFlag.AlignCenter
            )
            return

        grid_layout = QGridLayout()
        grid_layout.setSpacing(24)
        grid_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        widget_count = self.parent.width() / 650
        if widget_count > 2.92:
            widget_count = 3
        else:
            widget_count = int(widget_count)
        self.num_columns = max(1, widget_count)

        for index, event in enumerate(filtered_events):
            row = index // self.num_columns
            col = index % self.num_columns
            event_widget = EventWidget(event, mode="view", parent=self)
            grid_layout.addWidget(event_widget, row, col)

        events_scroll_widget = ScrollWidget(grid_layout, self)
        self.events_layout.addWidget(events_scroll_widget)
