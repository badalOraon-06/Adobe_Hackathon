# import fitz  # PyMuPDF

# def extract_outline(pdf_path):
#     doc = fitz.open(pdf_path)
#     headings = []

#     for page_num, page in enumerate(doc):
#         blocks = page.get_text("dict")["blocks"]
#         for block in blocks:
#             if "lines" not in block:
#                 continue
#             for line in block["lines"]:
#                 for span in line["spans"]:
#                     text = span["text"].strip()
#                     font_size = span["size"]

#                     # Skip empty lines or small font
#                     if not text or font_size < 8:
#                         continue

#                     heading_level = classify_heading_level(font_size)

#                     headings.append({
#                         "text": text,
#                         "font_size": font_size,
#                         "level": heading_level,
#                         "page": page_num + 1
#                     })

#     # Create hierarchy
#     structured = []
#     for h in headings:
#         level = h['level']
#         node = {
#             "title": h['text'],
#             "page": h['page'],
#             "children": []
#         }
#         if level == 1:
#             structured.append(node)
#         elif level == 2 and structured:
#             structured[-1]["children"].append(node)
#         elif level == 3 and structured and structured[-1]["children"]:
#             structured[-1]["children"][-1]["children"].append(node)

#     return structured


# def classify_heading_level(font_size):
#     """Simple heuristic: bigger font => higher heading level"""
#     if font_size > 16:
#         return 1  # H1
#     elif font_size > 13:
#         return 2  # H2
#     else:
#         return 3  # H3



import fitz  # PyMuPDF
from layoutparser.models import Detectron2LayoutModel

from PIL import Image

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    model = Detectron2LayoutModel(
        'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
        extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
        label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
    )
    headings = []

    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        layout = model.detect(img)
        for block in layout:
            if block.type == "Title":
                headings.append({
                    "text": block.text if hasattr(block, "text") else "",
                    "page": page_num + 1,
                    "bbox": block.block,  # bounding box
                })

    return headings