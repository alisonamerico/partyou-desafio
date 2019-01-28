from django.urls import path

from partyou.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contact, name='contact'),
    # path('produto/', views.product, name='product'),
    # path('registro/', views.registro, name='registro'),

]
