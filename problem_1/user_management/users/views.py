from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserInfo
from .forms import UserForm, UserInfoForm
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def list_users(request):
    users = User.objects.all()
    return render(request, 'users/list_users.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        if user_form.is_valid() and user_info_form.is_valid():
            # Create user
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Create user_info
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()

            messages.success(request, 'User added successfully')
            return redirect('list_users')
    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    return render(request, 'users/add_user.html', {'user_form': user_form, 'user_info_form': user_info_form})

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user_info = UserInfo.objects.get(user=user)
    user_info.delete()
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('list_users')

def export_users_pdf(request):
    users = User.objects.all()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    text = "User List:\n\n"
    for user in users:
        text += f"Username: {user.username}, Email: {user.email}\n"
    
    p.drawString(100, 750, text)
    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
