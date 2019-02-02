from django.urls import path

from partyou.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contact, name='contact'),
    path('registro/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('alterar-dados/', views.update_user, name='update_user'),
    path('alterar-senha/', views.update_password, name='update_password'),

]
