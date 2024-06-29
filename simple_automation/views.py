"""Views for simple app"""
import zipfile
import io
from datetime import datetime
import django.contrib.auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from simple_automation.forms import SignupForm, LoginForm, UploadFileForm


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

# TODO logout button
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


def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="modified_files.zip"'

        # Create a zip file to hold the modified files
        with io.BytesIO() as zip_buffer:
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in files:
                    # Check if the file ends with .txt
                    if uploaded_file.name.endswith('.txt'):
                        # Read the uploaded file
                        file_content = uploaded_file.read().decode('utf-8')

                        # Replace '1.4301-4.0' with '1.4301'
                        new_content = file_content.replace('1.4301-4.0', '1.4301')

                        # Add the modified file to the zip
                        zip_file.writestr(uploaded_file.name, new_content)

            # Set the zip buffer's position to the beginning
            zip_buffer.seek(0)
            response.write(zip_buffer.read())

        return response
    else:
        form = UploadFileForm()
        return render(request, 'main_work_screen.html', {'form': form})

