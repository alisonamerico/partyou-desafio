from django.urls import path

from partyou.produtos import views

app_name = 'produtos'
urlpatterns = [
    path('', views.index, name='index'),
    path('novo', views.new, name='new'),
    path('criar', views.create, name='create'),
]
