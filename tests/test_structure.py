from ingestion.extract import extract_pages
from ingestion.structure import build_document_tree


def print_tree(node, indent=0):

    print(
        "  " * indent
        + f"[L{node.level}] {node.title}"
    )

    for child in node.children:
        print_tree(child, indent + 1)


pages = extract_pages(
    "data/policies/family_plus.pdf"
)

root = build_document_tree(pages)

print_tree(root)