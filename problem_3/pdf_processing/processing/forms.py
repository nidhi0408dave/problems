from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Select PDF')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
