"""Views for simple app"""
import zipfile
import io
from datetime import datetime
import django.contrib.auth
import pyexcel_ods
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
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            material_name_map = {}

            # Process .ods file to create material_name_map
            ods_file_path = 'static/materials.ods'
            data = pyexcel_ods.get_data(ods_file_path)
            sheet = data.get("Sheet1", [])
            for row in sheet:
                if len(row) >= 2:
                    incorrect_name = row[0].strip()
                    correct_name = row[1].strip()
                    material_name_map[incorrect_name] = correct_name

            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="modified_files.zip"'

            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for uploaded_file in files:
                        if uploaded_file.name.endswith('.NC'):
                            file_content = uploaded_file.read().decode('utf-8')
                            lines = file_content.splitlines()

                            # Function to update material names
                            def update_material_names(lines_nc, material_name):
                                updated_text_lines = []
                                for line in lines_nc:
                                    original_line = line.strip("() \n")
                                    updated_name = original_line
                                    for incorrect_name_in_sheet, correct_name_in_sheet in material_name.items():
                                        if incorrect_name_in_sheet in original_line:
                                            updated_name = original_line.replace(incorrect_name_in_sheet, correct_name_in_sheet)
                                            break
                                    updated_text_lines.append(f"({updated_name})\n")
                                return updated_text_lines

                            updated_lines = update_material_names(lines, material_name_map)
                            new_content = ''.join(updated_lines)
                            zip_file.writestr(uploaded_file.name, new_content)

                zip_buffer.seek(0)
                response.write(zip_buffer.read())

            return response
    else:
        form = UploadFileForm()

    return render(request, 'main_work_screen.html', {'form': form})

