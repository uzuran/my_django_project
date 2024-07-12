"""Views for simple app"""
import zipfile
import io
from datetime import datetime
import django.contrib.auth
import pyexcel_ods
from django.http import HttpResponse
from django.shortcuts import render, redirect
from simple_automation.forms import SignupForm, LoginForm, UploadFileForm


def main_work_screen_view(request):
    """Main work screen render"""
    return render(request, 'main_work_screen.html')


def user_register_view(response):
    """Register form"""
    if response.method == 'POST':
        form = SignupForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('simple_app.html')
    else:
        form = SignupForm()
    return render(response, 'register.html', {'form': form})


def user_login_view(request):
    """
    Handle user login.

    This view handles the login process for users. If the request method is POST,
    it processes the login form data. If the form is valid, it attempts to
    authenticate the user with the provided username and password. If authentication
    is successful, the user is logged in and redirected to the main work screen.
    If the request method is GET, it displays the login form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the login form or the redirection.
    """
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


def clock_view(request):
    """Time clock views
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the context of datatime current time,
        and current date.
    """
    now = datetime.now()
    context = {
        'current_time': now.strftime("%H:%M:%S"),
        'current_date': now.strftime("%Y-%m-%d"),
    }
    return render(request, 'main_work_screen.html', context)


def user_check(request):
    user = request.user
    return render(request, 'main_work_screen.html', {'user': user})


def process_ods_file(ods_file_path):
    """
    Process the .ods file to create a map of incorrect to correct material names.

    Args:
        ods_file_path (str): The path to the .ods file.

    Returns:
        dict: A dictionary mapping incorrect material names to correct material names.
    """
    material_name_map = {}
    data = pyexcel_ods.get_data(ods_file_path)
    sheet = data.get("Sheet1", [])
    for row in sheet:
        if len(row) >= 2:
            incorrect_name = row[0].strip()
            correct_name = row[1].strip()
            material_name_map[incorrect_name] = correct_name
    return material_name_map


def update_material_names(lines, material_name_map):
    """
    Update material names in the provided lines based on the material name map.
    Args:
        lines (list of str): The lines of the file content.
        material_name_map (dict): A dictionary mapping incorrect
        material names to correct material names.
    Returns:
        list of str: The lines with updated material names.
    """
    updated_text_lines = []
    for line in lines:
        original_line = line.strip("() \n")
        updated_name = original_line
        for incorrect_name, correct_name in material_name_map.items():
            if incorrect_name in original_line:
                updated_name = original_line.replace(incorrect_name, correct_name)
                break
        updated_text_lines.append(f"({updated_name})\n")
    return updated_text_lines


def process_files(files, material_name_map):
    """
    Process the uploaded files, update material names, and create a zip file.

    Args:
        files (list of InMemoryUploadedFile): The uploaded files.
        material_name_map (dict): A dictionary mapping incorrect
        material names to correct material names.

    Returns:
        bytes: The content of the zip file containing the processed files.
    """
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for uploaded_file in files:
                if uploaded_file.name.endswith('.NC'):
                    file_content = uploaded_file.read().decode('utf-8')
                    lines = file_content.splitlines()
                    updated_lines = update_material_names(lines, material_name_map)
                    new_content = ''.join(updated_lines)
                    zip_file.writestr(uploaded_file.name, new_content)
        zip_buffer.seek(0)
        return zip_buffer.read()


def upload_file(request):
    """
    Handle file upload from the local disk, update material names,
    and return a zip file with modified content.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the zip file with modified files.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            material_name_map = process_ods_file('simple_automation/static/materials.ods')

            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="modified_files.zip"'
            response.write(process_files(files, material_name_map))

            return response
    else:
        form = UploadFileForm()

    return render(request, 'main_work_screen.html', {'form': form})
