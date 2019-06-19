"""dhbwroommanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from roommanager.views import download_and_analyse, test_model, retrieve_all, delete_models,retrieve_actual_date, retrieve_slot_inf
from roommanager.views import sign, main, room_form
from django.contrib.auth.views import auth_login, auth_logout
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', main, name='main'),
    path('room/<int:id>/', room_form, name="room"),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('sign/', sign, name='sign'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('test/', download_and_analyse, name='download_and_analyse'),
    path('<str:room_name>/test_model/', test_model, name='test_model'),
    path('allt', retrieve_all, name="retrieve_all"),
    path('one', retrieve_slot_inf, name="retrieve_slot_inf"),
    path('delete', delete_models, name="delete_models"),
    path('current', retrieve_actual_date, name="retrieve_actual_date")
]

