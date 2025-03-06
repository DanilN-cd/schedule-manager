"""
URL configuration for testdip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from testapp.views import index_page, groups_page, prep_page, home_page, add_group, delete_group, add_prep, delete_prep, edit_prep, edit_group, run_algorithm_page, run_algorithm, upload_file, update_schedule, delete_schedule_entry, add_schedule_entry, move_schedule_entry, get_subject_id, export_excel, get_group_subjects

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('schedule/', index_page, name='schedule_page'),
    path('groups/', groups_page, name='groups_page'),
    path('groups/add/', add_group, name='add_group'),
    path('groups/delete/<int:group_id>/', delete_group, name='delete_group'),
    path('groups/edit/<int:group_id>/', edit_group, name='edit_group'),
    path('prepods/', prep_page, name='prepods_page'),
    path('prepods/add/', add_prep, name='add_prep'),
    path('prepods/edit/<int:prepod_id>/', edit_prep, name='edit_prep'),
    path('prepods/delete/<int:prepod_id>/', delete_prep, name='delete_prep'),
    path('run_algorithm/', run_algorithm_page, name='run_algorithm_page'),
    path('run_algorithm/execute/', run_algorithm, name='run_algorithm'),
    path('upload_file/', upload_file, name='upload_file'),
    path('schedule/update_schedule/', update_schedule, name='update_schedule'),
    path('schedule/delete_schedule_entry/', delete_schedule_entry, name='delete_schedule_entry'),
    path('schedule/add_schedule_entry/', add_schedule_entry, name='add_schedule_entry'),
    path('schedule/move_schedule_entry/', move_schedule_entry, name='move_schedule_entry'),
    path('schedule/get_subject_id/', get_subject_id, name='get_subject_id'),
    path("export_excel/", export_excel, name="export_excel"),
     path('schedule/get_group_subjects/', get_group_subjects, name='get_group_subjects'),
]

