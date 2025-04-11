from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Basic validation
        error = None
        if not (username and email and password and password2):
            error = "All fields are required."
        elif password != password2:
            error = "Passwords don't match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif User.objects.filter(email=email).exists():
            error = "Email already exists."
            
        if error:
            return render(request, 'accounts/register.html', {'error': error})
            
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        login(request, user)
        return redirect('store:book_list')
    
    return render(request, 'accounts/register.html')

@login_required
def profile(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Update profile
        profile = request.user.profile
        profile.address = address
        profile.phone = phone
        profile.save()
        return redirect('accounts:profile')
    
    return render(request, 'accounts/profile.html')

def custom_logout(request):
    logout(request)
    return redirect('store:book_list')