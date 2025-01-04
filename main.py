from PyQt6.QtWidgets import QApplication
from src.database.connection import db
from src.ui.main_window import MainWindow


def main():
    """Main application entry point"""
    try:
        db.connect()

        app = QApplication([])

        window = MainWindow()
        window.show()

        app.exec()

    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
