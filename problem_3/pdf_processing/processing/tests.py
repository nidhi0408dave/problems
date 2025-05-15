import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_pdf_upload(client):
    with open('path/to/sample.pdf', 'rb') as pdf_file:
        response = client.post(reverse('upload_pdf'), {
            'pdf_file': pdf_file,
            'password': 'testpassword'
        }, format='multipart')

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'
