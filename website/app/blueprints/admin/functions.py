import os
from datetime import datetime

from PIL import Image
from flask import current_app

from pathlib import Path


def delete_images(img_path: str | None):
    full_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images')
    thumb_folder = os.path.join(full_folder, 'thumbs')

    if img_path:
        if os.path.isfile(file := os.path.join(full_folder, img_path)):
            os.remove(file)
        if os.path.isfile(file := os.path.join(thumb_folder, img_path)):
            os.remove(file)


def replace_image(data, img_path: str | None, prefix: str) -> str:
    full_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images')
    thumb_folder = os.path.join(full_folder, 'thumbs')

    filename = ".".join([
        prefix,
        str(datetime.timestamp(datetime.now())),
        'png'
    ])

    os.makedirs(full_folder, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)

    def calculate_size(image, a: int) -> tuple:
        width, height = image.size
        kt = max(width / a, height / a)

        return int(width / kt), int(height / kt)

    # Resize uploaded image and make thumbnail
    print(data)
    with Image.open(data) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # img = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=256)

        full = img.resize(calculate_size(img, 800), Image.Resampling.LANCZOS)
        full.save(os.path.join(full_folder, filename), 'PNG', compress_level=5, quality=90)
        thumb = img.resize(calculate_size(img, 400), Image.Resampling.LANCZOS)
        thumb.save(os.path.join(thumb_folder, filename), 'PNG', compress_level=5, quality=90)

    # Delete old images
    delete_images(img_path)

    return filename