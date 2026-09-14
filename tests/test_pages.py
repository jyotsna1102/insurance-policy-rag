from ingestion.extract import extract_pages

pages = extract_pages(
    "data/policies/family_plus.pdf"
)

page = pages[52]

print(page["text"])