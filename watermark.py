from PyPDF2 import PdfReader, PdfWriter

def add_watermark_pypdf2(input_pdf, watermark_pdf, output_pdf):
    reader = PdfReader(input_pdf)  # Use PdfReader
    watermark = PdfReader(watermark_pdf)  # Use PdfReader
    writer = PdfWriter()  # Use PdfWriter

    watermark_page = watermark.pages[0]  # Access pages via .pages[index]

    for page in reader.pages:
        page.merge_page(watermark_page)  # Use merge_page
        writer.add_page(page)  # Use add_page

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

add_watermark_pypdf2("original.pdf", "a8.pdf", "res2.pdf")
