from django.urls import path

from partyou.catalog import views

app_name = 'catalog'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.category, name='category'),
    path('produtos/<slug:slug>/', views.product, name='product'),
]
