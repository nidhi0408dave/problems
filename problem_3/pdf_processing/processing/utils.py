import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
import tempfile
from reportlab.lib.pagesizes import letter
from django.conf import settings

# Utility function to create a watermark PDF
def create_watermark(text, output_path="watermark.pdf"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 40)
    c.setFillAlpha(0.3)
    c.drawString(100, 500, text)
    c.save()

    # Make sure to write to disk correctly
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())

    return output_path

# Function to add watermark to the original PDF

def add_watermark(input_pdf_path, watermark_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    watermark_reader = PdfReader(watermark_pdf_path)
    watermark_page = watermark_reader.pages[0]

    for i, page in enumerate(reader.pages):
        try:
            if page.get_contents() is None:
                print(f"Skipping empty page {i}")
                continue
            page.merge_page(watermark_page)
            writer.add_page(page)
        except Exception as e:
            print(f"Error processing page {i}: {e}")
            continue

    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)


# Function to password protect the PDF
def password_protect(input_pdf, password, output_pdf):
    with open(input_pdf, "rb") as original_file:
        reader = PdfReader(original_file)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)
