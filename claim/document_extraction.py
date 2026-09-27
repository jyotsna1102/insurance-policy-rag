from typing import Type, TypeVar

from pydantic import BaseModel

from .pdf_parser import extract_text_from_pdf
from .llm_extractor import extract_structured_data


T = TypeVar("T", bound=BaseModel)


def extract_document(
    pdf_path: str,
    schema: Type[T],
) -> T:

    # Step 1: PDF → text
    document_text = extract_text_from_pdf(pdf_path)

    if not document_text.strip():
        raise ValueError(
            f"No text could be extracted from PDF: {pdf_path}"
        )

    # Step 2: text → structured Pydantic object
    result = extract_structured_data(
        document_text=document_text,
        schema=schema,
    )

    return result