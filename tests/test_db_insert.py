from ingestion.extract import extract_pages
from ingestion.structure import build_document_tree
from ingestion.chunk import chunk_document
from embeddings.embed import Embedder
from db.setup import insert_chunk


PDF_PATH = "data/policies/family_plus.pdf"


pages = extract_pages(PDF_PATH)
root = build_document_tree(pages)
chunks = chunk_document(root, max_chars=3000)

embedder = Embedder()

chunk = chunks[0]
embedding = embedder.embed(chunk.text)

insert_chunk(
    document_id="family_plus_v1",
    chunk_text=chunk.text,
    title=chunk.title,
    path=chunk.path,
    page_start=chunk.page_start,
    page_end=chunk.page_end,
    embedding=embedding,
)

print("First chunk inserted successfully.")