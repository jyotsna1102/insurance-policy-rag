import os
from pathlib import Path
from groq import Groq
from embeddings.embed import Embedder
from dotenv import load_dotenv
from db.setup import search_chunks
from claim.schemas import Claim


load_dotenv(Path(__file__).resolve().parents[1] / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query: str, context: str) -> str:
    prompt = f"""Answer the user's question using ONLY the policy context provided below.
If the answer cannot be determined from the context, say: "I could not find enough information in the policy."
Do not invent policy rules or values. Always mention the relevant policy section and page number when available.

Policy context:
{context}

User question: {query}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response.choices[0].message.content


def generate_claim_answer(claim: Claim, context: str) -> str:
    prompt = f"""Assess the following medical claim using ONLY the policy context provided.
Determine how much of the claim is payable under the policy.
Explain the covered and non-covered amounts when the policy provides enough information.
Use the net payable claim amount from the claim data, not the gross bill amount.
If the policy context does not contain enough information, say so clearly.
Always mention the relevant policy section and page number when available.

Claim JSON:
{claim.model_dump_json(indent=2)}

Policy context:
{context}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response.choices[0].message.content


def retrieve_context(query: str, limit: int = 5) -> str:
    embedder = Embedder()
    query_embedding = embedder.embed_query(query)
    results = search_chunks(query_embedding, limit=limit)

    context_parts = []
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

        section_path = " > ".join(path)
        formatted_chunk = (
            f"Section: {section_path}\n"
            f"Pages: {page_start}-{page_end}\n\n"
            f"{chunk_text.strip()}"
        )
        context_parts.append(formatted_chunk)

    return "\n\n---\n\n".join(context_parts)