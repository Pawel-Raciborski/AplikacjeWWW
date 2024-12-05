"""
URL configuration for lab2_project project.

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
from debug_toolbar.toolbar import debug_toolbar_urls
from lab2_app import views
from rest_framework.authtoken import views as auth_views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('osoba/create', views.create_osoba),
                  path('osoba/<int:pk>', views.get_osoba),
                  path('osoba/<int:pk>/delete', views.delete_osoba),
                  path('osoba/all', views.get_all_osoba),
                  path('osoba/alle', views.get_all_osoba_with_name),
                  path('stanowisko/create', views.create_stanowisko),
                  path('stanowisko/<int:pk>', views.get_stanowisko),
                  path('stanowisko/all', views.get_all_stanowisko),
                  path('stanowisko/<int:pk>/members', views.get_stanowisko_members),
                  path('api-auth', auth_views.obtain_auth_token),
                  path('osoba/<int:pk>/has-permission', views.osoba_view),
                  path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
              ] + debug_toolbar_urls()
