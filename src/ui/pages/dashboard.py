from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt
from ...models.sale import Sale
from ...models.event import Event
from ...models.user import User
from ..dialogs.create_event import CreateEventDialog
from ..components.event import EventWidget
from ..components.scroll import ScrollWidget


class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Sets up the dashboard UI"""
        layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Welcome, {self.parent().logged_in_user}!")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 20px; margin: 10px;")

        self.tabs = QTabWidget()

        self.events_tab = QWidget()
        self.events_layout = QVBoxLayout()
        self.create_event_button = QPushButton("Create New Event")
        self.create_event_button.clicked.connect(self.show_create_event_dialog)
        self.events_layout.addWidget(self.create_event_button)
        self.events_tab.setLayout(self.events_layout)

        self.purchases_tab = QWidget()
        self.purchases_layout = QVBoxLayout()
        self.browse_events_button = QPushButton("Browse Events")
        self.browse_events_button.clicked.connect(
            lambda ev,: self.parent().setup_central_widget()
        )
        self.purchases_layout.addWidget(self.browse_events_button)
        self.purchases_tab.setLayout(self.purchases_layout)

        self.tabs.addTab(self.events_tab, "My Events")
        self.tabs.addTab(self.purchases_tab, "My Bookings")

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.load_user_purchases()
        self.load_user_events()

    def show_create_event_dialog(self):
        """Shows dialog for creating a new event"""
        dialog = CreateEventDialog(self)
        if dialog.exec():
            self.load_user_events()

    def load_user_events(self):
        """Loads and displays user's created events"""
        for i in reversed(range(self.events_layout.count())):
            widget = self.events_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                continue
            widget.setParent(None)

        user_id = User.get_by_username(self.parent().logged_in_user)["id"]
        events = Event.get_user_events(user_id)

        events_layout = QVBoxLayout()
        events_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if not events:
            no_events_label = QLabel("You didn't create any event")
            no_events_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            events_layout.addWidget(no_events_label)
        else:
            for event in events:
                event_widget = EventWidget(event, mode="edit", parent=self)
                events_layout.addWidget(event_widget)

        events_scroll_Widget = ScrollWidget(events_layout, self)
        self.events_layout.addWidget(events_scroll_Widget)

    def load_user_purchases(self):
        """Loads and displays user's purchases"""
        user_id = User.get_by_username(self.parent().logged_in_user)["id"]
        purchases = Sale.get_user_purchases(user_id)

        purchases_layout = QVBoxLayout()
        purchases_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if not purchases:
            no_purchases_label = QLabel("You didn't buy any ticket")
            no_purchases_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            purchases_layout.addWidget(no_purchases_label)
        else:
            for purchase in purchases:
                purchase_widget = EventWidget(purchase, type="purchase", parent=self)
                purchases_layout.addWidget(purchase_widget)

        purchases_scroll_widget = ScrollWidget(purchases_layout, self)
        self.purchases_layout.addWidget(purchases_scroll_widget)
