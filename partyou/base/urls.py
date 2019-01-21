from django.urls import path

from partyou.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contato, name='contato'),
    path('registro/', views.registro, name='registro'),
]
