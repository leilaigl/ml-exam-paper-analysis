# havent figured out how to split for each question yet

from pdf2image import convert_from_path
from PIL import Image
import os


def convert_pdf_and_crop(pdf_path, save_dir, res=400, crop_box=None):
    pages = convert_from_path(pdf_path, res)

    name_with_extension = os.path.basename(pdf_path)
    name = os.path.splitext(name_with_extension)[0]

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for idx, page in enumerate(pages):
        page_path = os.path.join(save_dir, f"{name}_{idx}.png")
        page.save(page_path, "PNG")

        if crop_box:
            img = Image.open(page_path)
            cropped_img = img.crop(crop_box)
            cropped_img_path = os.path.join(save_dir, f"{name}_{idx}_cropped.png")
            cropped_img.save(cropped_img_path, "PNG")
            cropped_img.close()


pdf_path = "/Users/chae/Desktop/Finalproj/Geoga.pdf"
save_dir = "/Users/chae/Desktop/Finalproj/image/"
crop_box = (250, 350, 3450, 4200)


convert_pdf_and_crop(pdf_path, save_dir, crop_box=crop_box)
