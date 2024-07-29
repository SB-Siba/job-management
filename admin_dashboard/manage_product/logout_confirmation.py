from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logout_confirm(request):
    return render(request, 'logout_confirm.html')

def logout_action(request):
    logout(request)
    return redirect('admin_dashboard.html')  # Replace 'home' with your desired redirect URL
