from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QDateEdit,
    QTimeEdit,
    QLineEdit,
    QFormLayout,
    QDialogButtonBox,
)
from PyQt6.QtCore import QDate, QTime, Qt
from ...models.category import Category
from ...models.venue import Venue


class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Filter Events")
        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Filter Events")
        title.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.category_combobox = QComboBox()
        self.category_combobox.setMinimumWidth(200)
        self.category_combobox.addItem("All Categories", None)
        categories = Category.get_all()
        for category in categories:
            self.category_combobox.addItem(category["name"], category["id"])
        form_layout.addRow("Category:", self.category_combobox)

        self.venue_combobox = QComboBox()
        self.venue_combobox.setMinimumWidth(200)
        self.venue_combobox.addItem("All Venues", None)
        venues = Venue.get_all()
        for venue in venues:
            self.venue_combobox.addItem(venue["name"], venue["id"])
        form_layout.addRow("Venue:", self.venue_combobox)

        date_range_widget = QWidget()
        date_range_layout = QHBoxLayout()
        date_range_layout.setSpacing(10)
        date_range_layout.setContentsMargins(0, 0, 0, 0)

        self.start_date = QDateEdit(QDate.currentDate())
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.start_date.setCalendarPopup(True)
        self.start_date.setMinimumDate(QDate.currentDate())

        self.end_date = QDateEdit(QDate.currentDate().addMonths(3))
        self.end_date.setDisplayFormat("dd/MM/yyyy")
        self.end_date.setCalendarPopup(True)
        self.end_date.setMinimumDate(QDate.currentDate())

        date_range_layout.addWidget(self.start_date)
        date_range_layout.addWidget(QLabel("to"))
        date_range_layout.addWidget(self.end_date)
        date_range_widget.setLayout(date_range_layout)
        form_layout.addRow("Date Range:", date_range_widget)

        time_range_widget = QWidget()
        time_range_layout = QHBoxLayout()
        time_range_layout.setSpacing(10)
        time_range_layout.setContentsMargins(0, 0, 0, 0)

        self.start_time = QTimeEdit(QTime(0, 0))
        self.start_time.setDisplayFormat("HH:mm")

        self.end_time = QTimeEdit(QTime(23, 59))
        self.end_time.setDisplayFormat("HH:mm")

        time_range_layout.addWidget(self.start_time)
        time_range_layout.addWidget(QLabel("to"))
        time_range_layout.addWidget(self.end_time)
        time_range_widget.setLayout(time_range_layout)
        form_layout.addRow("Time Range:", time_range_widget)

        price_range_widget = QWidget()
        price_range_layout = QHBoxLayout()
        price_range_layout.setSpacing(10)
        price_range_layout.setContentsMargins(0, 0, 0, 0)

        self.min_price = QLineEdit()
        self.min_price.setPlaceholderText("Min")
        self.max_price = QLineEdit()
        self.max_price.setPlaceholderText("Max")

        price_range_layout.addWidget(self.min_price)
        price_range_layout.addWidget(QLabel("to"))
        price_range_layout.addWidget(self.max_price)
        price_range_widget.setLayout(price_range_layout)
        form_layout.addRow("Price Range ($):", price_range_widget)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox()
        button_box.addButton(QDialogButtonBox.StandardButton.Ok)
        button_box.addButton(QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addSpacing(15)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_filters(self):
        """Returns the current filter values"""
        return {
            "category_id": self.category_combobox.currentData(),
            "venue_id": self.venue_combobox.currentData(),
            "start_date": self.start_date.date(),
            "end_date": self.end_date.date(),
            "start_time": self.start_time.time(),
            "end_time": self.end_time.time(),
            "min_price": (
                float(self.min_price.text()) if self.min_price.text() else None
            ),
            "max_price": (
                float(self.max_price.text()) if self.max_price.text() else None
            ),
        }
