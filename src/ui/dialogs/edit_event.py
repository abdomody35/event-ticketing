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
from ...models.category import Category


class EditEventDialog(QDialog):
    def __init__(self, event_data, parent=None):
        super().__init__(parent)
        self.event_data = event_data
        self.setWindowTitle("Edit Event")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Event Name:")
        self.name_input = QLineEdit(self.event_data["name"])

        self.date_label = QLabel("Event Date:")
        self.date_input = QDateEdit()
        self.date_input.setDate(
            QDate.fromString(str(self.event_data["date"]), "yyyy-MM-dd")
        )
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setCalendarPopup(True)

        self.time_label = QLabel("Event Start Time:")
        self.time_input = QTimeEdit()
        self.time_input.setTime(
            QTime.fromString(str(self.event_data["start_time"]), "HH:mm:ss")
        )
        self.time_input.setDisplayFormat("HH:mm:ss")

        self.tickets_label = QLabel("Number of Tickets:")
        self.tickets_input = QLineEdit(str(self.event_data["number_of_tickets"]))

        self.price_label = QLabel("Price per Ticket:")
        self.price_input = QLineEdit(f"{self.event_data['price']:.2f}")

        self.venue_label = QLabel("Venue:")
        self.venue_combo = QComboBox()
        venues = Venue.get_all()
        current_venue_index = 0
        for i, venue in enumerate(venues):
            self.venue_combo.addItem(
                f"{venue['name']} - {venue['address']} - ({venue["seats"]} seat)",
                venue["id"],
            )
            if venue["id"] == self.event_data["venue_id"]:
                current_venue_index = i
        self.venue_combo.setCurrentIndex(current_venue_index)

        self.category_label = QLabel("Category:")
        self.category_combo = QComboBox()
        categories = Category.get_all()
        for category in categories:
            self.category_combo.addItem(category["name"], category["id"])
        self.category_combo.setCurrentIndex(
            self.category_combo.findData(self.event_data["category_id"])
        )

        self.update_button = QPushButton("Update Event")
        self.update_button.clicked.connect(self.update_event)

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
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def update_event(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Error", "Please enter an event name")
            return

        try:
            tickets = int(self.tickets_input.text())
            price = float(self.price_input.text())
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

        already_booked = self.event_data["number_of_bookings"]
        if tickets < already_booked:
            QMessageBox.warning(
                self,
                "Error",
                f"{already_booked} seats are already reserverd",
            )
            return

        event_data = {
            "name": self.name_input.text(),
            "date": self.date_input.date().toString("yyyy-MM-dd"),
            "venue_id": self.venue_combo.currentData(),
            "category_id": self.category_combo.currentData(),
            "start_time": self.time_input.time().toString("HH:mm:ss"),
            "number_of_tickets": tickets,
            "price": price,
        }

        try:
            Event.update(self.event_data["id"], **event_data)
            QMessageBox.information(self, "Success", "Event updated successfully")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update event: {str(e)}")
