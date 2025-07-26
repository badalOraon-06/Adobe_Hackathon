import fitz  # PyMuPDF
from collections import Counter
import re


def is_heading_candidate(text, size, body_size, is_bold):
    score = 0
    level = None

    if not text or len(text) > 100 or len(text.split()) > 15:
        return (0, None)
    if text.endswith(('.', ':', ';', ',')):
        return (0, None)
    if not re.match(r"^[A-Z0-9]", text):
        return (0, None)

    if size >= body_size + 6:
        score += 3
        level = "H1"
    elif size >= body_size + 3:
        score += 2
        level = "H2"
    elif size >= body_size + 1:
        score += 1
        level = "H3"

    if is_bold:
        score += 1
    if re.match(r"^\d+(\.\d+)*\s", text):
        score += 1

    return (score, level if score >= 2 else None)


def remove_numbers_if_only_numbers(text):
    if re.match(r'^\d+(\.\d+)*$', text.strip()):
        return ""
    return text


def extract_outline(pdf_path):
    outline = []
    title = ""
    font_sizes = []
    used_title_span_ids = set()

    try:
        document = fitz.open(pdf_path)

        # --- Title Extraction ---
        if document.page_count > 0:
            first_page = document[0]
            blocks = first_page.get_text("dict")["blocks"]
            largest_size = 0
            potential_titles = []

            for block in blocks:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = round(span["size"], 1)
                        font_name = span.get("font", "").lower()
                        is_bold = "bold" in font_name or "bd" in font_name

                        if not text or len(text.split()) > 12:
                            continue
                        if abs(span["bbox"][2] - span["bbox"][0]) < 50:
                            continue

                        font_sizes.append(size)

                        if size > largest_size:
                            largest_size = size
                            potential_titles = [(is_bold, size, text, span["bbox"])]
                        elif size == largest_size:
                            potential_titles.append((is_bold, size, text, span["bbox"]))

            if potential_titles:
                potential_titles.sort(key=lambda x: (-x[0], -x[1], -len(x[2])))
                title = potential_titles[0][2]
                title_bbox = potential_titles[0][3]
                used_title_span_ids.add(tuple(title_bbox))

        # --- Body Font Size Estimate ---
        for page in document:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.append(round(span["size"], 1))

        font_counter = Counter(font_sizes)
        most_common = [size for size, _ in font_counter.most_common()]
        body_font = most_common[-1] if most_common else 12

        # --- Heading Extraction ---
        for page_num, page in enumerate(document, 1):
            blocks = page.get_text("dict")["blocks"]
            blocks.sort(key=lambda b: b["bbox"][1])  # Top-to-bottom

            all_lines = []
            for block in blocks:
                if block["type"] != 0:
                    continue
                for line in block["lines"]:
                    spans = line.get("spans", [])
                    if not spans:
                        continue

                    font_sizes_line = [round(span["size"], 1) for span in spans]
                    font_names_line = [span.get("font", "").lower() for span in spans]
                    bold_flags = [("bold" in fn or "bd" in fn) for fn in font_names_line]
                    is_bold = bold_flags[0] if bold_flags else False

                    full_text = " ".join(span["text"].strip() for span in spans).strip()
                    line_bbox = spans[0]["bbox"] if spans else None

                    all_lines.append({
                        "text": full_text,
                        "sizes": font_sizes_line,
                        "is_bold": is_bold,
                        "bbox": line_bbox,
                        "spans": spans
                    })

            # Now evaluate each line
            for i in range(len(all_lines) - 1):
                line = all_lines[i]
                next_line = all_lines[i + 1]

                if len(set(line["sizes"])) > 1:
                    continue
                if any(tuple(span["bbox"]) in used_title_span_ids for span in line["spans"]):
                    continue

                current_text = line["text"]
                next_text = next_line["text"]

                if not current_text or not next_text:
                    continue

                cleaned = remove_numbers_if_only_numbers(current_text)
                if not cleaned:
                    continue

                avg_size = line["sizes"][0]
                next_avg_size = next_line["sizes"][0] if len(set(next_line["sizes"])) == 1 else avg_size

                if avg_size <= next_avg_size:
                    continue

                # NEW LOGIC: if any span qualifies, use entire line as heading
                found_heading = False
                final_level = None

                for span in line["spans"]:
                    span_text = span["text"].strip()
                    if not span_text:
                        continue

                    span_size = round(span["size"], 1)
                    font_name = span.get("font", "").lower()
                    is_bold = "bold" in font_name or "bd" in font_name

                    cleaned_span_text = remove_numbers_if_only_numbers(span_text)
                    if not cleaned_span_text:
                        continue

                    score, level = is_heading_candidate(cleaned_span_text, span_size, body_font, is_bold)
                    if level:
                        found_heading = True
                        if final_level is None or level < final_level:
                            final_level = level

                if found_heading:
                    outline.append({
                        "level": final_level,
                        "text": current_text,
                        "page": page_num
                    })

    except Exception as e:
        print(f"[Error] Failed to process '{pdf_path}': {e}")

    return {
        "title": title,
        "outline": outline
    }