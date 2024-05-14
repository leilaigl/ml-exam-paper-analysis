from pdf2image import convert_from_path
import fitz  # PyMuPDF
import re
from PIL import Image

pdf_path = '0460_m17_qp_22.pdf'

# images = convert_from_path(pdf_path)

pdf_document = fitz.open(pdf_path)

# for i, page in enumerate(pdf_document):
#     pix = page.get_pixmap()
#     pix.save(f"page_{i}.png")

# for page_num in range(len(pdf_document)):
#     page = pdf_document.load_page(page_num)
#     text = page.get_text("text")
    
#     lines = text.split('\n')
#     for line in lines:        
#         if line.startswith('('):
#             Question_Type = 'SUB'
#             Question_ID = re.search(r'^\((.*?)\)', line).group(0)
#         elif re.search(r'^\d(\d\s| )', line):
#             Question_Type = 'MAIN'
#             Question_ID = re.search(r'^\d(\d\s| )', line).group(0)
#             break
def crop_and_save_image(page_num, bbox, next_bbox=None, is_last=False):
    page = pdf_document.load_page(page_num)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Define the crop box horizontally between the questions
    if is_last:
        crop_box = (bbox[0], bbox[1], pix.width, bbox[3])
    else:
        crop_box = (bbox[0], bbox[1], next_bbox[0], bbox[3])
    
    cropped_image = img.crop(crop_box)
    cropped_image.save(f'page_{page_num}_question_{bbox[1]}.png', 'PNG')

# Iterate through each page and process questions
for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)
    text = page.get_text("text")
    blocks = page.get_text("blocks")  # Extract text blocks
    
    question_regions = []  # List to store question bounding boxes

    for block in blocks:
        bbox = block[:4]  # The bounding box of the text block
        line = block[4]   # The text itself

        if line.startswith('('):
            Question_Type = 'SUB'
            Question_ID = re.search(r'^\((.*?)\)', line).group(0)
            question_regions.append((page_num, bbox))
        elif re.search(r'^\d(\d\s| )', line):
            Question_Type = 'MAIN'
            Question_ID = re.search(r'^\d(\d\s| )', line).group(0)
            question_regions.append((page_num, bbox))
            break

    # Crop and save images based on the question regions
    for i in range(len(question_regions) - 1):
        _, bbox = question_regions[i]
        next_bbox = question_regions[i + 1][1]
        crop_and_save_image(page_num, bbox, next_bbox)
    
    # Handle the last question in the page
    if question_regions:
        _, bbox = question_regions[-1]
        crop_and_save_image(page_num, bbox, is_last=True)