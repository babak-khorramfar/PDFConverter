import os
from pdf2image import convert_from_path


def convert_pdf_to_images(pdf_path, output_folder, dpi=200):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        poppler_path = os.path.abspath("tools/poppler/Library/bin")
        images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)

        if not images:
            print("❌ هیچ تصویری تولید نشد.")
            return []

        saved_files = []
        for i, image in enumerate(images):
            output_path = os.path.join(
                output_folder,
                f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page_{i + 1}.png",
            )
            image.save(output_path, "PNG")
            saved_files.append(output_path)

        return saved_files

    except Exception as e:
        print("❌ خطا در تبدیل PDF:", e)
        return []
