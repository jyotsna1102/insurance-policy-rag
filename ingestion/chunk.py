from dataclasses import dataclass
import re

from .document import DocumentNode


@dataclass
class DocumentChunk:
    text: str
    title: str
    path: list[str]
    page_start: int | None
    page_end: int | None


def chunk_document(
    node: DocumentNode,
    max_chars: int = 3000,
    path: list[str] | None = None,
) -> list[DocumentChunk]:

    if path is None:
        path = []

    current_path = path + [node.title]

    chunks = []

    # First process child nodes.
    for child in node.children:
        chunks.extend(
            chunk_document(
                child,
                max_chars=max_chars,
                path=current_path,
            )
        )

    # Then process content belonging directly to this node.
    if node.content.strip():
        chunks.extend(
            chunk_content(
                node.content,
                node.title,
                current_path,
                node.page_start,
                node.page_end,
                max_chars,
            )
        )

    return chunks


def chunk_content(
    content: str,
    title: str,
    path: list[str],
    page_start: int | None,
    page_end: int | None,
    max_chars: int,
) -> list[DocumentChunk]:

    lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    list_items = detect_numbered_items(lines)

    # If we found a meaningful numbered sequence,
    # use item-level chunks.
    if len(list_items) >= 3:
        return [
            make_chunk(
                text=item,
                title=title,
                path=path,
                page_start=page_start,
                page_end=page_end,
            )
            for item in list_items
        ]

    # Otherwise treat the content as normal prose.
    return split_prose(
        content,
        title,
        path,
        page_start,
        page_end,
        max_chars,
    )


def detect_numbered_items(lines: list[str]) -> list[str]:
    """
    Detect generic numbered list/table items.

    Supports formats such as:

        1. Cancer
        2. Heart Attack

    and PDF-extracted table/list formats such as:

        77
        Microscope Cover
        Payable under OT Charges

        78
        Surgical Blade
        Payable under OT Charges
    """

    items = []
    current_item = None

    for line in lines:

        # Number followed by text:
        #
        # 1. Cancer
        # 2) Heart Attack
        # 3.10 AYUSH Treatment
        inline_match = re.match(
            r"^(\d+(?:\.\d+)*)(?:[.)])\s+(.+)$",
            line,
        )

        # Number by itself:
        #
        # 77
        # Microscope Cover
        number_only_match = re.match(
            r"^\d+$",
            line,
        )

        if inline_match:
            if current_item is not None:
                items.append(" ".join(current_item))

            current_item = [
                f"{inline_match.group(1)}. {inline_match.group(2)}"
            ]

        elif number_only_match:
            if current_item is not None:
                items.append(" ".join(current_item))

            current_item = [line]

        elif current_item is not None:
            current_item.append(line)

    if current_item is not None:
        items.append(" ".join(current_item))

    return items


def split_prose(
    content: str,
    title: str,
    path: list[str],
    page_start: int | None,
    page_end: int | None,
    max_chars: int,
) -> list[DocumentChunk]:

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", content)
        if paragraph.strip()
    ]

    chunks = []
    current_parts = []
    current_length = 0

    for paragraph in paragraphs:

        paragraph_length = len(paragraph)

        if (
            current_parts
            and current_length + paragraph_length + 1 > max_chars
        ):
            chunks.append(
                make_chunk(
                    text="\n\n".join(current_parts),
                    title=title,
                    path=path,
                    page_start=page_start,
                    page_end=page_end,
                )
            )

            current_parts = []
            current_length = 0

        if paragraph_length > max_chars:
            chunks.extend(
                split_large_paragraph(
                    paragraph,
                    title,
                    path,
                    page_start,
                    page_end,
                    max_chars,
                )
            )
            continue

        current_parts.append(paragraph)
        current_length += paragraph_length + 1

    if current_parts:
        chunks.append(
            make_chunk(
                text="\n\n".join(current_parts),
                title=title,
                path=path,
                page_start=page_start,
                page_end=page_end,
            )
        )

    return chunks


def split_large_paragraph(
    paragraph: str,
    title: str,
    path: list[str],
    page_start: int | None,
    page_end: int | None,
    max_chars: int,
) -> list[DocumentChunk]:

    sentences = re.split(
        r"(?<=[.!?])\s+",
        paragraph,
    )

    chunks = []
    current_parts = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        if (
            current_parts
            and current_length + sentence_length + 1 > max_chars
        ):
            chunks.append(
                make_chunk(
                    text=" ".join(current_parts),
                    title=title,
                    path=path,
                    page_start=page_start,
                    page_end=page_end,
                )
            )

            current_parts = []
            current_length = 0

        current_parts.append(sentence)
        current_length += sentence_length + 1

    if current_parts:
        chunks.append(
            make_chunk(
                text=" ".join(current_parts),
                title=title,
                path=path,
                page_start=page_start,
                page_end=page_end,
            )
        )

    return chunks


def make_chunk(
    text: str,
    title: str,
    path: list[str],
    page_start: int | None,
    page_end: int | None,
) -> DocumentChunk:

    return DocumentChunk(
        text=text.strip(),
        title=title,
        path=path,
        page_start=page_start,
        page_end=page_end,
    )