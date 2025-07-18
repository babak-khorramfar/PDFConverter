from PIL import Image


def convert_images_to_pdf(image_paths, output_path):
    try:
        if not image_paths:
            return False

        # باز کردن اولین عکس
        first_image = Image.open(image_paths[0]).convert("RGB")

        # تبدیل بقیه تصاویر
        rest_images = []
        for path in image_paths[1:]:
            img = Image.open(path).convert("RGB")
            rest_images.append(img)

        # ذخیره به صورت PDF
        first_image.save(output_path, save_all=True, append_images=rest_images)
        return True
    except Exception as e:
        print("❌ خطا در تبدیل تصویر به PDF:", e)
        return False
