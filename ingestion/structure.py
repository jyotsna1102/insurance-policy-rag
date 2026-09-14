import re

from ingestion.document import DocumentNode

def detect_level(line: str, parent: DocumentNode) -> int | None:
    line = line.strip()

    if not line:
        return None

    # Major structural headings
    if re.match(
        r"^(SECTION|CHAPTER)\s+\d+\b",
        line,
        re.IGNORECASE,
    ):
        return 0

    if re.match(
        r"^(ANNEXURE|APPENDIX)\s+[IVX0-9]+",
        line,
        re.IGNORECASE,
    ):
        return 0

    # Definitions
    if re.match(r"^Def\.\s*\d+\.", line, re.IGNORECASE):
        return 1

    # Numbered headings such as:
    # 3.1 Inpatient Care
    # 3.10 AYUSH Treatment
    numbered_heading = re.match(
        r"^(\d+\.\d+(?:\.\d+)*)\s+(.+)$",
        line,
    )

    if numbered_heading:
        return 2

    # A simple "1." is ambiguous.
    # Treat it as content unless we have strong evidence
    # that it is a structural heading.
    return None


def build_document_tree(pages):
    root = DocumentNode(
        title="Family Plus Policy Document",
        level=-1,
    )

    stack = [root]

    for page in pages:

        lines = page["text"].splitlines()

        for raw_line in lines:
            line = raw_line.strip()

            if not line:
                continue

            level = detect_level(line, stack[-1])

            if level is None:
                stack[-1].content += line + "\n"
                continue

            node = DocumentNode(
                title=line,
                level=level,
                page_start=page["page"],
                page_end=page["page"],
            )

            while stack and stack[-1].level >= level:
                stack.pop()

            stack[-1].add_child(node)

            stack.append(node)

    return root