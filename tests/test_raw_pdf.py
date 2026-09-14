import pymupdf

PDF_PATH = "data/policies/family_plus.pdf"

doc = pymupdf.open(PDF_PATH)

for page_number, page in enumerate(doc):
    text = page.get_text()

    if "Room Rent" in text or "Product Benefit" in text:
        print("\n" + "=" * 80)
        print("PAGE:", page_number + 1)
        print("=" * 80)
        print(text[:5000])