import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "insurance_rag",
    "user": "postgres",
    "password": "postgres",
}


def create_tables():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS policy_chunks (
                    id BIGSERIAL PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    chunk_text TEXT NOT NULL,
                    title TEXT,
                    path TEXT[],
                    page_start INTEGER,
                    page_end INTEGER,
                    embedding VECTOR(384)
                )
            """)

        conn.commit()

def insert_chunk(
    document_id: str,
    chunk_text: str,
    title: str,
    path: list[str],
    page_start: int | None,
    page_end: int | None,
    embedding: list[float],
):
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO policy_chunks (
                    document_id,
                    chunk_text,
                    title,
                    path,
                    page_start,
                    page_end,
                    embedding
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    document_id,
                    chunk_text,
                    title,
                    path,
                    page_start,
                    page_end,
                    embedding,
                ),
            )

        conn.commit()

def search_chunks(
    query_embedding: list[float],
    limit: int = 5,
):
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    chunk_text,
                    title,
                    path,
                    page_start,
                    page_end,
                    embedding <=> %s::vector AS distance
                FROM policy_chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (query_embedding, query_embedding, limit),
            )

            return cur.fetchall()


if __name__ == "__main__":
    create_tables()
    print("Database setup complete.")