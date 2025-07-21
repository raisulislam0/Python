import fitz  # PyMuPDF

doc = fitz.open("ReDoc.pdf")
page = doc[0]  # Modify first page

# Search for the word to replace
search_term = "POST"
replacement = "PUT"

text_instances = page.search_for(search_term)

for inst in text_instances:
    # Redact the original text
    page.add_redact_annot(inst, fill=(1, 1, 1))  # white background
    page.apply_redactions()

    # Add new text in the same position
    x, y = inst.x0, inst.y1 - 2  # slightly adjust for baseline
    page.insert_text((x, y), replacement, fontsize=10, color=(0, 0, 0))

doc.save("rr.pdf")
