from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QFrame,
)
from ...models.venue import Venue
from ...models.event import Event
from ...models.sale import Sale
from ..dialogs.edit_event import EditEventDialog
from ..dialogs.create_sale import CreatePurchaseDialog
from ..styles.card import CARD
from ..styles.button import BUTTON_PRIMARY, BUTTON_DANGER


class EventWidget(QWidget):
    def __init__(self, data, mode="view", type="event", parent=None):
        super().__init__(parent)
        self.data = data
        self.parent = parent
        self.mode = mode
        self.type = type
        self.event = self.get_event_data()
        self.setup_ui()

    def get_event_data(self):
        """Returns event data based on widget type"""
        if self.type == "event":
            return self.data
        else:
            return Event.get(self.data["event_id"])

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.setStyleSheet("font: 20px")

        card = QFrame()
        card.setStyleSheet(CARD)
        card.setObjectName("MainCard")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()

        name_label = QLabel(self.event["name"])
        name_label.setStyleSheet("font-weight: bold")
        title_layout.addWidget(name_label)

        if self.type == "event":
            available_tickets = (
                self.event["number_of_tickets"] - self.event["number_of_bookings"]
            )
            status_text = ""

            if self.mode == 'edit':
                if available_tickets > 0:
                    status_text = f"{available_tickets} Available out of {self.event['number_of_tickets']}"
                else:
                    status_text = f"{self.event['number_of_tickets']} Sold Out"
            elif available_tickets > 0:
                status_text = "Available"
            else:
                status_text = "Sold Out"

            status_label = QLabel(status_text)

            status_label.setStyleSheet(
                f"color: {'green' if available_tickets > 0 else 'red'}; font-weight: bold;"
            )
            title_layout.addWidget(status_label)

        header_layout.addLayout(title_layout)

        if self.mode == "edit" and self.type == "event":
            button_layout = QHBoxLayout()
            edit_button = QPushButton("📝 Edit")
            edit_button.setStyleSheet(BUTTON_PRIMARY)
            edit_button.clicked.connect(self.edit_event)

            delete_button = QPushButton("🗑️ Delete")
            delete_button.setStyleSheet(BUTTON_DANGER)
            delete_button.clicked.connect(self.delete_event)

            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            header_layout.addLayout(button_layout)
        elif self.type == "purchase":
            cancel_button = QPushButton("Cancel Booking")
            cancel_button.setStyleSheet(BUTTON_DANGER)
            cancel_button.clicked.connect(self.cancel_purchase)
            header_layout.addWidget(cancel_button)

        card_layout.addLayout(header_layout)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        card_layout.addWidget(line)

        details_layout = QHBoxLayout()

        left_col = QVBoxLayout()
        date_label = QLabel(f"📅 {self.event['date'].strftime("%d/%m/%Y")}")
        time_label = QLabel(f"🕒 {self.event['start_time']}")
        left_col.addWidget(date_label)
        left_col.addWidget(time_label)

        middle_col = QVBoxLayout()
        if (
            self.type == "purchase"
            or self.mode == "edit"
            or (
                self.type == "event"
                and self.event["number_of_tickets"] - self.event["number_of_bookings"]
                > 0
            )
        ):
            venue = Venue.get(self.event["venue_id"])
            venue_label = QLabel(f"📍 {venue['name']}")
            venue_address = QLabel(f"   {venue['address']}")
            venue_address.setStyleSheet("color: #666;")
            middle_col.addWidget(venue_label)
            middle_col.addWidget(venue_address)

        right_col = QVBoxLayout()
        if self.type == "purchase":
            quantity_label = QLabel(
                f"🎟️ {self.data['quantity_sold']} {'ticket' if self.data['quantity_sold'] == 1 else 'tickets'}"
            )
            quantity_label.setStyleSheet("font-weight: bold")
            price_label = QLabel(f"💰 Total: ${self.data['price_paid']:.2f}")
            price_label.setStyleSheet("font-weight: bold")
            right_col.addWidget(quantity_label)
            right_col.addWidget(price_label)
        else:
            price_label = QLabel(f"💰 ${self.event['price']:.2f}")
            price_label.setStyleSheet("font-weight: bold")
            right_col.addWidget(price_label)

            if self.mode == "view":
                available_tickets = (
                    self.event["number_of_tickets"] - self.event["number_of_bookings"]
                )
                if available_tickets > 0:
                    tickets_label = QLabel(f"🎟️ {available_tickets} tickets left")
                    right_col.addWidget(tickets_label)

                    book_button = QPushButton("Book Now")
                    book_button.setStyleSheet(BUTTON_PRIMARY)
                    book_button.clicked.connect(
                        lambda: self.show_purchase_dialog(self.event)
                    )
                    right_col.addWidget(book_button)

        details_layout.addLayout(left_col)
        details_layout.addLayout(middle_col)
        details_layout.addLayout(right_col)
        card_layout.addLayout(details_layout)
        main_layout.addWidget(card)
        main_layout.addStretch()

    def show_purchase_dialog(self, event):
        """Shows the purchase dialog for the selected event"""
        dialog = CreatePurchaseDialog(event, self)
        if dialog.exec():
            self.parent.load_events()

    def edit_event(self):
        dialog = EditEventDialog(self.event, self)
        if dialog.exec():
            self.parent.load_user_events()

    def delete_event(self):
        confirm = QMessageBox.question(
            self, "Confirm Deletion", "Are you sure you want to delete this event?"
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                Event.delete(self.event["id"])
                QMessageBox.information(self, "Success", "Event deleted successfully")
                self.parent.parent().show_dashboard()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting event {str(e)}")

    def cancel_purchase(self):
        updated_tickets = self.event["number_of_bookings"] - self.data["quantity_sold"]
        confirm = QMessageBox.question(
            self,
            "Confirm Cancelation",
            "Are you sure you want to cancel this booking?",
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                Sale.delete(self.data["id"])
                Event.update(self.event["id"], number_of_bookings=updated_tickets)
                QMessageBox.information(
                    self, "Success", "Booking canceled successfully"
                )
                self.parent.parent().show_dashboard()
                self.parent.parent().dashboard.tabs.setCurrentIndex(1)
            except Exception as e:
                QMessageBox.warning(
                    self, "Error", f"Failed to cancel booking: {str(e)}"
                )
