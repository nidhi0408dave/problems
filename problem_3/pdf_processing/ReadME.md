### Python Environment (Pyenv)
## pyenv virtualenv 3.11.8 problem_3
## pyenv activate problem_3

### Install Dependencies
## pip install -r requirements.txt

### Create Migrations
## python manage.py makemigrations

### Apply Migrations
## python manage.py migrate

### Run the Server
## python manage.py runserver

# Visit: http://127.0.0.1:8000/processing/upload/

### Features
### Upload Page: Users can upload any valid PDF file.
### Watermark: "CONFIDENTIAL" watermark is added using PyPDF2.
### Password Protection: PDF is encrypted with a default password.
### File Storage: Processed PDFs are saved in the /media/ directory on the server.