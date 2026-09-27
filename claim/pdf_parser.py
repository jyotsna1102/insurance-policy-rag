import pymupdf as pdf_parser


def extract_pages_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extract text from every page of a PDF.

    Returns:
        [
            {
                "page_number": 1,
                "text": "..."
            },
            ...
        ]
    """

    document = pdf_parser.open(pdf_path)

    pages = []

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")

            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })
    finally:
        document.close()

    return pages


def extract_text_from_pdf(pdf_path: str) -> str:
    pages = extract_pages_from_pdf(pdf_path)

    extracted_text = []

    for page in pages:
        if page["text"]:
            extracted_text.append(
                f"--- Page {page['page_number']} ---\n"
                f"{page['text']}"
            )

    text = "\n\n".join(extracted_text)

    if not text.strip():
        raise ValueError(
            "No text could be extracted from this PDF. "
            "The PDF may be scanned and require OCR."
        )

    return text