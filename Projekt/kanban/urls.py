"""
URL configuration for kanban project.

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
from rest_framework.authtoken import views as auth_views
import kanban_app.views as kanban_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', auth_views.obtain_auth_token),
    path('boards/create', kanban_views.create_board),
    path('boards/all', kanban_views.get_all_boards),
    path('boards/<int:pk>', kanban_views.get_board),
    path('boards/<int:board_id>/delete', kanban_views.delete_board),
    path('boards/<int:pk>/update', kanban_views.update_board),
    path('boards/<int:board_id>/add-members', kanban_views.add_member_to_board),
    path('boards/<int:board_id>/remove-members', kanban_views.remove_member_from_board),
    path('boards/<int:pk>/team-members', kanban_views.get_board_members),
    path('boards/<int:board_id>/columns', kanban_views.get_all_columns),
    path('columns/create', kanban_views.create_column),
    path('columns/<int:column_id>/update', kanban_views.update_column),
    path('columns/<int:column_id>/delete', kanban_views.delete_column),

]
