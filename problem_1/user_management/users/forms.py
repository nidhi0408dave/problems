from django import forms
from .models import User, UserInfo

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = forms.CharField(widget=forms.PasswordInput())

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['date_of_birth', 'mobile', 'gender', 'address']
