


#Paper size identifier
from pypdf import PdfReader

# Open the PDF file
pdf_path = "original.pdf"
reader = PdfReader(pdf_path)

# Access the first page
page = reader.pages[0]

# The mediaBox is a RectangleObject with the page dimensions
mediabox = page.mediabox

# The dimensions are given in points (72 points = 1 inch)
width_in_points = mediabox.width
height_in_points = mediabox.height

# Convert points to inches
points_per_inch = 72
width_in_inches = float(width_in_points) / points_per_inch
height_in_inches = float(height_in_points) / points_per_inch

print(f"Page size (in points): {width_in_points} x {height_in_points}")
print(f"Page size (in inches): {width_in_inches:.2f} x {height_in_inches:.2f}")

# Example to check if the page is A4 (8.27 x 11.69 inches)
if (width_in_inches == 8.27) and (height_in_inches == 11.69):
    print("This page is A4 size.")
