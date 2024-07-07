"""Urls for simple automation app"""

from django.urls import path
from simple_automation import views as v

urlpatterns = [
    path('register/', v.user_register_view, name='register'),
    # path('logout/', v.user_logout, name='logout'),
    path('login/', v.user_login_view, name='simple_app.html'),
    path('main_work_screen', v.main_work_screen_view, name='main_work_screen.html'),
    path('main_work_screen', v.clock_view, name='main_work_screen.html'),
    path('update_file', v.upload_file, name='main_work_screen.html')
]
