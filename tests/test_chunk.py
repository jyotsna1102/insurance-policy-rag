from ingestion.extract import extract_pages
from ingestion.structure import build_document_tree
from ingestion.chunk import chunk_document


pages = extract_pages(
    "data/policies/family_plus.pdf"
)

root = build_document_tree(pages)

chunks = chunk_document(
    root,
    max_chars=3000,
)

print("Total chunks:", len(chunks))

# for i, chunk in enumerate(chunks[:10], start=1):
#     print("\n--- CHUNK", i, "---")
#     print("Title:", chunk.title)
#     print("Path:", " > ".join(chunk.path))
#     print("Pages:", chunk.page_start, "-", chunk.page_end)
#     print("Length:", len(chunk.text))
#     print(chunk.text[:500])

# largest = sorted(
#     chunks,
#     key=lambda chunk: len(chunk.text),
#     reverse=True,
# )

# print("\n\n===== LARGEST CHUNKS =====")

# for i, chunk in enumerate(largest[:10], start=1):
#     print(f"\n--- LARGE CHUNK {i} ---")
#     print("Title:", chunk.title)
#     print("Path:", " > ".join(chunk.path))
#     print("Pages:", chunk.page_start, "-", chunk.page_end)
#     print("Length:", len(chunk.text))
#     print(chunk.text[:1000])

print("\n\n===== LIST/TABLE CHUNKS =====")

for chunk in chunks:
    if "Annexure III" in chunk.title or "Annexure I" in chunk.title:
        print("\n--- ITEM ---")
        print("Title:", chunk.title)
        print("Pages:", chunk.page_start, "-", chunk.page_end)
        print("Length:", len(chunk.text))
        print(chunk.text[:300])