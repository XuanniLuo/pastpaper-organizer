from pypdf import PdfWriter, PdfReader
 
# 要合并的PDF文件，按顺序排列
pdf_files = [
    "9702_m25_qp_22_Q1_Physical_quantities_and_units_1_3_2.pdf",
    "9702_w25_qp_22_Q1_Physical_quantities_and_units.pdf",
]
 
writer = PdfWriter()
for pdf_file in pdf_files:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
 
with open("paper2 topic 1.pdf", "wb") as f:
    writer.write(f)
 
print("合并完成，共", len(writer.pages), "页")