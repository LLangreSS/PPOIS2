import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from core.views.main_window import MainWindow
from core.models.repostitory import PatientRepository


def main():
    app = QApplication(sys.argv)

    app.setStyle("Breeze")

    repo = PatientRepository()

    window = MainWindow(repo)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
