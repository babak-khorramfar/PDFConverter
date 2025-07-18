import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase

if __name__ == "__main__":

    app = QApplication(sys.argv)

    QFontDatabase.addApplicationFont("resources/fonts/Vazirmatn-Regullar.ttf")

    # Load QSS
    with open("resources/styles/style.qss", "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
