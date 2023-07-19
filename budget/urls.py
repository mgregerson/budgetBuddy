"""
URL configuration for budgetBuddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('projects', views.project_list, name='list'),
    path('accounts', views.account_list, name='account_list'),
    path('add_project', views.ProjectCreateView.as_view(), name='add_project'),
    path('add_account', views.AccountCreateView.as_view(), name='add_account'),
    path('projects/<slug:project_slug>', views.project_detail, name='project_detail'),
    path('accounts/<slug:account_slug>', views.account_detail, name='account_detail')
]
