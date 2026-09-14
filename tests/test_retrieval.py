from embeddings.embed import Embedder
from db.setup import search_chunks


embedder = Embedder()

queries = [
    "Is maternity treatment covered?",
    "What are the waiting periods?",
    "What expenses are excluded from the policy?",
    "Is hospitalization covered?",
    "What is the room rent limit?",
]


for query in queries:
    print("\n" + "=" * 80)
    print("QUERY:", query)
    print("=" * 80)

    query_embedding = embedder.embed_query(query)

    results = search_chunks(query_embedding, limit=5)

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

        print("\n-----------------------------")
        print("Chunk ID:", chunk_id)
        print("Title:", title)
        print("Pages:", page_start, "-", page_end)
        print("Distance:", round(distance, 4))
        print("Text:", chunk_text[:500])