import pymupdf


def extract_pages(pdf_path):
    doc = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(doc):
        text = page.get_text().strip()

        if text:
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    return pages