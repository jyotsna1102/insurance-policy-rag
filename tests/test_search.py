from embeddings.embed import Embedder
from db.setup import search_chunks


embedder = Embedder()

queries = [
    "room rent limit",
    "room rent maximum",
    "Product Benefits Table room rent",
]


for query in queries:
    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    embedding = embedder.embed_query(query)

    results = search_chunks(embedding, limit=10)

    for result in results:
        (
            chunk_id,
            chunk_text,
            title,
            path,
            page_start,
            page_end,
            distance,
        ) = result

        print(
            f"\nID: {chunk_id} | "
            f"Title: {title} | "
            f"Pages: {page_start}-{page_end} | "
            f"Distance: {distance:.4f}"
        )

        print(chunk_text[:700])