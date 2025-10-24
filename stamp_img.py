#Another watermark app

from io import BytesIO
from pathlib import Path
from typing import List, Union

from PIL import Image
from pypdf import PageRange, PdfReader, PdfWriter, Transformation


def image_to_pdf(stamp_img: Union[Path, str]) -> PdfReader:
    img = Image.open(stamp_img)
    img_as_pdf = BytesIO()
    img.save(img_as_pdf, "pdf")
    return PdfReader(img_as_pdf)


def stamp_img(
    content_pdf: Union[Path, str],
    stamp_img: Union[Path, str],
    pdf_result: Union[Path, str],
    page_indices: Union[PageRange, List[int], None] = None,
):
    # Convert the image to a PDF
    stamp_pdf = image_to_pdf(stamp_img)

    # Then use the same stamp code from above
    stamp_page = stamp_pdf.pages[0]

    writer = PdfWriter()

    reader = PdfReader(content_pdf)
    writer.append(reader, pages=page_indices)
    for content_page in writer.pages:
        content_page.merge_transformed_page(
            stamp_page,
            Transformation(),
        )

    with open(pdf_result, "wb") as fp:
        writer.write(fp)


stamp_img("original.pdf", "input.jpg", "out.pdf")

