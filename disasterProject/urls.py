"""disasterProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from cope_with_disaster import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='floods/')),
    path('floods/', views.home, name='flood_home'),
    path('floods/current_stats', views.stats, name='current_stats'),
    path('floods/states/<slug:state>', views.state_info, name='state_info'),
    path('floods/states/<slug:state>/<slug:code>', views.stations_view, name='station'),
    path('floods/predictions', views.predict, name='flood_predictions'),
    path('floods/under_development', views.undev, name='undev'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('about/', views.about, name='about')
]
