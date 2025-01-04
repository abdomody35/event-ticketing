from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from ...models.event import Event
from ...models.user import User
from ...models.sale import Sale


class CreatePurchaseDialog(QDialog):
    def __init__(self, event_data, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.event_data = event_data
        self.setWindowTitle("Book Tickets")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.event_name_label = QLabel(f"<b>{self.event_data['name']}</b>")
        self.event_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.date_label = QLabel(f"Date: {self.event_data['date']}")
        self.tickets_available_label = QLabel(
            f"Available Tickets: {self.event_data['number_of_tickets']  - self.event_data["number_of_bookings"]}"
        )
        self.price_label = QLabel(f"Price per Ticket: ${self.event_data['price']:.2f}")

        self.quantity_label = QLabel("Select Quantity:")
        self.quantity_input = QLineEdit("1")

        self.purchase_button = QPushButton("Book")
        self.purchase_button.clicked.connect(self.make_purchase)

        layout.addWidget(self.event_name_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.tickets_available_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.purchase_button)

        self.setLayout(layout)

    def make_purchase(self):
        try:
            quantity = int(self.quantity_input.text())
            if quantity < 1:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid quantity")
            return

        total_price = quantity * self.event_data["price"]

        if quantity > self.event_data["number_of_tickets"]- self.event_data["number_of_bookings"]:
            QMessageBox.warning(self, "Error", "Not enough tickets available.")
            return

        try:
            user_id = User.get_by_username(self.parent.parent.parent.logged_in_user)["id"]
        except Exception as e:
            QMessageBox.critical(
                self,
                "You are not logged in",
                "Please Login to be able to book tikcets",
            )
            self.close()
            return
        
        if user_id == self.event_data["seller_id"]:
            QMessageBox.warning(self, "Error", "You cannot book your own event.")
            self.close()
            return

        try:
            updated_tickets = self.event_data["number_of_bookings"] + quantity

            Sale.create(
                event_id=self.event_data["id"],
                buyer_id=user_id,
                quantity_sold=quantity,
                price_paid=total_price,
            )

            Event.update(self.event_data["id"], number_of_bookings=updated_tickets)

            QMessageBox.information(
                self,
                "Success",
                f"You have successfully booked {quantity} tickets for ${total_price:.2f}!",
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to complete booking: {str(e)}")
