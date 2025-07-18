import sys
import os
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from PySide6.QtGui import QFontDatabase

if __name__ == "__main__":

    # پیدا کردن مسیر صحیح فایل style.qss
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    style_path = os.path.join(base_path, "resources", "styles", "style.qss")
    font_path = os.path.join(base_path, "resources", "fonts", "Vazirmatn-Regular.ttf")

    app = QApplication(sys.argv)

    # اعمال فونت
    QFontDatabase.addApplicationFont(font_path)

    # اعمال استایل
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
