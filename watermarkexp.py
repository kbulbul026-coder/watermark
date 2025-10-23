'''






Logo

latest
 
Search docs
User Guide

Installation
Migration Guide: 1.x to 2.x
Imports and Modules
Naming Adjustments
Robustness and strict=False
Exceptions, Warnings, and Log messages
Metadata
Extract Text from a PDF
Post-Processing of Text Extraction
Extract Images
Other images
Handle Attachments
Encryption and Decryption of PDFs
Merging PDF files
Cropping and Transforming PDFs
Transforming several copies of the same page
Reading PDF Annotations
Adding PDF Annotations
Adding a Stamp or Watermark to a PDF
Stamp (Overlay) / Watermark (Underlay)
Stamping images directly
Adding JavaScript to a PDF
Adding Viewer Preferences
Interactions with PDF Forms
Streaming Data with pypdf
Reduce PDF File Size
PDF Version Support
PDF/A Compliance
API Reference

The PdfReader Class
The PdfWriter Class
The Destination Class
The DocumentInformation Class
The Field Class
The Fit Class
The PageObject Class
The PageRange Class
The PaperSize Class
The RectangleObject Class
The Transformation Class
The XmpInformation Class
The annotations module
Constants
Errors
Generic PDF objects
The PdfDocCommon Class
Developer Guide

Developer Intro
The PDF Format
How pypdf parses PDF files
How pypdf writes PDF files
CMaps
The Deprecation Process
Documentation
Testing
Releasing
About pypdf

CHANGELOG
Changelog of PyPDF2 1.X
Project Governance
Taking Ownership of pypdf
History of pypdf
Contributors
Scope of pypdf
pypdf vs X
Frequently Asked Questions
AI-powered ad network for devs. Get your message in front of the right developers with EthicalAds.
Close Ad
pypdf
 Adding a Stamp or Watermark to a PDF
Adding a Stamp or Watermark to a PDF
Adding stamps or watermarks are two common ways to manipulate PDF files. A stamp is adding something on top of the document, a watermark is in the background of the document.

Stamp (Overlay) / Watermark (Underlay)
The process of stamping and watermarking is the same, you just need to set over parameter to True for stamping and False for watermarking.

You can use merge_page() if you don’t need to transform the stamp:
'''
from pypdf import PdfReader, PdfWriter

stamp = PdfReader("bg.pdf").pages[0]
writer = PdfWriter(clone_from="source.pdf")
for page in writer.pages:
    page.merge_page(stamp, over=False)  # here set to False for watermarking

writer.write("out.pdf")
Otherwise use merge_transformed_page() with Transformation if you need to translate, rotate, scale, etc. the stamp before merging it to the content page.

from pathlib import Path
from typing import List, Union

from pypdf import PdfReader, PdfWriter, Transformation


def stamp(
    content_pdf: Union[Path, str],
    stamp_pdf: Union[Path, str],
    pdf_result: Union[Path, str],
    page_indices: Union[None, List[int]] = None,
):
    stamp_page = PdfReader(stamp_pdf).pages[0]

    writer = PdfWriter()
    # page_indices can be a List(array) of page, tuples are for range definition
    reader = PdfReader(content_pdf)
    writer.append(reader, pages=page_indices)

    for content_page in writer.pages:
        content_page.merge_transformed_page(
            stamp_page,
            Transformation().scale(0.5),
        )

    writer.write(pdf_result)


stamp("example.pdf", "stamp.pdf", "out.pdf")
If you are experiencing wrongly rotated watermarks/stamps, try to use transfer_rotation_to_content() on the corresponding pages beforehand to fix the page boxes.

Example of stamp: stamp.png

Example of watermark: watermark.png

Stamping images directly
The above code only works for stamps that are already in PDF format. However, you can easily convert an image to PDF image using Pillow.

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


stamp_img("aamavas.pdf", "example.png", "out.pdf")
