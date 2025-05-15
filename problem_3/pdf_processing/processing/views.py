import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from .forms import PDFUploadForm
from .utils import create_watermark, add_watermark, password_protect
from PyPDF2 import PdfReader


# Utility function to check if the uploaded file is a valid PDF
def is_valid_pdf(file_path):
    try:
        # Try reading the file with PyPDF2
        reader = PdfReader(file_path)
        return True
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return False


# Handle the PDF upload, watermark, and password protection
def upload_pdf(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the uploaded file and password
            pdf_file = request.FILES['pdf_file']
            password = form.cleaned_data['password']

            # Log the file size and name to confirm it's being uploaded correctly
            print(f"Uploaded file: {pdf_file.name}, Size: {pdf_file.size} bytes")
            print(
                f"File content (first 100 bytes): {pdf_file.read(100)}")  # Check the first 100 bytes of the uploaded file

            # Check if the uploaded file is empty
            if pdf_file.size == 0:
                return HttpResponseBadRequest("Uploaded file is empty.")

            # Create the upload and output directories if they don't exist
            upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
            output_dir = os.path.join(settings.BASE_DIR, 'output')
            os.makedirs(upload_dir, exist_ok=True)
            os.makedirs(output_dir, exist_ok=True)

            # Save the uploaded file
            pdf_path = os.path.join(upload_dir, pdf_file.name)
            with open(pdf_path, 'wb') as f:
                f.write(pdf_file.read())

            # Recheck file size after saving it
            if os.path.getsize(pdf_path) == 0:
                return HttpResponseBadRequest("Uploaded file is empty after saving.")

            # Log the final file path and size
            print(f"File saved successfully at: {pdf_path}, Size: {os.path.getsize(pdf_path)} bytes")

            # Check if the file is a valid PDF
            if not is_valid_pdf(pdf_path):
                return HttpResponseBadRequest("Uploaded file is not a valid PDF.")

            # Create the watermark
            watermark_pdf = create_watermark('CONFIDENTIAL')

            # Define output paths for watermarked and password-protected PDFs
            watermarked_pdf_path = os.path.join(output_dir, f"watermarked_{pdf_file.name}")
            protected_pdf_path = os.path.join(output_dir, f"protected_{pdf_file.name}")

            # Add watermark to the PDF
            add_watermark(pdf_path, watermark_pdf, watermarked_pdf_path)

            # Apply password protection to the watermarked PDF
            password_protect(watermarked_pdf_path, password, protected_pdf_path)

            # Serve the password-protected PDF as a downloadable file
            with open(protected_pdf_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="protected_{pdf_file.name}"'
                return response

    else:
        # If the form is not submitted or file is missing, create a blank form
        form = PDFUploadForm()

    # Render the upload page with the form
    return render(request, 'upload_pdf.html', {'form': form})
