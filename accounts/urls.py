from django.urls import path

from partyou.accounts.views import login


app_name = 'accounts'
urlpatterns = [

    path('login/', login, name='login'),
    path('alterar-dados/', views.update_user, name='update_user'),
    path('alterar-senha/', views.update_password, name='update_password'),
    path('registro/', views.register, name='register'),

]