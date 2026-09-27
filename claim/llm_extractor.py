import os
import json
from pathlib import Path
from typing import Type, TypeVar
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel


load_dotenv(Path(__file__).resolve().parents[1] / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

T = TypeVar("T", bound=BaseModel)


SYSTEM_PROMPT = """
You are a medical document information extraction system.

Your task is to extract structured information from the
provided medical document.

Rules:

1. Extract information only when it is explicitly present
   in the document.

2. Do not guess or infer missing information.

3. If a field is not present, return null.

4. Preserve the meaning of the original document.

5. Dates should be returned in the format expected by the
   provided schema.

6. Numeric amounts should be returned as numbers.

7. If multiple values appear for a field, use the value that
   most clearly represents the requested field.

8. The document may have different layouts or formatting.
   Focus on the meaning of the content rather than its position.

9. Do not add information that is not supported by the document.

10. When the schema contains a procedures field, include explicitly documented
    diagnostic tests, treatments, procedures, and supportive care in that field.

Return the extracted result as a JSON object matching the provided schema.
"""


def extract_structured_data(
    document_text: str,
    schema: Type[T],
    model="openai/gpt-oss-120b",
) -> T:

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    "Extract the document into this JSON schema. "
                    "Use exactly these field names and include every required field.\n\n"
                    f"JSON schema:\n{json.dumps(schema.model_json_schema(), indent=2)}\n\n"
                    f"Document:\n{document_text}"
                ),
            },
        ],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return schema.model_validate(json.loads(content))