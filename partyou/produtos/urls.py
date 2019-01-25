from django.urls import path

from partyou.produtos import views

app_name = 'produtos'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.category, name='category'),
    path('produtos/<slug:slug>/', views.product, name='product'),
]
