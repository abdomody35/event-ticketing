from datetime import timedelta, datetime
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import QDate, QTime
from ...models.event import Event
from ...models.venue import Venue
from ...models.user import User
from ...models.category import Category


class CreateEventDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Event")
        self.setup_ui()
        self.setStyleSheet("font: 20px")

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Event Name:")
        self.name_input = QLineEdit()

        self.date_label = QLabel("Event Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setCalendarPopup(True)

        self.time_label = QLabel("Event Start Time:")
        self.time_input = QTimeEdit()
        self.time_input.setTime(QTime(0, 0))
        self.time_input.setDisplayFormat("HH:mm")

        self.tickets_label = QLabel("Number of Tickets:")
        self.tickets_input = QLineEdit()

        self.price_label = QLabel("Price per Ticket:")
        self.price_input = QLineEdit()

        self.venue_label = QLabel("Venue:")
        self.venue_combo = QComboBox()
        venues = Venue.get_all()
        for venue in venues:
            self.venue_combo.addItem(
                f"{venue['name']} - {venue['address']} - ({venue["seats"]} seat)",
                venue["id"],
            )

        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        categories = Category.get_all()
        for category in categories:
            self.category_combo.addItem(category["name"], category["id"])

        self.create_button = QPushButton("Create Event")
        self.create_button.clicked.connect(self.create_event)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_input)
        layout.addWidget(self.time_label)
        layout.addWidget(self.time_input)
        layout.addWidget(self.tickets_label)
        layout.addWidget(self.tickets_input)
        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)
        layout.addWidget(self.venue_label)
        layout.addWidget(self.venue_combo)
        layout.addWidget(self.category_label)
        layout.addWidget(self.category_combo)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def create_event(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Please enter an event name")
            return

        try:
            tickets = int(self.tickets_input.text())
            price = float(self.price_input.text())
            if tickets < 1 or price < 1:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid number of tickets or price")
            return

        venue_id = self.venue_combo.currentData()
        venue = Venue.get(venue_id)
        if tickets > venue["seats"]:
            QMessageBox.warning(self, "Error", "Not enough seats in the venue")
            return

        date = self.date_input.date().toString("yyyy-MM-dd")
        time = self.time_input.time().toString("HH:mm:ss")
        date_time = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S")
        if date_time < datetime.now() + timedelta(hours=2):
            QMessageBox.warning(
                self,
                "Error",
                "Date and time must be at least 2 hours from the current date and time",
            )
            return

        user_id = User.get_by_username(self.parent().parent().logged_in_user)["id"]

        event_data = {
            "name": self.name_input.text(),
            "date": date,
            "venue_id": venue_id,
            "category_id": self.category_combo.currentData(),
            "start_time": time,
            "seller_id": user_id,
            "number_of_tickets": tickets,
            "price": price,
        }

        try:
            Event.create(**event_data)
            QMessageBox.information(self, "Success", "Event created successfully")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create event: {str(e)}")
