from ingestion.extract import extract_pages
from ingestion.structure import build_document_tree
from ingestion.chunk import chunk_document


PDF_PATH = "data/policies/family_plus.pdf"

pages = extract_pages(PDF_PATH)
root = build_document_tree(pages)
chunks = chunk_document(root, max_chars=3000)


for chunk in chunks:
    text = chunk.text.lower()

    if "room rent" in text or "product benefit table" in text:
        print("\n" + "=" * 80)
        print("TITLE:", chunk.title)
        print("PATH:", " > ".join(chunk.path))
        print("PAGES:", chunk.page_start, "-", chunk.page_end)
        print("=" * 80)
        print(chunk.text[:1500])