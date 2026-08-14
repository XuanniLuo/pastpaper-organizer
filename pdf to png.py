import fitz  # pip install pymupdf

doc = fitz.open("input.pdf")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    pix.save(f"page_{i+1}.png")