"""Views for simple app"""
import django.contrib.auth
from datetime import datetime
from django.shortcuts import render, redirect
from simple_automation.forms import SignupForm, LoginForm


def user_register_view(response):
    """Register form"""
    if response.method == 'POST':
        form = SignupForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('simple_app.html')  # Redirect to login page after successful registration
    else:
        form = SignupForm()
    return render(response, 'register.html', {'form': form})


def user_login_view(request):
    """User login function"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = django.contrib.auth.authenticate(request, username=username, password=password)
            if user:
                django.contrib.auth.login(request, user)
                return redirect('main_work_screen.html')
    else:
        form = LoginForm()
    return render(request, 'simple_app.html', {'form': form})

# TODO logout button, button
# # logout page
# def user_logout(request):
#     logout(request)
#     return redirect('login')


def main_work_screen_view(request):
    """Main work screen render"""
    return render(request, 'main_work_screen.html')


def clock_view(request):
    now = datetime.now()
    context = {
        'current_time': now.strftime("%H:%M:%S"),
        'current_date': now.strftime("%Y-%m-%d"),
    }
    return render(request, 'main_work_screen.html', context)


def user_check(request):
    user = request.user
    return render(request, 'main_work_screen.html', {'user': user})
