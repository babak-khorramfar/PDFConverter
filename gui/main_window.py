import os
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QPushButton,
    QFileDialog,
    QScrollArea,
    QHBoxLayout,
)
from core.pdf_to_image import convert_pdf_to_images
from core.image_to_pdf import convert_images_to_pdf
from config.settings_manager import load_settings, save_settings
from PySide6.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = load_settings()
        self.last_dir = self.settings.get("last_directory", "")

        self.setWindowTitle("PDF ↔ تصویر")
        self.setFixedSize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        tabs = QTabWidget()

        # تب تبدیل PDF به تصویر
        pdf_to_image_tab = QWidget()
        pdf_to_image_layout = QVBoxLayout()

        # دکمه انتخاب فایل PDF
        self.select_pdf_button = QPushButton("انتخاب فایل PDF")
        self.select_pdf_button.clicked.connect(self.select_pdf_file)
        pdf_to_image_layout.addWidget(self.select_pdf_button)

        # لیبل برای نمایش آدرس فایل
        self.pdf_file_label = QLabel("هیچ فایلی انتخاب نشده")
        pdf_to_image_layout.addWidget(self.pdf_file_label)

        pdf_to_image_tab.setLayout(pdf_to_image_layout)

        # تبدیل PDF به تصویر
        self.convert_button = QPushButton("تبدیل PDF به تصویر")
        self.convert_button.clicked.connect(self.convert_selected_pdfs)
        pdf_to_image_layout.addWidget(self.convert_button)

        self.convert_result_label = QLabel("")
        pdf_to_image_layout.addWidget(self.convert_result_label)

        self.image_preview_area = QScrollArea()
        self.image_preview_widget = QWidget()
        self.image_preview_layout = QHBoxLayout()
        self.image_preview_widget.setLayout(self.image_preview_layout)
        self.image_preview_area.setWidgetResizable(True)
        self.image_preview_area.setWidget(self.image_preview_widget)
        pdf_to_image_layout.addWidget(self.image_preview_area)

        # تب تبدیل تصویر به PDF
        image_to_pdf_tab = QWidget()
        image_to_pdf_layout = QVBoxLayout()

        # دکمه انتخاب فایل تصویر
        self.select_image_button = QPushButton("انتخاب فایل تصویر")
        self.select_image_button.clicked.connect(self.select_image_file)
        image_to_pdf_layout.addWidget(self.select_image_button)

        # لیبل برای نمایش آدرس فایل تصویر
        self.image_file_label = QLabel("هیچ تصویری انتخاب نشده")
        image_to_pdf_layout.addWidget(self.image_file_label)

        image_to_pdf_tab.setLayout(image_to_pdf_layout)

        self.convert_to_pdf_button = QPushButton("تبدیل تصاویر به PDF")
        self.convert_to_pdf_button.clicked.connect(self.convert_images_to_pdf)
        image_to_pdf_layout.addWidget(self.convert_to_pdf_button)

        self.image_convert_result_label = QLabel("")
        image_to_pdf_layout.addWidget(self.image_convert_result_label)

        tabs.addTab(pdf_to_image_tab, "PDF → تصویر")
        tabs.addTab(image_to_pdf_tab, "تصویر → PDF")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)

        self.last_dir = ""
        self.selected_pdf_files = []
        self.selected_image_files = []

    def select_pdf_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "انتخاب فایل PDF", self.last_dir, "PDF File (*.pdf)"
        )
        if files:
            self.selected_pdf_files = files
            self.last_dir = os.path.dirname(files[0])
            self.settings["last_directory"] = self.last_dir
            save_settings(self.settings)
            text = "\n".join(files)
            self.pdf_file_label.setText(f"فایلهای انتخابی: \n{text}")
        else:
            self.selected_pdf_files = []
            self.pdf_file_label.setText(f"هیچ فایلی انتخاب نشده.")

    def select_image_file(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "انتخاب فایل‌های تصویر",
            self.last_dir,
            "Image Files (*.jpg *.jpeg *.png)",
        )
        if files:
            self.selected_image_files = files
            self.last_dir = os.path.dirname(files[0])
            self.settings["last_directory"] = self.last_dir
            save_settings(self.settings)
            text = "\n".join(files)
            self.image_file_label.setText(f"فایل‌های انتخابی:\n{text}")
        else:
            self.selected_image_files = []
            self.image_file_label.setText("هیچ تصویری انتخاب نشده.")

    def convert_selected_pdfs(self):
        if not self.selected_pdf_files:
            self.convert_result_label.setText("❌ هیچ فایلی برای تبدیل انتخاب نشده.")
            return

        output_dir = QFileDialog.getExistingDirectory(
            self, "انتخاب پوشه مقصد", self.last_dir
        )

        if not output_dir:
            self.convert_result_label.setText("❌ پوشه مقصد انتخاب نشده.")
            return

        all_outputs = []
        for pdf_file in self.selected_pdf_files:
            result = convert_pdf_to_images(pdf_file, output_dir)
            all_outputs.extend(result)

        if all_outputs:
            self.convert_result_label.setText(f"✅ {len(all_outputs)} تصویر ذخیره شد.")
            self.show_image_previews(all_outputs)
        else:
            self.convert_result_label.setText("❌ خطا در تبدیل فایل‌ها.")

    def show_image_previews(self, image_paths):
        # پاک کردن تصاویر قبلی
        for i in reversed(range(self.image_preview_layout.count())):
            widget_to_remove = self.image_preview_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        # اضافه کردن تصاویر جدید
        for path in image_paths:
            pixmap = QPixmap(path).scaledToWidth(150)
            label = QLabel()
            label.setPixmap(pixmap)
            self.image_preview_layout.addWidget(label)

    def convert_images_to_pdf(self):
        if not self.selected_image_files:
            self.image_convert_result_label.setText("❌ هیچ تصویری انتخاب نشده.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self, "ذخیره فایل PDF", self.last_dir + "/output.pdf", "PDF Files (*.pdf)"
        )

        if not output_path:
            self.image_convert_result_label.setText("❌ مسیر خروجی انتخاب نشد.")
            return

        success = convert_images_to_pdf(self.selected_image_files, output_path)

        if success:
            self.image_convert_result_label.setText(f"✅ ذخیره شد: {output_path}")
        else:
            self.image_convert_result_label.setText("❌ خطا در تبدیل تصاویر.")
