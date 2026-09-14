from ingestion.extract import extract_pages
from ingestion.structure import build_document_tree
from ingestion.chunk import chunk_document
from embeddings.embed import Embedder
from db.setup import insert_chunk


PDF_PATH = "data/policies/family_plus.pdf"
DOCUMENT_ID = "family_plus_v1"


def ingest_policy(pdf_path: str, document_id: str):

    # 1. Extract
    pages = extract_pages(pdf_path)
    print(f"Extracted {len(pages)} pages")

    # 2. Build document structure
    root = build_document_tree(pages)
    print("Document structure built")

    # 3. Create chunks
    chunks = chunk_document(root, max_chars=3000)
    print(f"Created {len(chunks)} chunks")

    # 4. Load embedding model once
    embedder = Embedder()

    # 5. Embed all chunks in one batch
    texts = [chunk.text for chunk in chunks]

    embeddings = embedder.model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    # 6. Insert chunks + embeddings
    for chunk, embedding in zip(chunks, embeddings):

        insert_chunk(
            document_id=document_id,
            chunk_text=chunk.text,
            title=chunk.title,
            path=chunk.path,
            page_start=chunk.page_start,
            page_end=chunk.page_end,
            embedding=embedding.tolist(),
        )

    print(f"Inserted {len(chunks)} chunks")


if __name__ == "__main__":
    ingest_policy(
        PDF_PATH,
        DOCUMENT_ID,
    )