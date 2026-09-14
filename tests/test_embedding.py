from ingestion.extract import extract_pages
from ingestion.structure import build_document_tree
from ingestion.chunk import chunk_document
from embeddings.embed import Embedder


PDF_PATH = "data/policies/family_plus.pdf"


# 1. Extract PDF
pages = extract_pages(PDF_PATH)

print("Pages:", len(pages))


# 2. Build document tree
root = build_document_tree(pages)

print("Document tree built")


# 3. Create chunks
chunks = chunk_document(
    root,
    max_chars=3000,
)

print("Chunks:", len(chunks))


# 4. Embed one chunk
embedder = Embedder()

chunk = chunks[0]

vector = embedder.embed(chunk.text)


# 5. Inspect result
print("\nFirst chunk:")
print(chunk.text[:500])

print("\nEmbedding dimension:", len(vector))
print("First 5 values:", vector[:5])