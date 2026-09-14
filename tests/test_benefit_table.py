import pymupdf

PDF_PATH = "data/policies/family_plus.pdf"

doc = pymupdf.open(PDF_PATH)

for page_number in range(55, 59):
    page = doc[page_number]

    print("\n" + "=" * 100)
    print("PAGE:", page_number + 1)
    print("=" * 100)
    print(page.get_text())